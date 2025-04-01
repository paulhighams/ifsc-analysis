#from neo4j import __version__ as neo4j_version
#print(neo4j_version)

from neo4j import GraphDatabase
import pandas as pd
import requests
import jmespath as jm
import itertools
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response

#####################################################################

def format_color_groups(df):
    colors = ['gold', 'lightblue']
    x = df.copy()
    factors = list(x['Country'].unique())
    i = 0
    for factor in factors:
        style = f'background-color: {colors[i]}'
        x.loc[x['Country'] == factor, :] = style
        i = not i
    return x

def highlight_female(x):
	if "Female" in x.WCupComp:
		return ['background-color: gold']*4
	else:
		return ['background-color: lightblue']*4 


def highlight_current(x):
	if "(Current)" in x.Athlete:
		return ['background-color: gold']*3
	else:
		return ['background-color: lightblue']*3 

############################################################################

if  __name__ == '__main__':

	# connect to ifsc api
	# api-endpoint
	method = "get"
	base_url = "https://ifsc.results.info/api/v1/speed_records"

	#do the auth thing
	HEADERS = {
        'accept': 'application/json',
        'x-auth-token': '716fea88f31484ba117459341ee3474fd4dfa9fc'
	    }

	try:
	    r = requests.request(method, url = f'{base_url}', headers = HEADERS)
	    r.raise_for_status()
	except requests.exceptions.RequestException as e:
	    print (f"Error while connecting to {base_url}: {e}")
	
	# extracting data in json format
	data = r.json()
	world_speed_records = jm.search("""
	world_record.*[].{
		Athlete: name,
		Nation:country,
		Time: time,
		When: date,
		Where: event
	}
	""",data)

	region_male_speed_records = jm.search("""
	continental_records.*[].male[].{
		Athlete: name,
		Nation:country,
		Time: time,
		When: date,
		Where: event
	}
	""",data)

	region_female_speed_records = jm.search("""
	continental_records.*[].female[].{
		Athlete: name,
		Nation:country,
		Time: time,
		When: date,
		Where: event
	}
	""",data)

	world_speed_records_df = pd.DataFrame(world_speed_records)
	region_male_speed_records_df = pd.DataFrame(region_male_speed_records)
	region_female_speed_records_df = pd.DataFrame(region_female_speed_records)
	world_speed_records_df.set_index('Athlete',drop=True,inplace=True)
	region_male_speed_records_df.set_index('Athlete',drop=True,inplace=True)
	region_female_speed_records_df.set_index('Athlete',drop=True,inplace=True)

	# end of getting the speed records
	#--------------------------------------------------------

	#get 2024 rankings by category and gender, the 94 in the url is for 2024, change each year
	standings_tmp_cur_yr_df = pd.DataFrame(columns = ['Firstname','Lastname','Nation','Category','Comp1','Points1','Comp2','Points2','Comp3','Points3','Comp4','Points4','Comp5','Points5','Comp6','Points6'])   # create an empty df
	the_cats = [1, 2, 3, 5, 6, 7]   # categories of male/female -  lead/speed/boulder
	for my_cat in the_cats:
		base_url = "https://ifsc.results.info/api/v1/cups/94/dcat/"+str(my_cat)
		try:
			r = requests.request(method, url = f'{base_url}', headers = HEADERS)
			r.raise_for_status()
		except requests.exceptions.RequestException as e:
			print (f"Error while connecting to {base_url}: {e}")
	
		# extracting data in json format
		data = r.json()
		#print (data)
		standings_temp = jm.search("""
		ranking[*].{
			Firstname: firstname,
			Lastname: lastname,
			Nation: country,
			Category: events[0].dcat,
			Comp1: events[0].event_name,
			Points1: events[0].points
			Comp2: events[1].event_name,
			Points2: events[1].points
			Comp3: events[2].event_name,
			Points3: events[2].points
			Comp4: events[3].event_name,
			Points4: events[3].points
			Comp5: events[4].event_name,
			Points5: events[4].points
			Comp6: events[5].event_name,
			Points6: events[5].points
		}
		""",data)
		standings_temp_df = pd.DataFrame(standings_temp)
		standings_tmp_cur_yr_df = standings_tmp_cur_yr_df.append(standings_temp_df, ignore_index=True)

	#turn the columns for comps and points into rows, then rest the index to get the other columns back, and merge the name columns
	standings_cur_yr_df = pd.wide_to_long(standings_tmp_cur_yr_df,stubnames=['Comp','Points'],i=['Firstname','Lastname','Nation','Category'],j='timeline')
	standings_cur_yr_df.reset_index(inplace=True)
	standings_cur_yr_df['Athlete'] = standings_cur_yr_df['Firstname'].astype(str) +' '+ standings_cur_yr_df['Lastname'] +' ('+ standings_cur_yr_df['Nation']+')'
	#now make points float and add cumulative rows after each comp
	standings_cur_yr_df['Points'] = standings_cur_yr_df['Points'].astype(float)
	standings_cur_yr_df['Points'] = standings_cur_yr_df['Points'].fillna(0)
	standings_cur_yr_df['Comp'] = standings_cur_yr_df['Comp'].fillna('x')  #temporary until all results are in.

	#now do a loop to add everything up to get cumulative points per round
	standings_cur_yr_sort_df = standings_cur_yr_df.sort_values(by=['Category','Athlete','timeline'], ascending=[True,True,True])
	standings_cur_yr_sort_df.reset_index(inplace=True)

	cumpoints = []
	myCumPoints = 0
	myCategory = standings_cur_yr_sort_df['Category'][0]
	myAthlete = standings_cur_yr_sort_df['Athlete'][0]
	for ind in standings_cur_yr_sort_df.index:
		if myCategory == standings_cur_yr_sort_df['Category'][ind] and myAthlete == standings_cur_yr_sort_df['Athlete'][ind]:
			myCumPoints = myCumPoints + standings_cur_yr_sort_df['Points'][ind]
			cumpoints.append(myCumPoints)
			#print(ind,standings_cur_yr_sort_df['Athlete'][ind], standings_cur_yr_sort_df['Points'][ind], myCumPoints)
		else:
			myCategory = standings_cur_yr_sort_df['Category'][ind]
			myAthlete = standings_cur_yr_sort_df['Athlete'][ind]
			myCumPoints = standings_cur_yr_sort_df['Points'][ind]
			cumpoints.append(myCumPoints)
			#print(ind,standings_cur_yr_sort_df['Athlete'][ind], standings_cur_yr_sort_df['Points'][ind], myCumPoints)

	# add the series of cumulative points to the dataframe
	standings_cur_yr_sort_df['CumPoints'] = cumpoints

	# now have all 6 categories in a dataframe
	print ('now in dataframe')
	#print (standings_cur_yr_df)
	#print (standings_cur_yr_df.info())

	standings_cur_yr_male_lead_df = standings_cur_yr_sort_df[(standings_cur_yr_sort_df.Category==1)]
	standings_cur_yr_male_speed_df = standings_cur_yr_sort_df[(standings_cur_yr_sort_df.Category==2)]
	standings_cur_yr_male_boulder_df = standings_cur_yr_sort_df[(standings_cur_yr_sort_df.Category==3)]
	standings_cur_yr_female_lead_df = standings_cur_yr_sort_df[(standings_cur_yr_sort_df.Category==5)]
	standings_cur_yr_female_speed_df = standings_cur_yr_sort_df[(standings_cur_yr_sort_df.Category==6)]
	standings_cur_yr_female_boulder_df = standings_cur_yr_sort_df[(standings_cur_yr_sort_df.Category==7)]

	#now have to add ranking positions, by making timeline the index and then groupby on timeline, and rank on Cumpoints, then tidy up
	standings_cur_yr_male_lead_df.set_index('timeline', inplace=True)
	standings_cur_yr_male_lead_df['Rank'] = (standings_cur_yr_male_lead_df.groupby ('timeline').rank(ascending=False).CumPoints)
	standings_cur_yr_male_lead_df.drop(['index'], axis=1)
	standings_cur_yr_male_lead_df.reset_index(inplace=True)
	#
	standings_cur_yr_female_lead_df.set_index('timeline', inplace=True)
	standings_cur_yr_female_lead_df['Rank'] = (standings_cur_yr_female_lead_df.groupby ('timeline').rank(ascending=False).CumPoints)
	standings_cur_yr_female_lead_df.drop(['index'], axis=1)
	standings_cur_yr_female_lead_df.reset_index(inplace=True)
	#
	standings_cur_yr_male_speed_df.set_index('timeline', inplace=True)
	standings_cur_yr_male_speed_df['Rank'] = (standings_cur_yr_male_speed_df.groupby ('timeline').rank(ascending=False).CumPoints)
	standings_cur_yr_male_speed_df.drop(['index'], axis=1)
	standings_cur_yr_male_speed_df.reset_index(inplace=True)
	#
	standings_cur_yr_female_speed_df.set_index('timeline', inplace=True)
	standings_cur_yr_female_speed_df['Rank'] = (standings_cur_yr_female_speed_df.groupby ('timeline').rank(ascending=False).CumPoints)
	standings_cur_yr_female_speed_df.drop(['index'], axis=1)
	standings_cur_yr_female_speed_df.reset_index(inplace=True)
	#
	standings_cur_yr_male_boulder_df.set_index('timeline', inplace=True)
	standings_cur_yr_male_boulder_df['Rank'] = (standings_cur_yr_male_boulder_df.groupby ('timeline').rank(ascending=False).CumPoints)
	standings_cur_yr_male_boulder_df.drop(['index'], axis=1)
	standings_cur_yr_male_boulder_df.reset_index(inplace=True)
	#
	standings_cur_yr_female_boulder_df.set_index('timeline', inplace=True)
	standings_cur_yr_female_boulder_df['Rank'] = (standings_cur_yr_female_boulder_df.groupby ('timeline').rank(ascending=False).CumPoints)
	standings_cur_yr_female_boulder_df.drop(['index'], axis=1)
	standings_cur_yr_female_boulder_df.reset_index(inplace=True)
	#

	# first select only events that have happened, then just get the top 10 ranking, change variable if you don't want 10
	top10 = 10
	# now for each category/dataframe
	mytempdf = standings_cur_yr_male_lead_df.loc[(standings_cur_yr_male_lead_df['Comp']!='x')]
	mytemp2df = mytempdf.groupby(['Category'], as_index=False)['timeline'].max()
	maxComp = mytemp2df['timeline'].loc[mytemp2df.index[0]]
	catComps = list(range(1,maxComp+1,1))
	mytempdf = standings_cur_yr_male_lead_df.loc[standings_cur_yr_male_lead_df['timeline'] .isin (catComps)]
	stand_cur_yr_male_lead_df = mytempdf.loc[(mytempdf['Rank']<top10+1)]
	stand_cur_yr_male_lead_df.sort_values(by =['timeline', 'Rank'], ascending=False, inplace = True)
	#
	mytempdf = standings_cur_yr_female_lead_df.loc[(standings_cur_yr_female_lead_df['Comp']!='x')]
	mytemp2df = mytempdf.groupby(['Category'], as_index=False)['timeline'].max()
	maxComp = mytemp2df['timeline'].loc[mytemp2df.index[0]]
	catComps = list(range(1,maxComp+1,1))
	mytempdf = standings_cur_yr_female_lead_df.loc[standings_cur_yr_female_lead_df['timeline'] .isin (catComps)]
	stand_cur_yr_female_lead_df = mytempdf.loc[(mytempdf['Rank']<top10+1)]
	stand_cur_yr_female_lead_df.sort_values(by =['timeline', 'Rank'], ascending=False, inplace = True)
	#
	mytempdf = standings_cur_yr_male_speed_df.loc[(standings_cur_yr_male_speed_df['Comp']!='x')]
	mytemp2df = mytempdf.groupby(['Category'], as_index=False)['timeline'].max()
	maxComp = mytemp2df['timeline'].loc[mytemp2df.index[0]]
	catComps = list(range(1,maxComp+1,1))
	mytempdf = standings_cur_yr_male_speed_df.loc[standings_cur_yr_male_speed_df['timeline'] .isin (catComps)]
	stand_cur_yr_male_speed_df = mytempdf.loc[(mytempdf['Rank']<top10+1)]
	stand_cur_yr_male_speed_df.sort_values(by =['timeline', 'Rank'], ascending=False, inplace = True)
	#
	mytempdf = standings_cur_yr_female_speed_df.loc[(standings_cur_yr_female_speed_df['Comp']!='x')]
	mytemp2df = mytempdf.groupby(['Category'], as_index=False)['timeline'].max()
	maxComp = mytemp2df['timeline'].loc[mytemp2df.index[0]]
	catComps = list(range(1,maxComp+1,1))
	mytempdf = standings_cur_yr_female_speed_df.loc[standings_cur_yr_female_speed_df['timeline'] .isin (catComps)]
	stand_cur_yr_female_speed_df = mytempdf.loc[(mytempdf['Rank']<top10+1)]
	stand_cur_yr_female_speed_df.sort_values(by =['timeline', 'Rank'], ascending=False, inplace = True)
	#
	mytempdf = standings_cur_yr_male_boulder_df.loc[(standings_cur_yr_male_boulder_df['Comp']!='x')]
	mytemp2df = mytempdf.groupby(['Category'], as_index=False)['timeline'].max()
	maxComp = mytemp2df['timeline'].loc[mytemp2df.index[0]]
	catComps = list(range(1,maxComp+1,1))
	mytempdf = standings_cur_yr_male_boulder_df.loc[standings_cur_yr_male_boulder_df['timeline'] .isin (catComps)]
	stand_cur_yr_male_boulder_df = mytempdf.loc[(mytempdf['Rank']<top10+1)]
	stand_cur_yr_male_boulder_df.sort_values(by =['timeline', 'Rank'], ascending=False, inplace = True)
	#
	mytempdf = standings_cur_yr_female_boulder_df.loc[(standings_cur_yr_female_boulder_df['Comp']!='x')]
	mytemp2df = mytempdf.groupby(['Category'], as_index=False)['timeline'].max()
	maxComp = mytemp2df['timeline'].loc[mytemp2df.index[0]]
	catComps = list(range(1,maxComp+1,1))
	mytempdf = standings_cur_yr_female_boulder_df.loc[standings_cur_yr_female_boulder_df['timeline'] .isin (catComps)]
	stand_cur_yr_female_boulder_df = mytempdf.loc[(mytempdf['Rank']<top10+1)]
	stand_cur_yr_female_boulder_df.sort_values(by =['timeline', 'Rank'], ascending=False, inplace = True)

	# now do a pretty graph for each category
	pic20ml = px.line(stand_cur_yr_male_lead_df, x = 'Comp', y = 'Rank', color = 'Athlete', text='Rank', markers=True)
	pic20ml.update_traces(marker=dict(size=30))
	pic20ml.update_traces(textposition='middle center')
	pic20ml.update_yaxes(autorange='reversed',title='Rank',visible=True, showticklabels=True)
	pic20ml.update_xaxes(autorange='reversed',title='Comp',visible=True, showticklabels=True)
	pic20ml.update_layout(xaxis=dict(showgrid=False), yaxis=dict(dict(showgrid=False),dtick=1), legend=dict(traceorder='reversed'), height = 1000 )
	#pic20ml.show()
	#
	pic20fl = px.line(stand_cur_yr_female_lead_df, x = 'Comp', y = 'Rank', color = 'Athlete', text='Rank', markers=True)
	pic20fl.update_traces(marker=dict(size=30))
	pic20fl.update_traces(textposition='middle center')
	pic20fl.update_yaxes(autorange='reversed',title='Rank',visible=True, showticklabels=True)
	pic20fl.update_xaxes(autorange='reversed',title='Comp',visible=True, showticklabels=True)
	pic20fl.update_layout(xaxis=dict(showgrid=False), yaxis=dict(dict(showgrid=False),dtick=1), legend=dict(traceorder='reversed'), height = 1000 )
	#pic20fl.show()
	#
	pic20ms = px.line(stand_cur_yr_male_speed_df, x = 'Comp', y = 'Rank', color = 'Athlete', text='Rank', markers=True)
	pic20ms.update_traces(marker=dict(size=30))
	pic20ms.update_traces(textposition='middle center')
	pic20ms.update_yaxes(autorange='reversed',title='Rank',visible=True, showticklabels=True)
	pic20ms.update_xaxes(autorange='reversed',title='Comp',visible=True, showticklabels=True)
	pic20ms.update_layout(xaxis=dict(showgrid=False), yaxis=dict(dict(showgrid=False),dtick=1), legend=dict(traceorder='reversed'), height = 1000 )
	#ic20ms.show()
	#
	pic20fs = px.line(stand_cur_yr_female_speed_df, x = 'Comp', y = 'Rank', color = 'Athlete', text='Rank', markers=True)
	pic20fs.update_traces(marker=dict(size=30))
	pic20fs.update_traces(textposition='middle center')
	pic20fs.update_yaxes(autorange='reversed',title='Rank',visible=True, showticklabels=True)
	pic20fs.update_xaxes(autorange='reversed',title='Comp',visible=True, showticklabels=True)
	pic20fs.update_layout(xaxis=dict(showgrid=False), yaxis=dict(dict(showgrid=False),dtick=1), legend=dict(traceorder='reversed'), height = 1000 )
	#pic20fs.show()
	#
	pic20mb = px.line(stand_cur_yr_male_boulder_df, x = 'Comp', y = 'Rank', color = 'Athlete', text='Rank', markers=True)
	pic20mb.update_traces(marker=dict(size=30))
	pic20mb.update_traces(textposition='middle center')
	pic20mb.update_yaxes(autorange='reversed',title='Rank',visible=True, showticklabels=True)
	pic20mb.update_xaxes(autorange='reversed',title='Comp',visible=True, showticklabels=True)
	pic20mb.update_layout(xaxis=dict(showgrid=False), yaxis=dict(dict(showgrid=False),dtick=1), legend=dict(traceorder='reversed'), height=1000 )
	#pic20mb.show()
	#
	pic20fb = px.line(stand_cur_yr_female_boulder_df, x = 'Comp', y = 'Rank', color = 'Athlete', text='Rank', markers=True)
	pic20fb.update_traces(marker=dict(size=30))
	pic20fb.update_traces(textposition='middle center')
	pic20fb.update_yaxes(autorange='reversed',title='Rank',visible=True, showticklabels=True)
	pic20fb.update_xaxes(autorange='reversed',title='Comp',visible=True, showticklabels=True)
	pic20fb.update_layout(xaxis=dict(showgrid=False), yaxis=dict(dict(showgrid=False),dtick=1), legend=dict(traceorder='reversed'), height = 1000 )
	#pic20fb.show()
	#

	# end of the current year standings
	#-----------------------------------------------------------------------------------------------------------------------------------
	#
	#make a connection to the neo4j database
	#
	conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="Charl1e")
	#
	# login to datapane at cmd prompt
	#$datapane login --token=63cd8316bd51c9b7c59b7eed012081ed7e8d5d16
	#
	# get the current date to use in queries, otherwise you will count comps that have not happened yet
	curDT = datetime.now ()
	todayStr = curDT.strftime("%Y-%m-%d")
	#print (todayStr)
	TwoYearsAgo = datetime.now() - relativedelta(years=3)
	TwoYearsOnly = TwoYearsAgo.strftime('%Y')
	TwoYearsAgoJanFirst = TwoYearsOnly + "-01-01"
	#print(TwoYearsAgoJanFirst)
	
	query_0 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Boulder" and yr.YearName in [2024,2022,2023]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, StartDate, Position
	'''

	query_1 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Lead" and yr.YearName in [2024,2022,2023]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, StartDate, Position
	'''
	
	query_2 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Speed" and yr.YearName in [2024,2022,2023]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, StartDate, Position
	'''

	query_3 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Boulder-Lead" and yr.YearName in [2024,2022,2023]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, StartDate, Position
	'''

	query_10 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE e.EventTypeName <> "World Cup" AND att.FinishPosition < 4 AND ct.CompTypeName = "Boulder" and yr.YearName in [2024,2022,2023]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position
	ORDER BY Gender, StartDate, Position
	'''

	query_11 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE e.EventTypeName <> "World Cup" AND att.FinishPosition < 4 AND ct.CompTypeName = "Lead" and yr.YearName in [2024,2022,2023]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position
	ORDER BY Gender, StartDate, Position
	'''

	query_12 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE e.EventTypeName <> "World Cup" AND att.FinishPosition < 4 AND ct.CompTypeName = "Speed" and yr.YearName in [2024,2022,2023]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position
	ORDER BY Gender, StartDate, Position
	'''

	query_13 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE e.EventTypeName <> "World Cup" AND att.FinishPosition < 4 AND ct.CompTypeName = "Boulder-Lead" and yr.YearName in [2024,2022,2023]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position
	ORDER BY Gender, StartDate, Position
	'''


	#query_40 = '''
	#'''
	#query_41 = '''
	#'''
	
	#run the queries and put the answer in dataframes
	dtf_0 = pd.DataFrame([dict(_) for _ in conn.query(query_0)])
	dtf_1 = pd.DataFrame([dict(_) for _ in conn.query(query_1)])
	dtf_2 = pd.DataFrame([dict(_) for _ in conn.query(query_2)])
	dtf_3 = pd.DataFrame([dict(_) for _ in conn.query(query_3)])
	dtf_10 = pd.DataFrame([dict(_) for _ in conn.query(query_10)])
	dtf_11 = pd.DataFrame([dict(_) for _ in conn.query(query_11)])
	dtf_12 = pd.DataFrame([dict(_) for _ in conn.query(query_12)])
	dtf_13 = pd.DataFrame([dict(_) for _ in conn.query(query_13)])
	#dtf_41 = pd.DataFrame([dict(_) for _ in conn.query(query_41)])
	
	dtf_0A = dtf_0.pivot(index=['Year','StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_1A = dtf_1.pivot(index=['Year','StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_2A = dtf_2.pivot(index=['Year','StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_3A = dtf_3.pivot(index=['Year','StartDate','Event'],columns=['Gender','Position'], values='Athlete')

	dtf_10A = dtf_10.pivot(index=['StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_11A = dtf_11.pivot(index=['StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_12A = dtf_12.pivot(index=['StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_13A = dtf_13.pivot(index=['StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	
	#produce report files

	#title="Boulder Events"
	dtf_0A.to_csv('last_3_years_world_cups_boulder.csv', header=True, index=True) 
	dtf_10A.to_csv('last_3_years_world_champs_boulder.csv', header=True, index=True) 
	#dp.Plot (pic20mb, label='Male Top 10 Ranking for 2024', caption=updateBoulderCaption),
	#dp.Plot (pic20fb, label='Female Top 10 Ranking for 2024', caption=updateBoulderCaption),

	#title="Lead Events"
	dtf_1A.to_csv('last_3_years_world_cups_lead.csv', header=True, index=True) 
	dtf_11A.to_csv('last_3_years_world_champs_lead.csv', header=True, index=True) 
	#dp.Plot (pic20ml, label='Male Top 10 Ranking for 2024', caption=updateLeadCaption),
	#dp.Plot (pic20fl, label='Female Top 10 Ranking for 2024', caption=updateLeadCaption),

	#title="Speed Events"
	dtf_2A.to_csv('last_3_years_world_cups_speed.csv', header=True, index=True) 
	dtf_12A.to_csv('last_3_years_world_champs_speed.csv', header=True, index=True) 
	world_speed_records_df.to_csv('speed_world_records.csv', header=True, index=True) 
	region_male_speed_records_df.to_csv('speed_regional_records_male.csv', header=True, index=True) 
	region_female_speed_records_df.to_csv('speed_regional_records_female.csv', header=True, index=True) 
	#dp.Plot (pic20ms, label='Male Top 10 Ranking for 2024', caption=updateSpeedCaption),
	#dp.Plot (pic20fs, label='Female Top 10 Ranking for 2024', caption=updateSpeedCaption),


	#title="Boulder-Lead Events"
	dtf_3A.to_csv('last_3_years_world_cups_boulderlead.csv', header=True, index=True)
	dtf_13A.to_csv('last_3_years_world_champs_boulderlead.csv', header=True, index=True)

				

	
    #path='LastThreeYears.html',
    #name='IFSC Events last 3 years',
	
	#
	# how to close the connection to the database
	#
	conn.close()
	print("thanks for all the fish")




