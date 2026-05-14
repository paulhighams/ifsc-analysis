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
from dotenv import load_dotenv
import os

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

	# get credentials
	load_dotenv()
	MY_URI = os.getenv("NEO4J_URI")
	MY_USER = os.getenv("NEO4J_USERNAME")
	MY_PWD = os.getenv("NEO4J_PASSWORD")
	MY_TOKEN = os.getenv("WORLD_CLIMBING_TOKEN")

	# connect to ifsc api
	# api-endpoint
	method = "get"
	base_url = "https://ifsc.results.info/api/v1/speed_records"

	#do the auth thing
	HEADERS = {
        'accept': 'application/json',
        'x-auth-token': MY_TOKEN
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

	#-----------------------------------------------------------------------------------------------------------------------------------
	#
	#make a connection to the neo4j database
	#
	conn = Neo4jConnection(uri=MY_URI, user=MY_USER, pwd=MY_PWD)
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
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Boulder" and yr.YearName in [2024,2025,2026]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, StartDate, Position
	'''

	query_1 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Lead" and yr.YearName in [2024,2025,2026]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, StartDate, Position
	'''
	
	query_2 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Speed" and yr.YearName in [2024,2025,2026]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, StartDate, Position
	'''

	#query_3 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	#MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	#MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	#WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Boulder-Lead" and yr.YearName in [2024,2025,2026]
	#RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position, yr.YearName AS Year
	#ORDER BY Gender, StartDate, Position
	#'''

	query_10 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE e.EventTypeName <> "World Cup" AND att.FinishPosition < 4 AND ct.CompTypeName = "Boulder" and yr.YearName in [2024,2025,2026]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position
	ORDER BY Gender, StartDate, Position
	'''

	query_11 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE e.EventTypeName <> "World Cup" AND att.FinishPosition < 4 AND ct.CompTypeName = "Lead" and yr.YearName in [2024,2025,2026]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position
	ORDER BY Gender, StartDate, Position
	'''

	query_12 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE e.EventTypeName <> "World Cup" AND att.FinishPosition < 4 AND ct.CompTypeName = "Speed" and yr.YearName in [2024,2025,2026]
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position
	ORDER BY Gender, StartDate, Position
	'''

	#query_13 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	#MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	#MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	#WHERE e.EventTypeName <> "World Cup" AND att.FinishPosition < 4 AND ct.CompTypeName = "Boulder-Lead" and yr.YearName in [2024,2025,2026]
	#RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, ev.EventName AS Event, ev.StartDate AS StartDate, att.FinishPosition AS Position
	#ORDER BY Gender, StartDate, Position
	#'''


	#query_40 = '''
	#'''
	#query_41 = '''
	#'''
	
	#run the queries and put the answer in dataframes
	dtf_0 = pd.DataFrame([dict(_) for _ in conn.query(query_0)])
	dtf_1 = pd.DataFrame([dict(_) for _ in conn.query(query_1)])
	dtf_2 = pd.DataFrame([dict(_) for _ in conn.query(query_2)])
	#dtf_3 = pd.DataFrame([dict(_) for _ in conn.query(query_3)])
	dtf_10 = pd.DataFrame([dict(_) for _ in conn.query(query_10)])
	dtf_11 = pd.DataFrame([dict(_) for _ in conn.query(query_11)])
	dtf_12 = pd.DataFrame([dict(_) for _ in conn.query(query_12)])
	#dtf_13 = pd.DataFrame([dict(_) for _ in conn.query(query_13)])
	#dtf_41 = pd.DataFrame([dict(_) for _ in conn.query(query_41)])
	
	#remove results for 2025 Wujiang because you can't pivot a tie
	dtf_1clean = dtf_1.query('Event != "WC Wujiang 2025"' )
	#print (dtf_1clean)
	#print (dtf_1clean.dtypes)

	# add in results for 2025 wujiang to cope with the tie
	dtf_1add = pd.DataFrame ({"Gender": ["Female","Female","Female","Male","Male","Male"],
		"Athlete": ["Erin MCNEICE and Chaehyun SEO","not awarded","Annie SANDERS","Sorato ANRAKU","Neo SUZUKI","Alberto GINÉS LÓPEZ"],
		"Event": ["WC Wujiang 2025","WC Wujiang 2025","WC Wujiang 2025","WC Wujiang 2025","WC Wujiang 2025","WC Wujiang 2025"],
		"StartDate": ["2025-04-25","2025-04-25","2025-04-25","2025-04-25","2025-04-25","2025-04-25"],
		"Position": [1,2,3,1,2,3],
		"Year": [2025,2025,2025,2025,2025,2025]})
	dtf_1fix = pd.concat([dtf_1clean, dtf_1add], ignore_index=True)
	dtf_1fixed = dtf_1fix.sort_values(['Gender','StartDate','Position'], axis=0, ascending=[True,True,True])
	#print (dtf_1fixed)
	dtf_0A = dtf_0.pivot(index=['Year','StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_1A = dtf_1fixed.pivot(index=['Year','StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_2A = dtf_2.pivot(index=['Year','StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	#dtf_3A = dtf_3.pivot(index=['Year','StartDate','Event'],columns=['Gender','Position'], values='Athlete')


	dtf_10A = dtf_10.pivot(index=['StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_11A = dtf_11.pivot(index=['StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	dtf_12A = dtf_12.pivot(index=['StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	#dtf_13A = dtf_13.pivot(index=['StartDate','Event'],columns=['Gender','Position'], values='Athlete')
	
	#produce report files

	#title="Boulder Events"
	dtf_0A.to_csv('last_3_years_world_cups_boulder.csv', header=True, index=True) 
	dtf_10A.to_csv('last_3_years_world_champs_boulder.csv', header=True, index=True) 
	#dp.Plot (pic20mb, label='Male Top 10 Ranking for 2025', caption=updateBoulderCaption),
	#dp.Plot (pic20fb, label='Female Top 10 Ranking for 2025', caption=updateBoulderCaption),

	#title="Lead Events"
	dtf_1A.to_csv('last_3_years_world_cups_lead.csv', header=True, index=True) 
	dtf_11A.to_csv('last_3_years_world_champs_lead.csv', header=True, index=True) 
	#dp.Plot (pic20ml, label='Male Top 10 Ranking for 2025', caption=updateLeadCaption),
	#dp.Plot (pic20fl, label='Female Top 10 Ranking for 2025', caption=updateLeadCaption),

	#title="Speed Events"
	dtf_2A.to_csv('last_3_years_world_cups_speed.csv', header=True, index=True) 
	dtf_12A.to_csv('last_3_years_world_champs_speed.csv', header=True, index=True) 
	world_speed_records_df.to_csv('speed_world_records.csv', header=True, index=True) 
	region_male_speed_records_df.to_csv('speed_regional_records_male.csv', header=True, index=True) 
	region_female_speed_records_df.to_csv('speed_regional_records_female.csv', header=True, index=True) 
	#dp.Plot (pic20ms, label='Male Top 10 Ranking for 2025', caption=updateSpeedCaption),
	#dp.Plot (pic20fs, label='Female Top 10 Ranking for 2025', caption=updateSpeedCaption),


	#title="Boulder-Lead Events"
	#dtf_3A.to_csv('last_3_years_world_cups_boulderlead.csv', header=True, index=True)
	#dtf_13A.to_csv('last_3_years_world_champs_boulderlead.csv', header=True, index=True)


	#
	# how to close the connection to the database
	#
	conn.close()
	print("thanks for all the fish")




