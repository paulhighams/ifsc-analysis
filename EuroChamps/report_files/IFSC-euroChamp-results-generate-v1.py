#from neo4j import __version__ as neo4j_version
#print(neo4j_version)

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
	
	# eurohamp win and podiums by athlete, by discipline for Male
	query_1 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ct.CompTypeName as Discipline, ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as NumChampGold, Count(att.FinTwo) as NumChampSilver, Count(att.FinThree) as NumChampBronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY NumChampGold DESC, NumChampSilver DESC, NumChampBronze DESC
	'''

	# euroChamp win and podiums by athlete, by discipline for Female
	query_2 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ct.CompTypeName as Discipline, ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as NumChampGold, Count(att.FinTwo) as NumChampSilver, Count(att.FinThree) as NumChampBronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY NumChampGold DESC, NumChampSilver DESC, NumChampBronze DESC
	'''
	# euroChamp win and podiums by athlete, aa discipline for Male
	query_3 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as NumChampGold, Count(att.FinTwo) as NumChampSilver, Count(att.FinThree) as NumChampBronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY NumChampGold DESC, NumChampSilver DESC, NumChampBronze DESC
	'''

	# euroChamp win and podiums by athlete, aa discipline for Female
	query_4 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as NumChampGold, Count(att.FinTwo) as NumChampSilver, Count(att.FinThree) as NumChampBronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY NumChampGold DESC, NumChampSilver DESC, NumChampBronze DESC
	'''

	#Number of athletes competing in a year at euro champs
	query_8 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[oc:OCCURS_IN]->(yr:Year),
	(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	RETURN yr.YearName AS Year, count(DISTINCT ath.PersonName) AS NumAthletes
	ORDER BY Year
	'''

	#Number of countries competing in a year at euro champs
	query_9 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[oc:OCCURS_IN]->(yr:Year),
	(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	RETURN yr.YearName AS Year, count(DISTINCT cntry.CountryName) AS NumCountries
	ORDER BY Year
	'''

	#Country Medal Table euro Championships - medals by gold, silver, bronze for each discipline
	query_13 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4
	RETURN cntry.CountryName as Country, ct.CompTypeName as Discipline, COUNT(att.FinOne) as Gold, COUNT(att.FinTwo) AS Silver, COUNT(att.FinThree) AS Bronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY Gold DESC, Silver DESC, Bronze DESC
	'''

	#Number of athletes who have Podiumed at euro Championships per country per discipline
	query_14 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[p:PODIUM]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, ct.CompTypeName AS Discipline, count(DISTINCT ath.PersonName) as NumAthleteswithChampPodiums
	ORDER BY NumAthleteswithChampPodiums DESC
	'''
	
	#Number of athletes who have won at euro Championships per country per discipline
	query_15 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[w:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, ct.CompTypeName AS Discipline, count(DISTINCT ath.PersonName) as NumAthleteswithChampWins
	ORDER BY NumAthleteswithChampWins DESC
	'''

	#Number of athletes who have Podiumed at euro Championships per country all disciplines
	query_18 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[p:PODIUM]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, count(DISTINCT ath.PersonName) as NumAthleteswithChampPodiums
	ORDER BY NumAthleteswithChampPodiums DESC
	'''
	
	#Number of athletes who have won at euro Championships per country all disciplines
	query_19 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[w:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, count(DISTINCT ath.PersonName) as NumAthleteswithChampWins
	ORDER BY NumAthleteswithChampWins DESC
	'''
	
	#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_20 = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_21 = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

	#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_22 = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_23 = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

	#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_24 = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_25 = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

	#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_26 = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_27 = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

	#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_26BL = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

#Athlete Medal Table World Championships (one discipline) - by comp medals by gold, silver, bronze
	query_27BL = '''MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:1}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:2}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	UNION ALL
	MATCH (cntry:Country)<-[REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS {FinishPosition:3}]->(cmp:Competition)<-[CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
	MATCH (ev:Event)-[OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
	RETURN cmp.CompetitionName AS Competition,yr.YearName AS Year, ath.PersonName+' ('+cntry.IOCAlpha3+')' AS Athlete, att.FinishPosition AS FinishPosition
	ORDER BY Year DESC, FinishPosition
	'''

	#list of the euro championships, by country and venue
	query_28 = '''MATCH (ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'European Championship'}),
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
	#Number of euroChamps attended by an Athlete (sex) in a single discipline
	query_30 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_31 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_32 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_33 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_34 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_35 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_36 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_37 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Combined"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_36BL = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_37BL = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder-Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''

	# as above but all disciplines
	query_38 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	query_39 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "European Championship"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumChamps
		ORDER BY NumChamps DESC
	'''
	#query_40 = '''
	#'''
	#query_41 = '''
	#'''
	
	#run the queries and put the answer in dataframes
	dtf_1 = pd.DataFrame([dict(_) for _ in conn.query(query_1)])
	dtf_2 = pd.DataFrame([dict(_) for _ in conn.query(query_2)])
	dtf_3 = pd.DataFrame([dict(_) for _ in conn.query(query_3)])
	dtf_4 = pd.DataFrame([dict(_) for _ in conn.query(query_4)])
	dtf_8 = pd.DataFrame([dict(_) for _ in conn.query(query_8)])
	dtf_9 = pd.DataFrame([dict(_) for _ in conn.query(query_9)])
	dtf_13 = pd.DataFrame([dict(_) for _ in conn.query(query_13)])
	dtf_14 = pd.DataFrame([dict(_) for _ in conn.query(query_14)])
	dtf_15 = pd.DataFrame([dict(_) for _ in conn.query(query_15)])
	dtf_18 = pd.DataFrame([dict(_) for _ in conn.query(query_18)])
	dtf_19 = pd.DataFrame([dict(_) for _ in conn.query(query_19)])
	dtf_20 = pd.DataFrame([dict(_) for _ in conn.query(query_20)])
	dtf_21 = pd.DataFrame([dict(_) for _ in conn.query(query_21)])
	dtf_22 = pd.DataFrame([dict(_) for _ in conn.query(query_22)])
	dtf_23 = pd.DataFrame([dict(_) for _ in conn.query(query_23)])
	dtf_24 = pd.DataFrame([dict(_) for _ in conn.query(query_24)])
	dtf_25 = pd.DataFrame([dict(_) for _ in conn.query(query_25)])
	dtf_26 = pd.DataFrame([dict(_) for _ in conn.query(query_26)])
	dtf_27 = pd.DataFrame([dict(_) for _ in conn.query(query_27)])
	dtf_26BL = pd.DataFrame([dict(_) for _ in conn.query(query_26BL)])
	dtf_27BL = pd.DataFrame([dict(_) for _ in conn.query(query_27BL)])
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
	dtf_36BL = pd.DataFrame([dict(_) for _ in conn.query(query_36BL)])
	dtf_37BL = pd.DataFrame([dict(_) for _ in conn.query(query_37BL)])
	dtf_38 = pd.DataFrame([dict(_) for _ in conn.query(query_38)])
	dtf_39 = pd.DataFrame([dict(_) for _ in conn.query(query_39)])
	#dtf_40 = pd.DataFrame([dict(_) for _ in conn.query(query_40)])
	#dtf_41 = pd.DataFrame([dict(_) for _ in conn.query(query_41)])

	#get rid of people with 0 medals
	dtf_1_trim = dtf_1[(dtf_1.NumChampGold != 0) | (dtf_1.NumChampSilver != 0) | (dtf_1.NumChampBronze != 0)]
	#split into the 4 disciplines
	dtf_1_lead = dtf_1_trim[dtf_1_trim['Discipline'] == 'Lead']
	dtf_1_speed = dtf_1_trim[dtf_1_trim['Discipline'] == 'Speed']
	dtf_1_boulder = dtf_1_trim[dtf_1_trim['Discipline'] == 'Boulder']
	dtf_1_combined = dtf_1_trim[dtf_1_trim['Discipline'] == 'Combined']
	dtf_1_boulderlead = dtf_1_trim[dtf_1_trim['Discipline'] == 'Boulder-Lead']
	print(dtf_1_boulderlead)
	#drop the discipline column as we dont want to show it
	dtf_1_lead.drop(columns=['Discipline'], inplace=True)
	dtf_1_speed.drop(columns=['Discipline'], inplace=True)
	dtf_1_boulder.drop(columns=['Discipline'], inplace=True)
	dtf_1_combined.drop(columns=['Discipline'], inplace=True)
	dtf_1_boulderlead.drop(columns=['Discipline'], inplace=True)
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_1_lead.reset_index(drop=True, inplace=True); dtf_1_lead.index = dtf_1_lead.index +1
	dtf_1_speed.reset_index(drop=True, inplace=True); dtf_1_speed.index = dtf_1_speed.index + 1
	dtf_1_boulder.reset_index(drop=True, inplace=True); dtf_1_boulder.index = dtf_1_boulder.index + 1
	dtf_1_combined.reset_index(drop=True, inplace=True); dtf_1_combined.index = dtf_1_combined.index + 1
	dtf_1_boulderlead.reset_index(drop=True, inplace=True); dtf_1_boulderlead.index = dtf_1_boulderlead.index + 1

	#get rid of people with 0 medals
	dtf_2_trim = dtf_2[(dtf_2.NumChampGold != 0) | (dtf_2.NumChampSilver != 0) | (dtf_2.NumChampBronze != 0)]
	#split into the 4 disciplines
	dtf_2_lead = dtf_2_trim[dtf_2_trim['Discipline'] == 'Lead']
	dtf_2_speed = dtf_2_trim[dtf_2_trim['Discipline'] == 'Speed']
	dtf_2_boulder = dtf_2_trim[dtf_2_trim['Discipline'] == 'Boulder']
	dtf_2_combined = dtf_2_trim[dtf_2_trim['Discipline'] == 'Combined']
	dtf_2_boulderlead = dtf_2_trim[dtf_2_trim['Discipline'] == 'Boulder-Lead']
	#drop the discipline column as we dont want to show it
	dtf_2_lead.drop(columns=['Discipline'], inplace=True)
	dtf_2_speed.drop(columns=['Discipline'], inplace=True)
	dtf_2_boulder.drop(columns=['Discipline'], inplace=True)
	dtf_2_combined.drop(columns=['Discipline'], inplace=True)
	dtf_2_boulderlead.drop(columns=['Discipline'], inplace=True)
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_2_lead.reset_index(drop=True, inplace=True); dtf_2_lead.index = dtf_2_lead.index +1
	dtf_2_speed.reset_index(drop=True, inplace=True); dtf_2_speed.index = dtf_2_speed.index + 1
	dtf_2_boulder.reset_index(drop=True, inplace=True); dtf_2_boulder.index = dtf_2_boulder.index + 1
	dtf_2_combined.reset_index(drop=True, inplace=True); dtf_2_combined.index = dtf_2_combined.index + 1
	dtf_2_boulderlead.reset_index(drop=True, inplace=True); dtf_2_boulderlead.index = dtf_2_boulderlead.index + 1

	#get rid of people with 0 medals
	dtf_3_trim = dtf_3[(dtf_3.NumChampGold != 0) | (dtf_3.NumChampSilver != 0) | (dtf_3.NumChampBronze != 0)]
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_3_trim.reset_index(drop=True, inplace=True); dtf_3_trim.index = dtf_3_trim.index +1

	#get rid of people with 0 medals
	dtf_4_trim = dtf_4[(dtf_4.NumChampGold != 0) | (dtf_4.NumChampSilver != 0) | (dtf_4.NumChampBronze != 0)]
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_4_trim.reset_index(drop=True, inplace=True); dtf_4_trim.index = dtf_4_trim.index +1


	dtf_14_15 = pd.merge( dtf_15, dtf_14, how="outer", on=["Country","Discipline"])
	dtf_14_15 = dtf_14_15.fillna(0)
	dtf_14_15['NumAthleteswithChampWins'] = dtf_14_15['NumAthleteswithChampWins'].astype(int)
	dtf_14_15.index = dtf_14_15.index + 1

	#join tables, change col from float to int, sort by wins then podiums and tidy up the index
	dtf_18_19 = pd.merge( dtf_19, dtf_18, how="outer", on=["Country"])
	dtf_18_19 = dtf_18_19.fillna(0)
	dtf_18_19['NumAthleteswithChampWins'] = dtf_18_19['NumAthleteswithChampWins'].astype(int)
	dtf_18_19.sort_values(by = ['NumAthleteswithChampWins','NumAthleteswithChampPodiums'], ascending = False, inplace = True)
	dtf_18_19.reset_index(drop=True, inplace=True);	dtf_18_19.index = dtf_18_19.index +1

	#split into the 4 disciplines
	dtf_13_lead = dtf_13[dtf_13['Discipline'] == 'Lead']
	dtf_13_speed = dtf_13[dtf_13['Discipline'] == 'Speed']
	dtf_13_boulder = dtf_13[dtf_13['Discipline'] == 'Boulder']
	dtf_13_combined = dtf_13[dtf_13['Discipline'] == 'Combined']
	dtf_13_boulderlead = dtf_13[dtf_13['Discipline'] == 'Boulder-Lead']
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_13_lead.reset_index(drop=True, inplace=True); dtf_13_lead.index = dtf_13_lead.index +1
	dtf_13_speed.reset_index(drop=True, inplace=True); dtf_13_speed.index = dtf_13_speed.index + 1
	dtf_13_boulder.reset_index(drop=True, inplace=True); dtf_13_boulder.index = dtf_13_boulder.index + 1
	dtf_13_combined.reset_index(drop=True, inplace=True); dtf_13_combined.index = dtf_13_combined.index + 1
	dtf_13_boulderlead.reset_index(drop=True, inplace=True); dtf_13_boulderlead.index = dtf_13_boulderlead.index + 1

	#split into the 4 disciplines
	dtf_14_15_lead = dtf_14_15[dtf_14_15['Discipline'] == 'Lead']
	dtf_14_15_speed = dtf_14_15[dtf_14_15['Discipline'] == 'Speed']
	dtf_14_15_boulder = dtf_14_15[dtf_14_15['Discipline'] == 'Boulder']
	dtf_14_15_combined = dtf_14_15[dtf_14_15['Discipline'] == 'Combined']
	dtf_14_15_boulderlead = dtf_14_15[dtf_14_15['Discipline'] == 'Boulder-Lead']
	# reset the index and then add 1, so the index starts at 1 and not zero
	dtf_14_15_lead.reset_index(drop=True, inplace=True); dtf_14_15_lead.index = dtf_14_15_lead.index + 1
	dtf_14_15_speed.reset_index(drop=True, inplace=True); dtf_14_15_speed.index = dtf_14_15_speed.index + 1
	dtf_14_15_boulder.reset_index(drop=True, inplace=True); dtf_14_15_boulder.index = dtf_14_15_boulder.index +1
	dtf_14_15_combined.reset_index(drop=True, inplace=True); dtf_14_15_combined.index = dtf_14_15_combined.index + 1
	dtf_14_15_boulderlead.reset_index(drop=True, inplace=True); dtf_14_15_boulderlead.index = dtf_14_15_boulderlead.index + 1
	
	dtf_20p = dtf_20.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	#dtf_21p = dtf_21.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_20p.sort_values(by=['Year'], ascending = [False], inplace=True)
	#dtf_21p.sort_values(by=['Year'], ascending = [False], inplace=True)
	dtf_21.sort_values(by=['Year','FinishPosition'], ascending = [False,True], inplace=True)
	#print (dtf_21p)
	dtf_22p = dtf_22.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_23p = dtf_23.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_22p.sort_values(by=['Year'], ascending = [False], inplace=True)
	dtf_23p.sort_values(by=['Year'], ascending = [False], inplace=True)
	dtf_24p = dtf_24.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_25p = dtf_25.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_24p.sort_values(by=['Year'], ascending = [False], inplace=True)
	dtf_25p.sort_values(by=['Year'], ascending = [False], inplace=True)
	dtf_26p = dtf_26.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_27p = dtf_27.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_26p.sort_values(by=['Year'], ascending = [False], inplace=True)
	dtf_27p.sort_values(by=['Year'], ascending = [False], inplace=True)
	dtf_26BLp = dtf_26BL.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_27BLp = dtf_27BL.pivot(index=['Competition','Year'], columns='FinishPosition', values='Athlete')
	dtf_26BLp.sort_values(by=['Year'], ascending = [False], inplace=True)
	dtf_27BLp.sort_values(by=['Year'], ascending = [False], inplace=True)
	
	# add a colmn to current atletes to indicate they are currently competing
	dtf_29F['Status'] = 'Current'
	dtf_29M['Status'] = 'Current'

	# get dataframe sorted by NumWChamps in each Country, and then get top 3 for each Country
	dtf_30_temp = dtf_30.groupby('Country').head(3).reset_index(drop=True)
	dtf_30_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
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
	dtf_31_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
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
	dtf_32_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
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
	dtf_33_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
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
	dtf_34_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
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
	dtf_35_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
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
	dtf_36_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
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
	dtf_37_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_37_cur = pd.merge(dtf_37_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_37_country = dtf_37_cur.loc[dtf_37_cur['Status'] == 'Current','Country']
	dtf_37_country.drop_duplicates(keep='first',inplace=True)
	l37 = dtf_37_country.values.tolist()
	#use the list to filter for countries
	dtf_37_filtered = dtf_37_cur[dtf_37_cur['Country'].isin(l37)]
	dtf_37_filtered = dtf_37_filtered.fillna('')

	# get dataframe sorted by NumWChamps in each Country, and then get top 3 for each Country
	dtf_36BL_temp = dtf_36BL.groupby('Country').head(3).reset_index(drop=True)
	dtf_36BL_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_36BL_cur = pd.merge(dtf_36BL_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_36BL_country = dtf_36BL_cur.loc[dtf_36BL_cur['Status'] == 'Current','Country']
	dtf_36BL_country.drop_duplicates(keep='first',inplace=True)
	l36BL = dtf_36BL_country.values.tolist()
	#use the list to filter for countries
	dtf_36BL_filtered = dtf_36BL_cur[dtf_36BL_cur['Country'].isin(l36BL)]
	dtf_36BL_filtered = dtf_36BL_filtered.fillna('')

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_37BL_temp = dtf_37BL.groupby('Country').head(3).reset_index(drop=True)
	dtf_37BL_temp.sort_values(by=['Country','NumChamps'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_37BL_cur = pd.merge(dtf_37BL_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_37BL_country = dtf_37BL_cur.loc[dtf_37BL_cur['Status'] == 'Current','Country']
	dtf_37BL_country.drop_duplicates(keep='first',inplace=True)
	l37BL = dtf_37BL_country.values.tolist()
	#use the list to filter for countries
	dtf_37BL_filtered = dtf_37BL_cur[dtf_37BL_cur['Country'].isin(l37BL)]
	dtf_37BL_filtered = dtf_37BL_filtered.fillna('')

	#add one to the indexes ready for display
	dtf_30.index = dtf_30.index + 1
	dtf_31.index = dtf_31.index + 1
	dtf_32.index = dtf_32.index + 1
	dtf_33.index = dtf_33.index + 1
	dtf_34.index = dtf_34.index + 1
	dtf_35.index = dtf_35.index + 1
	dtf_36.index = dtf_36.index + 1
	dtf_37.index = dtf_37.index + 1
	dtf_36BL.index = dtf_36BL.index + 1
	dtf_37BL.index = dtf_37BL.index + 1
	dtf_38.index = dtf_38.index + 1
	dtf_39.index = dtf_39.index + 1

	#produce csv files
	#name='IFSC European Championship Statistics',

	#title="Event and Country Statistics"
	dtf_28.to_csv('List_of_European_Championships.csv', header=True, index=True)
	dtf_9.to_csv('Num_of_Countries_at_European_Championships.csv', header=True, index=True)
	dtf_8.to_csv('Num_of_Athletes_at_European_Championships.csv', header=True, index=True)

	#title="European Championship Competition and Athlete Participation Statistics"				
	dtf_30.to_csv('Number_of_Boulder_European_Champs_attended_female_Top_20.csv', header=True, index=True)
	dtf_31.to_csv('Number_of_Boulder_European_Champs_attended_male_Top_20.csv', header=True, index=True)
	dtf_32.to_csv('Number_of_Lead_European_Champs_attended_female_Top_20.csv', header=True, index=True)
	dtf_33.to_csv('Number_of_Lead_European_Champs_attended_male_Top_20.csv', header=True, index=True)
	dtf_34.to_csv('Number_of_Speed_European_Champs_attended_female_Top_20', header=True, index=True)
	dtf_35.to_csv('Number_of_Speed_European_Champs_attended_male_Top_20.csv', header=True, index=True)
	dtf_36.to_csv('Number_of_combined_European_Champs_attended_female_Top_20.csv', header=True, index=True)
	dtf_37.to_csv('Number_of_combined_European_Champs_attended_male_Top_20.csv', header=True, index=True)
	dtf_36BL.to_csv('Number_of_Boulder_Lead_European_Champs_attended_female_Top_20.csv', header=True, index=True)
	dtf_37BL.to_csv('Number_of_Boulder_Lead_European_Champs_attended_male_Top_20.csv', header=True, index=True)
	dtf_38.to_csv('Number_of_all_disciplines_European_Champs_attended_female_Top_20.csv', header=True, index=True)
	dtf_39.to_csv('Number_of_all_disciplines_European_Champs_attended_male_Top_20.csv', header=True, index=True)
	#title="Country Results European Champs"
	dtf_13_boulder.to_csv('European_Championships_Medal_Table_for_Boulder.csv', header=True, index=True)
	dtf_13_lead.to_csv('European_Championships_Medal_Table_for_Lead.csv', header=True, index=True)
	dtf_13_speed.to_csv('European_Championships_Medal_Table_for_Speed.csv', header=True, index=True)
	dtf_13_combined.to_csv('European_Championships_Medal_Table_for_combined.csv', header=True, index=True)
	dtf_13_boulderlead.to_csv('European_Championships_Medal_Table_for_Boulder_Lead.csv', header=True, index=True)
	dtf_14_15_boulder.to_csv('Number_of_athletes_per_Country_with_European_Championship_wins_and_podiums_for_Boulder.csv', header=True, index=True)
	dtf_14_15_lead.to_csv('Number_of_athletes_per_Country_with_European_Championship_wins_and_podiums_for_Lead.csv', header=True, index=True)
	dtf_14_15_speed.to_csv('Number_of_athletes_per_Country_with_European_Championship_wins_and_podiums_for_Speed.csv', header=True, index=True)
	dtf_14_15_combined.to_csv('Number_of_athletes_per_Country_with_European_Championship_wins_and_podiums_for_combined.csv', header=True, index=True)
	dtf_14_15_boulderlead.to_csv('Number_of_athletes_per_Country_with_European_Championship_wins_and_podiums_for_Boulder_Lead.csv', header=True, index=True)
	dtf_18_19.to_csv('Number_of_athletes_per_Country_with_European_Championship_wins_and_podiums_for_all_disciplines.csv', header=True, index=True)
	#title="Athlete Results"
	dtf_1_boulder.to_csv('European_Championship_Boulder_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_boulder.to_csv('European_Championship_Boulder_wins_and_podiums_female.csv', header=True, index=True)
	dtf_1_lead.to_csv('European_Championship_Lead_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_lead.to_csv('European_Championship_Lead_wins_and_podiums_female.csv', header=True, index=True)
	dtf_1_speed.to_csv('European_Championship_Speed_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_speed.to_csv('European_Championship_Speed_wins_and_podiums_female.csv', header=True, index=True)
	dtf_1_combined.to_csv('European_Championship_combined_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_combined.to_csv('European_Championship_combined_wins_and_podiums_female.csv', header=True, index=True)
	dtf_1_boulderlead.to_csv('European_Championship_Boulder_Lead_wins_and_podiums_male.csv', header=True, index=True)
	dtf_2_boulderlead.to_csv('European_Championship_Boulder_Lead_wins_and_podiums_female.csv', header=True, index=True)
	dtf_3_trim.to_csv('European_Championship_all_disciplines_wins_and_podiums_male.csv', header=True, index=True)
	dtf_4_trim.to_csv('European_Championship_all_disciplines_wins_and_podiums_female.csv', header=True, index=True)

	#title="podiums by event"
	dtf_20p.to_csv('European_Championship_Lead_Podiums_by_Event_male.csv', header=True, index=True)
	dtf_21.to_csv('European_Championship_Lead_Podiums_by_Event_female.csv', header=True, index=True)
	dtf_22p.to_csv('European_Championship_Speed_Podiums_by_Event_male.csv', header=True, index=True)
	dtf_23p.to_csv('European_Championship_Speed_Podiums_by_Event_female.csv', header=True, index=True)
	dtf_24p.to_csv('European_Championship_Boulder_Podiums_by_Event_male.csv', header=True, index=True)
	dtf_25p.to_csv('European_Championship_Boulder_Podiums_by_Event_female.csv', header=True, index=True)
	dtf_26p.to_csv('European_Championship_combined_Podiums_by_Event_male.csv', header=True, index=True)
	dtf_27p.to_csv('European_Championship_combined_Podiums_by_Event_female.csv', header=True, index=True)
	dtf_26BLp.to_csv('European_Championship_Boulder_Lead_Podiums_by_Event_male.csv', header=True, index=True)
	dtf_27BLp.to_csv('European_Championship_Boulder_Lead_Podiums_by_Event_female.csv', header=True, index=True)
	
	#
	# how to close the connection to the database
	#
	conn.close()
	print("thanks for all the fish")




