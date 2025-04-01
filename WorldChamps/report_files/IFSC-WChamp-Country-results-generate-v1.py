#from neo4j import __version__ as neo4j_version
#print(neo4j_version)

from math import nan
from neo4j import GraphDatabase
import pandas as pd
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

#--------------------------------------------------------------
def format_color_groups(df):
    colors = ['gold', 'lightblue']
    x = df.copy()
    factors = list(x['WChampEvent'].unique())
    i = 0
    for factor in factors:
        style = f'background-color: {colors[i]}'
        x.loc[x['WChampEvent'] == factor, :] = style
        i = not i
    return x
#-----------------------------------------------------------------
def format_color_groups2(df):
    colors = ['lemonchiffon', 'lightcyan']
    x = df.copy()
    factors = list(x['WChampEvent'].unique())
    i = 0
    for factor in factors:
        style = f'background-color: {colors[i]}'
        x.loc[x['WChampEvent'] == factor, :] = style
        i = not i
    return x
#-----------------------------------------------------------------
if  __name__ == '__main__':
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
	TwoYearsAgo = datetime.now() - relativedelta(years=2)
	TwoYearsOnly = TwoYearsAgo.strftime('%Y')
	TwoYearsAgoJanFirst = TwoYearsOnly + "-01-01"
	#print(TwoYearsAgoJanFirst)
	
	# WChamp win and podiums by athlete, by discipline for Male
	query_1 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ct.CompTypeName as Discipline, ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as NumWChampGold, Count(att.FinTwo) as NumWChampSilver, Count(att.FinThree) as NumWChampBronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY NumWChampGold DESC, NumWChampSilver DESC, NumWChampBronze DESC
	'''

	# WChamp win and podiums by athlete, by discipline for Female
	query_2 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ct.CompTypeName as Discipline, ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as NumWChampGold, Count(att.FinTwo) as NumWChampSilver, Count(att.FinThree) as NumWChampBronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY NumWChampGold DESC, NumWChampSilver DESC, NumWChampBronze DESC
	'''
	# WChamp win and podiums by athlete, aa discipline for Male
	query_3 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as NumWChampGold, Count(att.FinTwo) as NumWChampSilver, Count(att.FinThree) as NumWChampBronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY NumWChampGold DESC, NumWChampSilver DESC, NumWChampBronze DESC
	'''

	# WChamp win and podiums by athlete, aa discipline for Female
	query_4 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as NumWChampGold, Count(att.FinTwo) as NumWChampSilver, Count(att.FinThree) as NumWChampBronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY NumWChampGold DESC, NumWChampSilver DESC, NumWChampBronze DESC
	'''

	#get the previous podiums for each discipline
	query_6 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Boulder"
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, Year DESC, Position
	'''

	query_7 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Lead"
	RETURN ath.Sex AS Gender, collect(ath.PersonName) AS Athlete, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, Year DESC, Position
	'''
	
	query_8 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 AND ct.CompTypeName = "Speed"
	RETURN ath.Sex AS Gender, ath.PersonName AS Athlete, att.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, Year DESC, Position
	'''

	#Country Medal Table World Championships - medals by gold, silver, bronze, total
	query_12 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4
	RETURN cntry.CountryName as Country, COUNT(att.FinOne) as Gold, COUNT(att.FinTwo) AS Silver, COUNT(att.FinThree) AS Bronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY Total DESC, Gold DESC, Silver DESC, Bronze DESC
	'''

	#Country Medal Table World Championships - medals by gold, silver, bronze, total for each discipline
	query_13 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4
	RETURN cntry.CountryName as Country, ct.CompTypeName as Discipline, COUNT(att.FinOne) as Gold, COUNT(att.FinTwo) AS Silver, COUNT(att.FinThree) AS Bronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY Total DESC, Gold DESC, Silver DESC, Bronze DESC
	'''

	#Number of athletes who have Podiumed at World Championships per country per discipline
	query_14 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[p:PODIUM]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, ct.CompTypeName AS Discipline, count(DISTINCT ath.PersonName) as NumAthleteswithWChampPodiums
	ORDER BY NumAthleteswithWChampPodiums DESC
	'''
	
	#Number of athletes who have won at World Championships per country per discipline
	query_15 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[w:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, ct.CompTypeName AS Discipline, count(DISTINCT ath.PersonName) as NumAthleteswithWChampWins
	ORDER BY NumAthleteswithWChampWins DESC
	'''

	#Country Medal Table World Championships - medals by gold, silver, bronze, total
	query_16 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4
	RETURN ev.EventName as WChampEvent, cntry.CountryName as Country, COUNT(att.FinOne) as Gold, COUNT(att.FinTwo) AS Silver, COUNT(att.FinThree) AS Bronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY WChampEvent DESC, Total DESC, Gold DESC, Silver DESC, Bronze DESC
	'''

	#Country Medal Table World Championships - medals by gold, silver, bronze, total for each discipline
	query_17 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4
	RETURN ev.EventName as WChampEvent, cntry.CountryName as Country, ct.CompTypeName as Discipline, COUNT(att.FinOne) as Gold, COUNT(att.FinTwo) AS Silver, COUNT(att.FinThree) AS Bronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY WChampEvent DESC, Total DESC, Gold DESC, Silver DESC, Bronze DESC
	'''

	#Number of athletes who have Podiumed at World Championships per country all disciplines
	query_18 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[p:PODIUM]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, count(DISTINCT ath.PersonName) as NumAthleteswithWChampPodiums
	ORDER BY NumAthleteswithWChampPodiums DESC
	'''
	
	#Number of athletes who have won at World Championships per country all disciplines
	query_19 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[w:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, count(DISTINCT ath.PersonName) as NumAthleteswithWChampWins
	ORDER BY NumAthleteswithWChampWins DESC
	'''

	#Number of athletes to represent a country by discipline at world champs
	query_20 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Championship'}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WITH ev.EventName AS Event, cntry.IOCAlpha3 AS Country, ct.CompTypeName AS Discipline, count(DISTINCT ath.PersonName) AS NumAthletes
	ORDER BY NumAthletes DESC
	LIMIT 20
	RETURN Event AS Event, Country AS Country, Discipline AS Discipline, NumAthletes AS NumTeam
    ORDER BY Event,Discipline,Country
	'''
	
	#Number of athletes competing by country at world champs
	query_21 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Championship'})
	WITH  ev.EventName AS Event, cntry.IOCAlpha3 AS Country, count(DISTINCT ath.PersonName) AS TotalAthletes
	ORDER BY TotalAthletes DESC
	LIMIT 20
	RETURN Event, Country+' - '+TotalAthletes AS TotalTeam
	'''
	
	#Number of countries competing at world champs
	query_22 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Championship'})
	RETURN ev.EventName AS Event, count(DISTINCT cntry.CountryName) AS NumCountries
	ORDER BY Event
	'''
	#Number of countries competing by discipline at world champs
	query_23 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Championship'}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ev.EventName AS Event, ct.CompTypeName AS Discipline, count(DISTINCT cntry.CountryName) AS NumCountries
	ORDER BY Event, Discipline
	'''

	# Number of Athletes competing at World Champs
	query_25 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	WHERE e.EventTypeName = 'World Championship'
	RETURN ev.EventName AS Event, count(DISTINCT ath.PersonName) AS NumAthletes
	ORDER BY Event
	'''

	# Number of Athletes competing by discipline at World Champs
	query_26 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ev.EventName AS Event, ct.CompTypeName AS Discipline, count(att) as NumAthletes
	ORDER BY Event, Discipline
	'''


	#list of the world championships, by country and venue
	query_28 = '''MATCH (ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Championship'}),
      	(v:Venue)-[:HOSTS]->(ev:Event)-[:CONSISTS_OF]->(cmp:Competition),
      	(v:Venue)-[:IS_PART_OF]->(c:Country)
		WHERE  ev.StartDate < date("'''+todayStr+'''")
		RETURN c.CountryName AS Country, ev.EventName AS EventName, ev.StartDate AS Start, ev.EndDate AS Finish,
		       v.VenueName AS Venue, count(cmp) AS NumComps
		ORDER by ev.StartDate
	'''
	#get a list of current athletes - means they have competed in 2021 or 2022
	query_29M = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		WHERE  ev.StartDate > date("'''+TwoYearsAgoJanFirst+'''")
		RETURN DISTINCT ath.PersonName AS Athlete,cntry.CountryName AS Country
		ORDER BY Country
	'''
	query_29F = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		WHERE  ev.StartDate > date("'''+TwoYearsAgoJanFirst+'''")
		RETURN DISTINCT ath.PersonName AS Athlete,cntry.CountryName AS Country
		ORDER BY Country
	'''
	#Number of WChamps attended by an Athlete (sex) in a single discipline
	query_30 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_31 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_32 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_33 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_34 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_35 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_36 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_37 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_51 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_52 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	# as above but all disciplines - the reason for the left (...,11) is to count 2014 as one thing not 2
	query_38 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
	query_39 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWChamps
		ORDER BY NumWChamps DESC
	'''
    # youngest and oldest queries
	# youngest winner
	query_40 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: $qgender})-[att:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: $discipline})
		RETURN ct.CompTypeName AS Discipline, ath.Sex AS Gender, ath.PersonName+' ('+cntry.IOCAlpha3+') '+left(cmp.CompetitionName, 11) AS Athlete, MIN(duration.inMonths(ath.DoB, ev.StartDate)) AS Age 
		ORDER BY Age
		LIMIT 1
	'''
	# youngest podium
	query_41 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: $qgender})-[att:PODIUM]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: $discipline})
		RETURN ct.CompTypeName AS Discipline, ath.Sex AS Gender, ath.PersonName+' ('+cntry.IOCAlpha3+') '+left(cmp.CompetitionName, 11) AS Athlete, MIN(duration.between(ath.DoB, ev.StartDate)) AS Age
		ORDER BY Age
		LIMIT 1
	'''
	# youngest in final
	query_42 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: $qgender})-[att:IN_FINAL]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: $discipline})
		RETURN ct.CompTypeName AS Discipline, ath.Sex AS Gender, ath.PersonName+' ('+cntry.IOCAlpha3+') '+left(cmp.CompetitionName, 11) AS Athlete, MIN(duration.between(ath.DoB, ev.StartDate)) AS Age
		ORDER BY Age
		LIMIT 1
	'''
	# youngest attends
	query_43 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: $qgender})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: $discipline})
		RETURN ct.CompTypeName AS Discipline, ath.Sex AS Gender, ath.PersonName+' ('+cntry.IOCAlpha3+') '+left(cmp.CompetitionName, 11) AS Athlete, MIN(duration.between(ath.DoB, ev.StartDate)) AS Age
		ORDER BY Age
		LIMIT 1
	'''
	# oldest winner
	query_45 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: $qgender})-[att:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: $discipline})
		WHERE ath.DoB IS NOT NULL
		RETURN ct.CompTypeName AS Discipline, ath.Sex AS Gender, ath.PersonName+' ('+cntry.IOCAlpha3+') '+left(cmp.CompetitionName, 11) AS Athlete, MAX(duration.inMonths(ath.DoB, ev.StartDate)) AS Age 
		ORDER BY Age DESC
		LIMIT 1
	'''
	# oldest podium
	query_46 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: $qgender})-[att:PODIUM]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: $discipline})
		WHERE ath.DoB IS NOT NULL
		RETURN ct.CompTypeName AS Discipline, ath.Sex AS Gender, ath.PersonName+' ('+cntry.IOCAlpha3+') '+left(cmp.CompetitionName, 11) AS Athlete, MAX(duration.between(ath.DoB, ev.StartDate)) AS Age
		ORDER BY Age DESC
		LIMIT 1
	'''
	# oldest in final
	query_47 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: $qgender})-[att:IN_FINAL]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: $discipline})
		WHERE ath.DoB IS NOT NULL
		RETURN ct.CompTypeName AS Discipline, ath.Sex AS Gender, ath.PersonName+' ('+cntry.IOCAlpha3+') '+left(cmp.CompetitionName, 11) AS Athlete, MAX(duration.between(ath.DoB, ev.StartDate)) AS Age
		ORDER BY Age DESC
		LIMIT 1
	'''
	# oldest attends
	query_48 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: $qgender})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: $discipline})
		WHERE ath.DoB IS NOT NULL
		RETURN ct.CompTypeName AS Discipline, ath.Sex AS Gender, ath.PersonName+' ('+cntry.IOCAlpha3+') '+left(cmp.CompetitionName, 11) AS Athlete, MAX(duration.between(ath.DoB, ev.StartDate)) AS Age
		ORDER BY Age DESC
		LIMIT 1
	'''
	# best finish by discipline, gender and country
	query_50 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
		WHERE ct.CompTypeName IN ["Lead","Speed","Boulder"]
		RETURN cntry.IOCAlpha3 AS Country, ct.CompTypeName AS Discipline, ath.Sex AS Gender, MIN(att.FinishPosition) as BestPosition
		ORDER BY Country,Discipline,Gender
	'''
	
	#run the queries and put the answer in dataframes
	dtf_1 = pd.DataFrame([dict(_) for _ in conn.query(query_1)])
	dtf_2 = pd.DataFrame([dict(_) for _ in conn.query(query_2)])
	dtf_3 = pd.DataFrame([dict(_) for _ in conn.query(query_3)])
	dtf_4 = pd.DataFrame([dict(_) for _ in conn.query(query_4)])
	#dtf_5 = pd.DataFrame([dict(_) for _ in conn.query(query_5)])
	dtf_6 = pd.DataFrame([dict(_) for _ in conn.query(query_6)])
	dtf_7 = pd.DataFrame([dict(_) for _ in conn.query(query_7)])
	dtf_8 = pd.DataFrame([dict(_) for _ in conn.query(query_8)])
	#dtf_9 = pd.DataFrame([dict(_) for _ in conn.query(query_9)])
	#dtf_10 = pd.DataFrame([dict(_) for _ in conn.query(query_10)])
	#dtf_11 = pd.DataFrame([dict(_) for _ in conn.query(query_11)])
	dtf_12 = pd.DataFrame([dict(_) for _ in conn.query(query_12)])
	dtf_13 = pd.DataFrame([dict(_) for _ in conn.query(query_13)])
	dtf_14 = pd.DataFrame([dict(_) for _ in conn.query(query_14)])
	dtf_15 = pd.DataFrame([dict(_) for _ in conn.query(query_15)])
	dtf_16 = pd.DataFrame([dict(_) for _ in conn.query(query_16)])
	dtf_17 = pd.DataFrame([dict(_) for _ in conn.query(query_17)])
	dtf_18 = pd.DataFrame([dict(_) for _ in conn.query(query_18)])
	dtf_19 = pd.DataFrame([dict(_) for _ in conn.query(query_19)])
	dtf_20 = pd.DataFrame([dict(_) for _ in conn.query(query_20)])
	dtf_21 = pd.DataFrame([dict(_) for _ in conn.query(query_21)])
	dtf_22 = pd.DataFrame([dict(_) for _ in conn.query(query_22)])
	dtf_23 = pd.DataFrame([dict(_) for _ in conn.query(query_23)])
	#dtf_24 = pd.DataFrame([dict(_) for _ in conn.query(query_24)])
	dtf_25 = pd.DataFrame([dict(_) for _ in conn.query(query_25)])
	dtf_26 = pd.DataFrame([dict(_) for _ in conn.query(query_26)])
	#dtf_27 = pd.DataFrame([dict(_) for _ in conn.query(query_27)])
	dtf_28 = pd.DataFrame([dict(_) for _ in conn.query(query_28)])
	dtf_29M = pd.DataFrame([dict(_) for _ in conn.query(query_29M)])
	dtf_29F = pd.DataFrame([dict(_) for _ in conn.query(query_29F)])
	dtf_30 = pd.DataFrame([dict(_) for _ in conn.query(query_30)])
	dtf_31 = pd.DataFrame([dict(_) for _ in conn.query(query_31)])
	dtf_32 = pd.DataFrame([dict(_) for _ in conn.query(query_32)])
	dtf_33 = pd.DataFrame([dict(_) for _ in conn.query(query_33)])
	dtf_34 = pd.DataFrame([dict(_) for _ in conn.query(query_34)])
	dtf_35 = pd.DataFrame([dict(_) for _ in conn.query(query_35)])
	dtf_36 = pd.DataFrame([dict(_) for _ in conn.query(query_36)])
	dtf_37 = pd.DataFrame([dict(_) for _ in conn.query(query_37)])
	dtf_51 = pd.DataFrame([dict(_) for _ in conn.query(query_51)])
	dtf_52 = pd.DataFrame([dict(_) for _ in conn.query(query_52)])
	dtf_38 = pd.DataFrame([dict(_) for _ in conn.query(query_38)])
	dtf_39 = pd.DataFrame([dict(_) for _ in conn.query(query_39)])
	#parameters to reuse queries
	params = {"qgender": "Male", "discipline": "Lead"}
	dtf_40m_lead = pd.DataFrame([dict(_) for _ in conn.query(query_40, params)])
	params = {"qgender": "Female", "discipline": "Lead"}
	dtf_40f_lead = pd.DataFrame([dict(_) for _ in conn.query(query_40, params)])
	params = {"qgender": "Male", "discipline": "Speed"}
	dtf_40m_speed = pd.DataFrame([dict(_) for _ in conn.query(query_40, params)])
	params = {"qgender": "Female", "discipline": "Speed"}
	dtf_40f_speed = pd.DataFrame([dict(_) for _ in conn.query(query_40, params)])
	params = {"qgender": "Male", "discipline": "Boulder"}
	dtf_40m_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_40, params)])
	params = {"qgender": "Female", "discipline": "Boulder"}
	dtf_40f_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_40, params)])

	params = {"qgender": "Male", "discipline": "Lead"}
	dtf_41m_lead = pd.DataFrame([dict(_) for _ in conn.query(query_41, params)])
	params = {"qgender": "Female", "discipline": "Lead"}
	dtf_41f_lead = pd.DataFrame([dict(_) for _ in conn.query(query_41, params)])
	params = {"qgender": "Male", "discipline": "Speed"}
	dtf_41m_speed = pd.DataFrame([dict(_) for _ in conn.query(query_41, params)])
	params = {"qgender": "Female", "discipline": "Speed"}
	dtf_41f_speed = pd.DataFrame([dict(_) for _ in conn.query(query_41, params)])
	params = {"qgender": "Male", "discipline": "Boulder"}
	dtf_41m_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_41, params)])
	params = {"qgender": "Female", "discipline": "Boulder"}
	dtf_41f_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_41, params)])

	params = {"qgender": "Male", "discipline": "Lead"}
	dtf_42m_lead = pd.DataFrame([dict(_) for _ in conn.query(query_42, params)])
	params = {"qgender": "Female", "discipline": "Lead"}
	dtf_42f_lead = pd.DataFrame([dict(_) for _ in conn.query(query_42, params)])
	params = {"qgender": "Male", "discipline": "Speed"}
	dtf_42m_speed = pd.DataFrame([dict(_) for _ in conn.query(query_42, params)])
	params = {"qgender": "Female", "discipline": "Speed"}
	dtf_42f_speed = pd.DataFrame([dict(_) for _ in conn.query(query_42, params)])
	params = {"qgender": "Male", "discipline": "Boulder"}
	dtf_42m_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_42, params)])
	params = {"qgender": "Female", "discipline": "Boulder"}
	dtf_42f_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_42, params)])

	params = {"qgender": "Male", "discipline": "Lead"}
	dtf_43m_lead = pd.DataFrame([dict(_) for _ in conn.query(query_43, params)])
	params = {"qgender": "Female", "discipline": "Lead"}
	dtf_43f_lead = pd.DataFrame([dict(_) for _ in conn.query(query_43, params)])
	params = {"qgender": "Male", "discipline": "Speed"}
	dtf_43m_speed = pd.DataFrame([dict(_) for _ in conn.query(query_43, params)])
	params = {"qgender": "Female", "discipline": "Speed"}
	dtf_43f_speed = pd.DataFrame([dict(_) for _ in conn.query(query_43, params)])
	params = {"qgender": "Male", "discipline": "Boulder"}
	dtf_43m_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_43, params)])
	params = {"qgender": "Female", "discipline": "Boulder"}
	dtf_43f_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_43, params)])

	#parameters to reuse queries
	params = {"qgender": "Male", "discipline": "Lead"}
	dtf_45m_lead = pd.DataFrame([dict(_) for _ in conn.query(query_45, params)])
	params = {"qgender": "Female", "discipline": "Lead"}
	dtf_45f_lead = pd.DataFrame([dict(_) for _ in conn.query(query_45, params)])
	params = {"qgender": "Male", "discipline": "Speed"}
	dtf_45m_speed = pd.DataFrame([dict(_) for _ in conn.query(query_45, params)])
	params = {"qgender": "Female", "discipline": "Speed"}
	dtf_45f_speed = pd.DataFrame([dict(_) for _ in conn.query(query_45, params)])
	params = {"qgender": "Male", "discipline": "Boulder"}
	dtf_45m_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_45, params)])
	params = {"qgender": "Female", "discipline": "Boulder"}
	dtf_45f_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_45, params)])

	params = {"qgender": "Male", "discipline": "Lead"}
	dtf_46m_lead = pd.DataFrame([dict(_) for _ in conn.query(query_46, params)])
	params = {"qgender": "Female", "discipline": "Lead"}
	dtf_46f_lead = pd.DataFrame([dict(_) for _ in conn.query(query_46, params)])
	params = {"qgender": "Male", "discipline": "Speed"}
	dtf_46m_speed = pd.DataFrame([dict(_) for _ in conn.query(query_46, params)])
	params = {"qgender": "Female", "discipline": "Speed"}
	dtf_46f_speed = pd.DataFrame([dict(_) for _ in conn.query(query_46, params)])
	params = {"qgender": "Male", "discipline": "Boulder"}
	dtf_46m_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_46, params)])
	params = {"qgender": "Female", "discipline": "Boulder"}
	dtf_46f_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_46, params)])

	params = {"qgender": "Male", "discipline": "Lead"}
	dtf_47m_lead = pd.DataFrame([dict(_) for _ in conn.query(query_47, params)])
	params = {"qgender": "Female", "discipline": "Lead"}
	dtf_47f_lead = pd.DataFrame([dict(_) for _ in conn.query(query_47, params)])
	params = {"qgender": "Male", "discipline": "Speed"}
	dtf_47m_speed = pd.DataFrame([dict(_) for _ in conn.query(query_47, params)])
	params = {"qgender": "Female", "discipline": "Speed"}
	dtf_47f_speed = pd.DataFrame([dict(_) for _ in conn.query(query_47, params)])
	params = {"qgender": "Male", "discipline": "Boulder"}
	dtf_47m_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_47, params)])
	params = {"qgender": "Female", "discipline": "Boulder"}
	dtf_47f_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_47, params)])

	params = {"qgender": "Male", "discipline": "Lead"}
	dtf_48m_lead = pd.DataFrame([dict(_) for _ in conn.query(query_48, params)])
	params = {"qgender": "Female", "discipline": "Lead"}
	dtf_48f_lead = pd.DataFrame([dict(_) for _ in conn.query(query_48, params)])
	params = {"qgender": "Male", "discipline": "Speed"}
	dtf_48m_speed = pd.DataFrame([dict(_) for _ in conn.query(query_48, params)])
	params = {"qgender": "Female", "discipline": "Speed"}
	dtf_48f_speed = pd.DataFrame([dict(_) for _ in conn.query(query_48, params)])
	params = {"qgender": "Male", "discipline": "Boulder"}
	dtf_48m_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_48, params)])
	params = {"qgender": "Female", "discipline": "Boulder"}
	dtf_48f_boulder = pd.DataFrame([dict(_) for _ in conn.query(query_48, params)])

	dtf_50 = pd.DataFrame([dict(_) for _ in conn.query(query_50)])

	#--------------------------------------------
	# tidy up the dataframes
	#get rid of people with 0 medals
	dtf_1_trim = dtf_1[(dtf_1.NumWChampGold != 0) | (dtf_1.NumWChampSilver != 0) | (dtf_1.NumWChampBronze != 0)]
	#split into the 4 disciplines
	dtf_1_lead = dtf_1_trim[dtf_1_trim['Discipline'] == 'Lead']
	dtf_1_speed = dtf_1_trim[dtf_1_trim['Discipline'] == 'Speed']
	dtf_1_boulder = dtf_1_trim[dtf_1_trim['Discipline'] == 'Boulder']
	dtf_1_combined = dtf_1_trim[dtf_1_trim['Discipline'] == 'Combined']
	#drop the discipline column as we dont want to show it
	dtf_1_lead.drop(columns=['Discipline'], inplace=True)
	dtf_1_speed.drop(columns=['Discipline'], inplace=True)
	dtf_1_boulder.drop(columns=['Discipline'], inplace=True)
	dtf_1_combined.drop(columns=['Discipline'], inplace=True)
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_1_lead.reset_index(drop=True, inplace=True); dtf_1_lead.index = dtf_1_lead.index +1
	dtf_1_speed.reset_index(drop=True, inplace=True); dtf_1_speed.index = dtf_1_speed.index + 1
	dtf_1_boulder.reset_index(drop=True, inplace=True); dtf_1_boulder.index = dtf_1_boulder.index + 1
	dtf_1_combined.reset_index(drop=True, inplace=True); dtf_1_combined.index = dtf_1_combined.index + 1

	#get rid of people with 0 medals
	dtf_2_trim = dtf_2[(dtf_2.NumWChampGold != 0) | (dtf_2.NumWChampSilver != 0) | (dtf_2.NumWChampBronze != 0)]
	#split into the 4 disciplines
	dtf_2_lead = dtf_2_trim[dtf_2_trim['Discipline'] == 'Lead']
	dtf_2_speed = dtf_2_trim[dtf_2_trim['Discipline'] == 'Speed']
	dtf_2_boulder = dtf_2_trim[dtf_2_trim['Discipline'] == 'Boulder']
	dtf_2_combined = dtf_2_trim[dtf_2_trim['Discipline'] == 'Combined']
	#drop the discipline column as we dont want to show it
	dtf_2_lead.drop(columns=['Discipline'], inplace=True)
	dtf_2_speed.drop(columns=['Discipline'], inplace=True)
	dtf_2_boulder.drop(columns=['Discipline'], inplace=True)
	dtf_2_combined.drop(columns=['Discipline'], inplace=True)
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_2_lead.reset_index(drop=True, inplace=True); dtf_2_lead.index = dtf_2_lead.index +1
	dtf_2_speed.reset_index(drop=True, inplace=True); dtf_2_speed.index = dtf_2_speed.index + 1
	dtf_2_boulder.reset_index(drop=True, inplace=True); dtf_2_boulder.index = dtf_2_boulder.index + 1
	dtf_2_combined.reset_index(drop=True, inplace=True); dtf_2_combined.index = dtf_2_combined.index + 1

	#get rid of people with 0 medals
	dtf_3_trim = dtf_3[(dtf_3.NumWChampGold != 0) | (dtf_3.NumWChampSilver != 0) | (dtf_3.NumWChampBronze != 0)]
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_3_trim.reset_index(drop=True, inplace=True); dtf_3_trim.index = dtf_3_trim.index +1

	#get rid of people with 0 medals
	dtf_4_trim = dtf_4[(dtf_4.NumWChampGold != 0) | (dtf_4.NumWChampSilver != 0) | (dtf_4.NumWChampBronze != 0)]
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_4_trim.reset_index(drop=True, inplace=True); dtf_4_trim.index = dtf_4_trim.index +1

	dtf_6A = dtf_6.pivot(index=['Year'],columns=['Gender','Position'], values='Athlete')
	dtf_7A = dtf_7.pivot(index=['Year'],columns=['Gender','Position'], values='Athlete')
	dtf_8A = dtf_8.pivot(index=['Year'],columns=['Gender','Position'], values='Athlete')
	dtf_6B = dtf_6A.sort_index(ascending = False)
	dtf_7B = dtf_7A.sort_index(ascending = False)
	dtf_8B = dtf_8A.sort_index(ascending = False)

	dtf_14_15 = pd.merge( dtf_15, dtf_14, how="outer", on=["Country","Discipline"])
	dtf_14_15 = dtf_14_15.fillna(0)
	dtf_14_15['NumAthleteswithWChampWins'] = dtf_14_15['NumAthleteswithWChampWins'].astype(int)
	dtf_14_15.index = dtf_14_15.index + 1

	#join tables, change col from float to int, sort by wins then podiums and tidy up the index
	dtf_18_19 = pd.merge( dtf_19, dtf_18, how="outer", on=["Country"])
	dtf_18_19 = dtf_18_19.fillna(0)
	dtf_18_19['NumAthleteswithWChampWins'] = dtf_18_19['NumAthleteswithWChampWins'].astype(int)
	dtf_18_19.sort_values(by = ['NumAthleteswithWChampWins','NumAthleteswithWChampPodiums'], ascending = False, inplace = True)
	dtf_18_19.reset_index(drop=True, inplace=True);	dtf_18_19.index = dtf_18_19.index +1

	#split into the 4 disciplines
	dtf_13_lead = dtf_13[dtf_13['Discipline'] == 'Lead']
	dtf_13_speed = dtf_13[dtf_13['Discipline'] == 'Speed']
	dtf_13_boulder = dtf_13[dtf_13['Discipline'] == 'Boulder']
	dtf_13_boulderlead = dtf_13[dtf_13['Discipline'] == 'BoulderLead']
	dtf_13_combined = dtf_13[dtf_13['Discipline'] == 'Combined']
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_13_lead.reset_index(drop=True, inplace=True); dtf_13_lead.index = dtf_13_lead.index +1
	dtf_13_speed.reset_index(drop=True, inplace=True); dtf_13_speed.index = dtf_13_speed.index + 1
	dtf_13_boulder.reset_index(drop=True, inplace=True); dtf_13_boulder.index = dtf_13_boulder.index + 1
	dtf_13_combined.reset_index(drop=True, inplace=True); dtf_13_combined.index = dtf_13_combined.index + 1
	dtf_13_boulderlead.reset_index(drop=True, inplace=True); dtf_13_boulderlead.index = dtf_13_boulderlead.index + 1
	dtf_12.reset_index(drop=True, inplace=True); dtf_12.index = dtf_12.index + 1

	#split into the 4 disciplines
	dtf_14_15_lead = dtf_14_15[dtf_14_15['Discipline'] == 'Lead']
	dtf_14_15_speed = dtf_14_15[dtf_14_15['Discipline'] == 'Speed']
	dtf_14_15_boulder = dtf_14_15[dtf_14_15['Discipline'] == 'Boulder']
	dtf_14_15_combined = dtf_14_15[dtf_14_15['Discipline'] == 'Combined']
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_14_15_lead.reset_index(drop=True, inplace=True); dtf_14_15_lead.index = dtf_14_15_lead.index + 1
	dtf_14_15_speed.reset_index(drop=True, inplace=True); dtf_14_15_speed.index = dtf_14_15_speed.index + 1
	dtf_14_15_boulder.reset_index(drop=True, inplace=True); dtf_14_15_boulder.index = dtf_14_15_boulder.index +1
	dtf_14_15_combined.reset_index(drop=True, inplace=True); dtf_14_15_combined.index = dtf_14_15_combined.index + 1

	#split into the 4 disciplines
	dtf_17_lead = dtf_17[dtf_17['Discipline'] == 'Lead']
	dtf_17_speed = dtf_17[dtf_17['Discipline'] == 'Speed']
	dtf_17_boulder = dtf_17[dtf_17['Discipline'] == 'Boulder']
	dtf_17_combined = dtf_17[dtf_17['Discipline'] == 'Combined']
	dtf_17_boulderlead = dtf_17[dtf_17['Discipline'] == 'BoulderLead']
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_17_lead.reset_index(drop=True, inplace=True); dtf_17_lead.index = dtf_17_lead.index +1
	dtf_17_speed.reset_index(drop=True, inplace=True); dtf_17_speed.index = dtf_17_speed.index + 1
	dtf_17_boulder.reset_index(drop=True, inplace=True); dtf_17_boulder.index = dtf_17_boulder.index + 1
	dtf_17_combined.reset_index(drop=True, inplace=True); dtf_17_combined.index = dtf_17_combined.index + 1
	dtf_17_boulderlead.reset_index(drop=True, inplace=True); dtf_17_boulderlead.index = dtf_17_boulderlead.index + 1
	dtf_16.reset_index(drop=True, inplace=True); dtf_16.index = dtf_16.index + 1

	# do stuff for 20 to 23
	dtf_20A = dtf_20.pivot(index=["Event","Country"],columns="Discipline",values="NumTeam")
	dtf_20B = dtf_20A.fillna(0.0)
	dtf_20B['Boulder'] = dtf_20B['Boulder'].astype('Int32')
	dtf_20B['Lead'] = dtf_20B['Lead'].astype('Int32')
	dtf_20B['Speed'] = dtf_20B['Speed'].astype('Int32')
	#dtf_20C = dtf_20B
	#dtf_20C.reset_index(drop=True, inplace=True)


	dtf_23A = dtf_23.pivot(index=["Event"],columns="Discipline",values="NumCountries")
	dtf_23B = dtf_23A.fillna(0.0)
	dtf_23B['Boulder'] = dtf_23B['Boulder'].astype('Int32')
	dtf_23B['Lead'] = dtf_23B['Lead'].astype('Int32')
	dtf_23B['Speed'] = dtf_23B['Speed'].astype('Int32')
	dtf_23B['Combined'] = dtf_23B['Combined'].astype('Int32')
	dtf_23B['Boulder-Lead'] = dtf_23B['Boulder-Lead'].astype('Int32')
	dtf_24 = pd.merge(dtf_22, dtf_23B, how="inner", on=["Event"])

	dtf_26A = dtf_26.pivot(index=["Event"],columns="Discipline",values="NumAthletes")
	dtf_26B = dtf_26A.fillna(0.0)
	dtf_26B['Boulder'] = dtf_26B['Boulder'].astype('Int32')
	dtf_26B['Lead'] = dtf_26B['Lead'].astype('Int32')
	dtf_26B['Speed'] = dtf_26B['Speed'].astype('Int32')
	dtf_26B['Combined'] = dtf_26B['Combined'].astype('Int32')
	dtf_26B['Boulder-Lead'] = dtf_26B['Boulder-Lead'].astype('Int32')
	dtf_27 = pd.merge(dtf_25, dtf_26B, how="inner", on=["Event"])

	# add a colmn to current atletes to indicate they are currently competing
	dtf_29F['Status'] = 'Current'
	dtf_29M['Status'] = 'Current'

	# get dataframe sorted by NumWChamps in each Country, and then get top 3 for each Country
	dtf_30_temp = dtf_30.groupby('Country').head(3).reset_index(drop=True)
	dtf_30_temp.sort_values(by=['Country','NumWChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_30_cur = pd.merge(dtf_30_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_30_country = dtf_30_cur.loc[dtf_30_cur['Status'] == 'Current','Country']
	dtf_30_country.drop_duplicates(keep='first',inplace=True)
	l30 = dtf_30_country.values.tolist()
	#use the list to filter for countries
	dtf_30_filtered = dtf_30_cur[dtf_30_cur['Country'].isin(l30)]
	dtf_30_filtered = dtf_30_filtered.fillna('')

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_31_temp = dtf_31.groupby('Country').head(3).reset_index(drop=True)
	dtf_31_temp.sort_values(by=['Country','NumWChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_31_cur = pd.merge(dtf_31_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_31_country = dtf_31_cur.loc[dtf_31_cur['Status'] == 'Current','Country']
	dtf_31_country.drop_duplicates(keep='first',inplace=True)
	l31 = dtf_31_country.values.tolist()
	#use the list to filter for countries
	dtf_31_filtered = dtf_31_cur[dtf_31_cur['Country'].isin(l31)]
	dtf_31_filtered = dtf_31_filtered.fillna('')

	# get dataframe sorted by NumWChamps in each Country, and then get top 3 for each Country
	dtf_32_temp = dtf_32.groupby('Country').head(3).reset_index(drop=True)
	dtf_32_temp.sort_values(by=['Country','NumWChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_32_cur = pd.merge(dtf_32_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_32_country = dtf_32_cur.loc[dtf_32_cur['Status'] == 'Current','Country']
	dtf_32_country.drop_duplicates(keep='first',inplace=True)
	l32 = dtf_32_country.values.tolist()
	#use the list to filter for countries
	dtf_32_filtered = dtf_32_cur[dtf_32_cur['Country'].isin(l32)]
	dtf_32_filtered = dtf_32_filtered.fillna('')

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_33_temp = dtf_33.groupby('Country').head(3).reset_index(drop=True)
	dtf_33_temp.sort_values(by=['Country','NumWChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_33_cur = pd.merge(dtf_33_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_33_country = dtf_33_cur.loc[dtf_33_cur['Status'] == 'Current','Country']
	dtf_33_country.drop_duplicates(keep='first',inplace=True)
	l33 = dtf_33_country.values.tolist()
	#use the list to filter for countries
	dtf_33_filtered = dtf_33_cur[dtf_33_cur['Country'].isin(l33)]
	dtf_33_filtered = dtf_33_filtered.fillna('')

	# get dataframe sorted by NumWChamps in each Country, and then get top 3 for each Country
	dtf_34_temp = dtf_34.groupby('Country').head(3).reset_index(drop=True)
	dtf_34_temp.sort_values(by=['Country','NumWChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_34_cur = pd.merge(dtf_34_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_34_country = dtf_34_cur.loc[dtf_34_cur['Status'] == 'Current','Country']
	dtf_34_country.drop_duplicates(keep='first',inplace=True)
	l34 = dtf_34_country.values.tolist()
	#use the list to filter for countries
	dtf_34_filtered = dtf_34_cur[dtf_34_cur['Country'].isin(l34)]
	dtf_34_filtered = dtf_34_filtered.fillna('')

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_35_temp = dtf_35.groupby('Country').head(3).reset_index(drop=True)
	dtf_35_temp.sort_values(by=['Country','NumWChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_35_cur = pd.merge(dtf_35_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_35_country = dtf_35_cur.loc[dtf_35_cur['Status'] == 'Current','Country']
	dtf_35_country.drop_duplicates(keep='first',inplace=True)
	l35 = dtf_35_country.values.tolist()
	#use the list to filter for countries
	dtf_35_filtered = dtf_35_cur[dtf_35_cur['Country'].isin(l35)]
	dtf_35_filtered = dtf_35_filtered.fillna('')

	# get dataframe sorted by NumWChamps in each Country, and then get top 3 for each Country
	dtf_36_temp = dtf_36.groupby('Country').head(3).reset_index(drop=True)
	dtf_36_temp.sort_values(by=['Country','NumWChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_36_cur = pd.merge(dtf_36_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_36_country = dtf_36_cur.loc[dtf_36_cur['Status'] == 'Current','Country']
	dtf_36_country.drop_duplicates(keep='first',inplace=True)
	l36 = dtf_36_country.values.tolist()
	#use the list to filter for countries
	dtf_36_filtered = dtf_36_cur[dtf_36_cur['Country'].isin(l36)]
	dtf_36_filtered = dtf_36_filtered.fillna('')

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_37_temp = dtf_37.groupby('Country').head(3).reset_index(drop=True)
	dtf_37_temp.sort_values(by=['Country','NumWChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_37_cur = pd.merge(dtf_35_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_37_country = dtf_37_cur.loc[dtf_37_cur['Status'] == 'Current','Country']
	dtf_37_country.drop_duplicates(keep='first',inplace=True)
	l37 = dtf_37_country.values.tolist()
	#use the list to filter for countries
	dtf_37_filtered = dtf_37_cur[dtf_37_cur['Country'].isin(l37)]
	dtf_37_filtered = dtf_37_filtered.fillna('')

	#add one to the indexes ready for display
	dtf_30.index = dtf_30.index + 1
	dtf_31.index = dtf_31.index + 1
	dtf_32.index = dtf_32.index + 1
	dtf_33.index = dtf_33.index + 1
	dtf_34.index = dtf_34.index + 1
	dtf_35.index = dtf_35.index + 1
	dtf_36.index = dtf_36.index + 1
	dtf_37.index = dtf_37.index + 1
	dtf_51.index = dtf_51.index + 1
	dtf_52.index = dtf_52.index + 1
	dtf_38.index = dtf_38.index + 1
	dtf_39.index = dtf_39.index + 1

	#merge all the winners, sort out the columns and tidy
	frames = [dtf_40f_boulder,dtf_40m_boulder,dtf_40f_lead,dtf_40m_lead,dtf_40f_speed,dtf_40m_speed]
	dtf_40 = pd.concat(frames)
	dtf_40['MonthsObj'] = dtf_40['Age'].str.slice(0, 1)
	dtf_40['MonthsStr'] = dtf_40['MonthsObj'].astype('string')
	dtf_40['MonthsInt'] = dtf_40.MonthsStr.str.slice(1,4).astype('Int32')
	dtf_40['Years'] = dtf_40.MonthsInt.div(12).astype('Int32')
	dtf_40['Months'] = dtf_40.MonthsInt.mod(12)
	dtf_40['Winner'] = dtf_40['Athlete'].map(str) + ' Age: ' + dtf_40['Years'].map(str) + 'y '+ dtf_40['Months'].map(str) + 'm'
	dtf_40.drop(columns=['Age','MonthsObj','MonthsStr','MonthsInt','Athlete','Years','Months'], inplace=True)

	#merge all the podiums, sort out the columns and tidy
	frames = [dtf_41f_boulder,dtf_41m_boulder,dtf_41f_lead,dtf_41m_lead,dtf_41f_speed,dtf_41m_speed]
	dtf_41 = pd.concat(frames)
	dtf_41['MonthsObj'] = dtf_41['Age'].str.slice(0, 1)
	dtf_41['MonthsStr'] = dtf_41['MonthsObj'].astype('string')
	dtf_41['MonthsInt'] = dtf_41.MonthsStr.str.slice(1,4).astype('Int32')
	dtf_41['Years'] = dtf_41.MonthsInt.div(12).astype('Int32')
	dtf_41['Months'] = dtf_41.MonthsInt.mod(12)
	dtf_41['Podium'] = dtf_41['Athlete'].map(str) + ' Age: ' + dtf_41['Years'].map(str) + 'y '+ dtf_41['Months'].map(str) + 'm'
	dtf_41.drop(columns=['Age','MonthsObj','MonthsStr','MonthsInt','Athlete','Years','Months'], inplace=True)

	#merge all the finals, sort out the columns and tidy
	frames = [dtf_42f_boulder,dtf_42m_boulder,dtf_42f_lead,dtf_42m_lead,dtf_42f_speed,dtf_42m_speed]
	dtf_42 = pd.concat(frames)
	dtf_42['MonthsObj'] = dtf_42['Age'].str.slice(0, 1)
	dtf_42['MonthsStr'] = dtf_42['MonthsObj'].astype('string')
	dtf_42['MonthsInt'] = dtf_42.MonthsStr.str.slice(1,4).astype('Int32')
	dtf_42['Years'] = dtf_42.MonthsInt.div(12).astype('Int32')
	dtf_42['Months'] = dtf_42.MonthsInt.mod(12)
	dtf_42['Finalist'] = dtf_42['Athlete'].map(str) + ' Age: ' + dtf_42['Years'].map(str) + 'y '+ dtf_42['Months'].map(str) + 'm'
	dtf_42.drop(columns=['Age','MonthsObj','MonthsStr','MonthsInt','Athlete','Years','Months'], inplace=True)

	#merge all the attends, sort out the columns and tidy
	frames = [dtf_43f_boulder,dtf_43m_boulder,dtf_43f_lead,dtf_43m_lead,dtf_43f_speed,dtf_43m_speed]
	dtf_43 = pd.concat(frames)
	dtf_43['MonthsObj'] = dtf_43['Age'].str.slice(0, 1)
	dtf_43['MonthsStr'] = dtf_43['MonthsObj'].astype('string')
	dtf_43['MonthsInt'] = dtf_43.MonthsStr.str.slice(1,4).astype('Int32')
	dtf_43['Years'] = dtf_43.MonthsInt.div(12).astype('Int32')
	dtf_43['Months'] = dtf_43.MonthsInt.mod(12)
	dtf_43['Attendee'] = dtf_43['Athlete'].map(str) + ' Age: ' + dtf_43['Years'].map(str) + 'y '+ dtf_43['Months'].map(str) + 'm'
	dtf_43.drop(columns=['Age','MonthsObj','MonthsStr','MonthsInt','Athlete','Years','Months'], inplace=True)

	#merge all the yougest dataframes together
	dtf_44a = pd.merge(dtf_40, dtf_41, how="inner", on=["Discipline", "Gender"])
	dtf_44b = pd.merge(dtf_42, dtf_43, how="inner", on=["Discipline", "Gender"])
	dtf_44 = pd.merge(dtf_44a, dtf_44b, how="inner", on=["Discipline", "Gender"])

	#merge all the winners, sort out the columns and tidy
	frames = [dtf_45f_boulder,dtf_45m_boulder,dtf_45f_lead,dtf_45m_lead,dtf_45f_speed,dtf_45m_speed]
	dtf_45 = pd.concat(frames)
	dtf_45['MonthsObj'] = dtf_45['Age'].str.slice(0, 1)
	dtf_45['MonthsStr'] = dtf_45['MonthsObj'].astype('string')
	dtf_45['MonthsInt'] = dtf_45.MonthsStr.str.slice(1,4).astype('Int32')
	dtf_45['Years'] = dtf_45.MonthsInt.div(12).astype('Int32')
	dtf_45['Months'] = dtf_45.MonthsInt.mod(12)
	dtf_45['Winner'] = dtf_45['Athlete'].map(str) + ' Age: ' + dtf_45['Years'].map(str) + 'y '+ dtf_45['Months'].map(str) + 'm'
	dtf_45.drop(columns=['Age','MonthsObj','MonthsStr','MonthsInt','Athlete','Years','Months'], inplace=True)

	#merge all the podiums, sort out the columns and tidy
	frames = [dtf_46f_boulder,dtf_46m_boulder,dtf_46f_lead,dtf_46m_lead,dtf_46f_speed,dtf_46m_speed]
	dtf_46 = pd.concat(frames)
	dtf_46['MonthsObj'] = dtf_46['Age'].str.slice(0, 1)
	dtf_46['MonthsStr'] = dtf_46['MonthsObj'].astype('string')
	dtf_46['MonthsInt'] = dtf_46.MonthsStr.str.slice(1,4).astype('Int32')
	dtf_46['Years'] = dtf_46.MonthsInt.div(12).astype('Int32')
	dtf_46['Months'] = dtf_46.MonthsInt.mod(12)
	dtf_46['Podium'] = dtf_46['Athlete'].map(str) + ' Age: ' + dtf_46['Years'].map(str) + 'y '+ dtf_46['Months'].map(str) + 'm'
	dtf_46.drop(columns=['Age','MonthsObj','MonthsStr','MonthsInt','Athlete','Years','Months'], inplace=True)

	#merge all the finals, sort out the columns and tidy
	frames = [dtf_47f_boulder,dtf_47m_boulder,dtf_47f_lead,dtf_47m_lead,dtf_47f_speed,dtf_47m_speed]
	dtf_47 = pd.concat(frames)
	dtf_47['MonthsObj'] = dtf_47['Age'].str.slice(0, 1)
	dtf_47['MonthsStr'] = dtf_47['MonthsObj'].astype('string')
	dtf_47['MonthsInt'] = dtf_47.MonthsStr.str.slice(1,4).astype('Int32')
	dtf_47['Years'] = dtf_47.MonthsInt.div(12).astype('Int32')
	dtf_47['Months'] = dtf_47.MonthsInt.mod(12)
	dtf_47['Finalist'] = dtf_47['Athlete'].map(str) + ' Age: ' + dtf_47['Years'].map(str) + 'y '+ dtf_47['Months'].map(str) + 'm'
	dtf_47.drop(columns=['Age','MonthsObj','MonthsStr','MonthsInt','Athlete','Years','Months'], inplace=True)

	#merge all the attends, sort out the columns and tidy
	frames = [dtf_48f_boulder,dtf_48m_boulder,dtf_48f_lead,dtf_48m_lead,dtf_48f_speed,dtf_48m_speed]
	dtf_48 = pd.concat(frames)
	dtf_48['MonthsObj'] = dtf_48['Age'].str.slice(0, 1)
	dtf_48['MonthsStr'] = dtf_48['MonthsObj'].astype('string')
	dtf_48['MonthsInt'] = dtf_48.MonthsStr.str.slice(1,4).astype('Int32')
	dtf_48['Years'] = dtf_48.MonthsInt.div(12).astype('Int32')
	dtf_48['Months'] = dtf_48.MonthsInt.mod(12)
	dtf_48['Attendee'] = dtf_48['Athlete'].map(str) + ' Age: ' + dtf_48['Years'].map(str) + 'y '+ dtf_48['Months'].map(str) + 'm'
	dtf_48.drop(columns=['Age','MonthsObj','MonthsStr','MonthsInt','Athlete','Years','Months'], inplace=True)

	#merge all the oldest dataframes together
	dtf_49a = pd.merge(dtf_45, dtf_46, how="inner", on=["Discipline", "Gender"])
	dtf_49b = pd.merge(dtf_47, dtf_48, how="inner", on=["Discipline", "Gender"])
	dtf_49 = pd.merge(dtf_49a, dtf_49b, how="inner", on=["Discipline", "Gender"])

	dtf_50A = dtf_50.pivot(index=["Country","Gender"],columns="Discipline",values="BestPosition")
	dtf_50B = dtf_50A.fillna(0.0)
	dtf_50B['Boulder'] = dtf_50B['Boulder'].astype('Int32')
	dtf_50B['Lead'] = dtf_50B['Lead'].astype('Int32')
	dtf_50B['Speed'] = dtf_50B['Speed'].astype('Int32')

	#create dataframes for 2025 WChamps
	#data = [["Switzerland","WChamp 2023 All","2023-08-01","2023-08-12","Bern",8]]
	#dtf_28a = dtf_28.append(pd.DataFrame(data,columns=['Country','EventName','Start','Finish','Venue','NumComps']), ignore_index = True)

	#data = [["WChamp 2023 All",54,nan,nan,nan,nan]]
	#dtf_24a = dtf_24.append(pd.DataFrame(data,columns=['Event','NumCountries','Boulder','Combined','Lead','Speed']), ignore_index = True)

	#data = [["WChamp 2023 All",428,252,nan,261,143]]
	#dtf_27a = dtf_27.append(pd.DataFrame(data,columns=['Event','NumAthletes','Boulder','Combined','Lead','Speed']), ignore_index = True)

	myslice = ['WChampEvent','Country']

	mystyles = [dict(selector="", props=[('border','2px solid black')])]


	#print (dtf_2_boulder)

	#produce csv files for publishing

	#title="Event and Country Statistics"
	dtf_28.to_csv('list_of_world_championships.csv', header=True, index=True)
	dtf_24.to_csv('Countries_competing_at_World_Championships.csv', header=True, index=True)
	dtf_27.to_csv('Athletes_competing_at_World_Championships.csv', header=True, index=True)
	dtf_21.to_csv('20_Largest_Total_Team_size_at_World_Championships.csv', header=True, index=True)
	#dp.Group(
	#dtf_20B.to_csv('20 Largest Teams per Discipline at World Championships', header=True, index=False)
	
	# --------------------------

	#title="World Chamionship Competition and Athlete Participation Statistics"
	dtf_30.to_csv('Number_of_Boulder_World_Champs_attended_female.csv', header=True, index=True)
	dtf_31.to_csv('Number_of_Boulder_World_Champs_attended_male.csv', header=True, index=True)
	dtf_32.to_csv('Number_of_Lead_World_Champs_attended_female.csv', header=True, index=True)
	dtf_33.to_csv('Number_of_Lead_World_Champs_attended_male.csv', header=True, index=True)
	dtf_34.to_csv('Number_of_Speed_World_Champs_attended_female.csv', header=True, index=True)
	dtf_35.to_csv('Number_of_Speed_World_Champs_attended_male.csv', header=True, index=True)
	dtf_36.to_csv('Number_of_Combined_World_Champs_attended_female.csv', header=True, index=True)
	dtf_37.to_csv('Number_of_Combined_World_Champs_attended_male.csv', header=True, index=True)
	dtf_51.to_csv('Number_of_BoulderLead_World_Champs_attended_female.csv', header=True, index=True)
	dtf_52.to_csv('Number_of_BoulderLead_World_Champs_attended_male.csv', header=True, index=True)
	dtf_38.to_csv('Number_of_World_Champs_all_disciplines_attended_female.csv', header=True, index=True)
	dtf_39.to_csv('Number_of_World_Champs_all_disciplines_attended_male.csv', header=True, index=True)

	# --------------------------

	#title="Country Results World Champs"

	dtf_13_boulder.to_csv('World_Championships_Medal_Table_for_Boulder.csv', header=True, index=True)
	dtf_13_lead.to_csv('World_Championships_Medal_Table_for_Lead.csv', header=True, index=True)
	dtf_13_speed.to_csv('World_Championships_Medal_Table_for_Speed.csv', header=True, index=True)
	dtf_13_combined.to_csv('World_Championships_Medal_Table_for_Combined.csv', header=True, index=True)
	dtf_13_boulderlead.to_csv('World_Championships_Medal_Table_for_BoulderLead.csv', header=True, index=True)
	dtf_12.to_csv('World_Championships_Medal_Table_for_All_disciplines.csv', header=True, index=True)
	dtf_14_15_boulder.to_csv('Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_Boulder.csv', header=True, index=True)
	dtf_14_15_lead.to_csv('Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_Lead.csv', header=True, index=True)
	dtf_14_15_speed.to_csv('Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_Speed.csv', header=True, index=True)
	dtf_14_15_combined.to_csv('Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_Combined.csv', header=True, index=True)
	dtf_18_19.to_csv('Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_all_disciplines.csv', header=True, index=True)
	dtf_50B.to_csv('Country_best_finishes_by_gender_and_discipline.csv', header=True, index=True)

	# --------------------------

	#title="Country Results World Champs per Year"

	dtf_16.to_csv('World_Championships_Medal_Table_for_All_disciplines_per_World_Championship.csv', header=True, index=True)
	dtf_17_boulder.to_csv('World_Championships_Medal_Table_for_Boulder.csv', header=True, index=True)
	dtf_17_lead.to_csv('World_Championships_Medal_Table_for_Lead.csv', header=True, index=True)
	dtf_17_speed.to_csv('World_Championships_Medal_Table_for_Speed.csv', header=True, index=True)
	dtf_17_combined.to_csv('World_Championships_Medal_Table_for_Combined.csv', header=True, index=True)
	dtf_17_boulderlead.to_csv('World_Championships_Medal_Table_for_BoulderLead.csv', header=True, index=True)

	# --------------------------

	#title="Youngest and Oldest Stats"
	# dp.Text("Youngest"),
	# dp.Table(dtf_44.style.hide_index().set_table_styles(mystyles), caption=updateAllCaption),
	# dp.Text("Oldest"),
	# dp.Table(dtf_49.style.hide_index().set_table_styles(mystyles), caption=updateAllCaption),
    # columns=1,

	# --------------------------

	#title="Athlete Results"

	dtf_1_boulder.to_csv('World_Championship_Boulder_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_boulder.to_csv('World_Championship_Boulder_wins_and_podiums_female.csv', header=True, index=True)
	dtf_1_lead.to_csv('World_Championship_Lead_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_lead.to_csv('World_Championship_Lead_wins_and_podiums_female.csv', header=True, index=True)
	dtf_1_speed.to_csv('World_Championship_Speed_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_speed.to_csv('World_Championship_Speed_wins_and_podiums_female.csv', header=True, index=True)
	dtf_1_combined.to_csv('World_Championship_Combined_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_combined.to_csv('World_Championship_Combined_wins_and_podiums_female.csv', header=True, index=True)
	dtf_3_trim.to_csv('World_Championship_all_disciplines_wins_and_podiums_male.csv', header=True, index=True)
	dtf_4_trim.to_csv('World_Championship_all_disciplines_wins_and_podiums_female.csv', header=True, index=True)
	dtf_6B.to_csv('World_Championship_Boulder_podium_list_male_and_female.csv', header=True, index=True)
	dtf_7B.to_csv('World_Championship_Lead_podium_list_male_and_female.csv', header=True, index=True)
	dtf_8B.to_csv('World_Championship_Speed_podium_list_male_and_female.csv', header=True, index=True)


	# --------------------------


      	#path='WChampCountryResults.html'
        # name='IFSC World Championship Statistics',
	
	#
	# how to close the connection to the database
	#
	conn.close()
	print("thanks for all the fish")




