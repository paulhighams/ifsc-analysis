#from neo4j import __version__ as neo4j_version
#print(neo4j_version)

from neo4j import GraphDatabase
import pandas as pd
#import itertools
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
	
	# Number of World Cups
	query_1 = '''MATCH (ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	WHERE  e.EventTypeName = 'World Cup' AND ev.StartDate < date("'''+todayStr+'''")
	RETURN e.EventTypeName, count(ev) AS Total
	'''
	
	# Number of World Cups hosted by Country
	query_2 = '''MATCH (ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Cup'}),
    (v:Venue)-[:HOSTS]->(ev:Event),
    (v:Venue)-[:IS_PART_OF]->(c:Country)
	WHERE ev.StartDate < date("'''+todayStr+'''")
	RETURN c.CountryName AS Country, count(ev) AS Total
	ORDER BY Total DESC
	'''
	
	# Number of World Cup events by Venue
	query_3 = '''MATCH (ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Cup'}),
    (v:Venue)-[:HOSTS]->(ev:Event)
	WHERE  ev.StartDate < date("'''+todayStr+'''")
	RETURN v.VenueName AS Venue, count(ev) AS Total
	ORDER BY Total DESC
	'''
	
	# Number of world cup events per year
	query_4 = '''MATCH (ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Cup'}),
    (ev:Event)-[:OCCURS_IN]->(yr:Year)
	RETURN e.EventTypeName, yr.YearName AS Year, count(yr) AS NumEvents
	ORDER BY Year
	'''
	
	#Number of world Cup competitions by comp-type
	query_5 = '''MATCH (ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Cup'}),
    (ct:CompType)-[:CLASSIFIES]->(cmp:Competition),
    (ev:Event)-[:CONSISTS_OF]->(cmp:Competition)
	WHERE  ev.StartDate < date("'''+todayStr+'''")
	RETURN e.EventTypeName, ct.CompTypeName AS Discipline, count(cmp) as NumComps
	ORDER BY Discipline
	'''
	
	#count the number of world cup evrnts by Year by Discipline
	query_6 = '''MATCH (ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Cup'}),
    (ev:Event)-[:OCCURS_IN]->(y:Year),
    (ev:Event)-[:CONSISTS_OF]->(cmp:Competition),
    (ct:CompType)-[:CLASSIFIES]->(cmp:Competition)
	RETURN y.YearName AS Year, ct.CompTypeName AS Discipline, count(DISTINCT ev.EventName) AS NumEvents
	ORDER BY Year
	'''
	
	#Number of athletes to represent a country by discipline at world cups
	query_7 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Cup'}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, ct.CompTypeName AS Discipline, count(DISTINCT ath.PersonName) AS Athletes
	ORDER BY Country
	'''
	
	#Number of athletes competing in a year by country at world cups
	query_8 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[oc:OCCURS_IN]->(yr:Year),
	(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Cup'})
	RETURN yr.YearName AS Year, cntry.CountryName AS Country, count(DISTINCT ath.PersonName) AS NumAthletes
	ORDER BY Year, Country
	'''
	
	#Number of countries competing in a year at world cups
	query_9 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[oc:OCCURS_IN]->(yr:Year),
	(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: 'World Cup'})
	RETURN yr.YearName AS Year, count(DISTINCT cntry.CountryName) AS NumCountries
	ORDER BY Year
	'''
	
	#Number of athletes who have Podiumed at World Cups per country per discipline
	query_10 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[p:PODIUM]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, ct.CompTypeName AS Discipline, count(DISTINCT ath.PersonName) as NumAthleteswithWCupPodiums
	ORDER BY NumAthleteswithWCupPodiums DESC
	'''
	
	#Number of athletes who have won at World Cups per country per discipline
	query_11 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[w:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, ct.CompTypeName AS Discipline, count(DISTINCT ath.PersonName) as NumAthleteswithWCupWins
	ORDER BY NumAthleteswithWCupWins DESC
	'''
	
	#Country Medal Table World Cups - medals by gold, silver, bronze, Total for each discipline
	query_12 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4
	RETURN cntry.CountryName as Country, ct.CompTypeName as Discipline, COUNT(att.FinOne) as Gold, COUNT(att.FinTwo) AS Silver, COUNT(att.FinThree) AS Bronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY Total DESC, Gold DESC, Silver DESC, Bronze DESC
	'''

	#Country Medal Table World Cups - medals by gold, silver, bronze, Total
	query_13 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4
	RETURN cntry.CountryName as Country, COUNT(att.FinOne) as Gold, COUNT(att.FinTwo) AS Silver, COUNT(att.FinThree) AS Bronze, COUNT(att.FinThree) + COUNT(att.FinTwo) + COUNT(att.FinOne) AS Total
	ORDER BY Total DESC, Gold DESC, Silver DESC, Bronze DESC
	'''

	# when a podium has all been from the same country
	query_14 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[pod:PODIUM]->(cmp:Competition)
	WITH cmp as comp1, count(DISTINCT cntry.CountryName) as podcnt
	WHERE podcnt = 1
	WITH comp1
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(comp1:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE att.FinishPosition < 4 and ct.CompTypeName IN ["Boulder", "Lead"]
	RETURN cntry.CountryName as Country, ct.CompTypeName as CompType, comp1.CompetitionName as WCupComp, collect(ath.PersonName) as Athletes
	ORDER BY ct.CompTypeName
	'''

	#Number of athletes who have Podiumed at World Cups per country all disciplines
	query_16 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[p:PODIUM]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, count(DISTINCT ath.PersonName) as NumAthleteswithWCupPodiums
	ORDER BY NumAthleteswithWCupPodiums DESC
	'''
	
	#Number of athletes who have won at World Cups per country all disciplines
	query_17 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[w:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"}),
	(cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN cntry.CountryName AS Country, count(DISTINCT ath.PersonName) as NumAthleteswithWCupWins
	ORDER BY NumAthleteswithWCupWins DESC
	'''

	#WCSeries medals by country per discipline
	query_18 = '''MATCH (ct:CompType)-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete)-[:REPRESENTS]->(c)
	where r.FinishPosition < 4
	RETURN ct.CompTypeName AS Discipline, c.IOCAlpha3 AS Country, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS Gold,
	SUM(CASE r.FinishPosition WHEN 2 THEN 1 ELSE 0 END) AS Silver, SUM(CASE r.FinishPosition WHEN 3 THEN 1 ELSE 0 END) AS Bronze, count(r.FinishPosition) as Total
	ORDER BY Gold DESC, Silver DESC, Bronze Desc
	'''

	#WCSeries medals by country all countries
	query_19 = '''MATCH (ct:CompType)-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete)-[:REPRESENTS]->(c)
	where r.FinishPosition < 4
	RETURN c.IOCAlpha3 AS Country, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS Gold,
	SUM(CASE r.FinishPosition WHEN 2 THEN 1 ELSE 0 END) AS Silver, SUM(CASE r.FinishPosition WHEN 3 THEN 1 ELSE 0 END) AS Bronze, count(r.FinishPosition) as Total
	ORDER BY Gold DESC, Silver DESC, Bronze Desc
	'''

	#Number of WCups attended by an Athlete (sex) in a single discipline
	query_20 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWCups
		ORDER BY NumWCups DESC
	'''
	query_21 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Boulder"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWCups
		ORDER BY NumWCups DESC
	'''
	query_22 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWCups
		ORDER BY NumWCups DESC
	'''
	query_23 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWCups
		ORDER BY NumWCups DESC
	'''
	query_24 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWCups
		ORDER BY NumWCups DESC
	'''
	query_25 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWCups
		ORDER BY NumWCups DESC
	'''
	# as above but all disciplines
	query_26 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWCups
		ORDER BY NumWCups DESC
	'''
	query_27 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
		RETURN ath.PersonName AS Athlete,cntry.CountryName AS Country, count(cmp.CompetitionName) as NumWCups
		ORDER BY NumWCups DESC
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

	# get the 10 best finishes in a WC Series for each M/F and Discipline combination queries 30 to 35
	query_30 = '''MATCH (c:Country)
	WITH c.IOCAlpha3 AS CntryList
	UNWIND CntryList AS CntryItem 
	  MATCH (ct:CompType {CompTypeName: 'Boulder'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete  {Sex: 'Female'})-[:REPRESENTS]->(c:Country)
	  where r.FinishPosition < 50 and c.IOCAlpha3 = CntryItem
	WITH ath.PersonName as Athlete, ath.Sex as Gender, c.IOCAlpha3 as Country,ct.CompTypeName as Discipline, wcs.WCSeriesName as Series, r.FinishPosition as FinPosn
	ORDER BY Country, Discipline, Gender, FinPosn
	RETURN Country, Discipline, Athlete, Gender, Series, FinPosn
	'''

	query_31 = '''MATCH (c:Country)
	WITH c.IOCAlpha3 AS CntryList
	UNWIND CntryList AS CntryItem 
		MATCH (ct:CompType {CompTypeName: 'Boulder'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete  {Sex: "Male"})-[:REPRESENTS]->(c:Country)
		WHERE r.FinishPosition < 50 and c.IOCAlpha3 = CntryItem
	WITH ath.PersonName as Athlete, ath.Sex as Gender, c.IOCAlpha3 as Country,ct.CompTypeName as Discipline, wcs.WCSeriesName as Series, r.FinishPosition as FinPosn
	ORDER BY Country, Discipline, Gender, FinPosn
	RETURN Country, Discipline, Athlete, Gender, Series, FinPosn
	'''

	query_32 = '''MATCH (c:Country)
	WITH c.IOCAlpha3 AS CntryList
	UNWIND CntryList AS CntryItem 
		MATCH (ct:CompType {CompTypeName: 'Lead'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete  {Sex: "Female"})-[:REPRESENTS]->(c:Country)
		WHERE r.FinishPosition < 50 and c.IOCAlpha3 = CntryItem
	WITH ath.PersonName as Athlete, ath.Sex as Gender, c.IOCAlpha3 as Country,ct.CompTypeName as Discipline, wcs.WCSeriesName as Series, r.FinishPosition as FinPosn
	ORDER BY Country, Discipline, Gender, FinPosn
	RETURN Country, Discipline, Athlete, Gender, Series, FinPosn
	'''

	query_33 = '''MATCH (c:Country)
	WITH c.IOCAlpha3 AS CntryList
	UNWIND CntryList AS CntryItem 
		MATCH (ct:CompType {CompTypeName: 'Lead'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete  {Sex: "Male"})-[:REPRESENTS]->(c:Country)
		WHERE r.FinishPosition < 50 and c.IOCAlpha3 = CntryItem
	WITH ath.PersonName as Athlete, ath.Sex as Gender, c.IOCAlpha3 as Country,ct.CompTypeName as Discipline, wcs.WCSeriesName as Series, r.FinishPosition as FinPosn
	ORDER BY Country, Discipline, Gender, FinPosn
	RETURN Country, Discipline, Athlete, Gender, Series, FinPosn
	'''

	query_34 = '''MATCH (c:Country)
	WITH c.IOCAlpha3 AS CntryList
	UNWIND CntryList AS CntryItem 
		MATCH (ct:CompType {CompTypeName: 'Speed'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete  {Sex: "Female"})-[:REPRESENTS]->(c:Country)
		WHERE r.FinishPosition < 50 and c.IOCAlpha3 = CntryItem
	WITH ath.PersonName as Athlete, ath.Sex as Gender, c.IOCAlpha3 as Country,ct.CompTypeName as Discipline, wcs.WCSeriesName as Series, r.FinishPosition as FinPosn
	ORDER BY Country, Discipline, Gender, FinPosn
	RETURN Country, Discipline, Athlete, Gender, Series, FinPosn
	'''

	query_35 = '''MATCH (c:Country)
	WITH c.IOCAlpha3 AS CntryList
	UNWIND CntryList AS CntryItem 
		MATCH (ct:CompType {CompTypeName: 'Speed'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete  {Sex: "Male"})-[:REPRESENTS]->(c:Country)
		WHERE r.FinishPosition < 50 and c.IOCAlpha3 = CntryItem
	WITH ath.PersonName as Athlete, ath.Sex as Gender, c.IOCAlpha3 as Country,ct.CompTypeName as Discipline, wcs.WCSeriesName as Series, r.FinishPosition as FinPosn
	ORDER BY Country, Discipline, Gender, FinPosn
	RETURN Country, Discipline, Athlete, Gender, Series, FinPosn
	'''

	#get all male speed qualifying times
	query_36 = '''MATCH (ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	WHERE att.QualificationScore IS NOT NULL AND NOT att.QualificationScore IN ['FALSE START','FALL','fall','False start']
	RETURN toInteger(yr.YearName) AS Year, toFloat(head(split(att.QualificationScore,'('))) AS QualTime
	'''

	#get all the female speed qualifying times
	query_37 = '''MATCH (ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	WHERE att.QualificationScore IS NOT NULL AND NOT att.QualificationScore IN ['FALSE START','FALL','fall','False start']
	RETURN toInteger(yr.YearName) AS Year, toFloat(head(split(att.QualificationScore,'('))) AS QualTime
	'''

	#Tops in a lead final by year
	query_38 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	WHERE toUpper(att.FinalScore) = "TOP"
	RETURN yr.YearName AS Year, ath.Sex AS Gender, count(att.FinalScore) AS NumTops
	ORDER BY Gender, Year, NumTops DESC
	'''

	#Tops in a lead semifinal by year
	query_39 = '''MATCH (ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Lead"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	WHERE toUpper(att.SemiFinalScore) = "TOP"
	RETURN yr.YearName AS Year, ath.Sex AS Gender, count(att.SemiFinalScore) AS NumTops
	ORDER BY Gender, Year, NumTops DESC
	'''

	#get the previous podiums for each discipline
	query_40 = '''MATCH (ct:CompType)-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete)-[:REPRESENTS]->(c)
	MATCH (wcs:WCSeries)-[tp:TAKES_PLACE_IN]->(yr:Year)
	MATCH (wcs:WCSeries)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE r.FinishPosition < 4 AND ct.CompTypeName = "Boulder"
	RETURN ath.Sex AS Gender, collect(ath.PersonName) AS Athlete, r.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, Year DESC, Position
	'''

	query_41 = '''MATCH (ct:CompType)-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete)-[:REPRESENTS]->(c)
	MATCH (wcs:WCSeries)-[tp:TAKES_PLACE_IN]->(yr:Year)
	MATCH (wcs:WCSeries)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE r.FinishPosition < 4 AND ct.CompTypeName = "Lead"
	RETURN ath.Sex AS Gender, collect(ath.PersonName) AS Athlete, r.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, Year DESC, Position
	'''
	
	query_42 = '''MATCH (ct:CompType)-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete)-[:REPRESENTS]->(c)
	MATCH (wcs:WCSeries)-[tp:TAKES_PLACE_IN]->(yr:Year)
	MATCH (wcs:WCSeries)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE r.FinishPosition < 4 AND ct.CompTypeName = "Speed"
	RETURN ath.Sex AS Gender, collect(ath.PersonName) AS Athlete, r.FinishPosition AS Position, yr.YearName AS Year
	ORDER BY Gender, Year DESC, Position
	'''

	# get male speed fastest and slowest qualifying times
	query_43 = '''MATCH (ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	WHERE (att.FinalScore IS NOT NULL OR att.EightFinalScore IS NOT NULL OR att.QtrFinalScore IS NOT NULL OR att.SemiFinalScore IS NOT NULL)
	AND att.QualificationScore IS NOT NULL AND yr.YearName > 2012
	RETURN yr.YearName AS Year, ev.StartDate AS CompDate, cmp.CompetitionName AS Comp, MIN(toFloat(att.QualificationScore)) AS FastestQual, MAX(toFloat(att.QualificationScore)) AS SlowestQual
	ORDER BY FastestQual
	'''

	# get female speed fastest and slowest qualifying times
	query_44 = '''MATCH (ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: "Speed"})
	MATCH (ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	WHERE (att.FinalScore IS NOT NULL OR att.EightFinalScore IS NOT NULL OR att.QtrFinalScore IS NOT NULL OR att.SemiFinalScore IS NOT NULL)
	AND att.QualificationScore IS NOT NULL AND yr.YearName > 2012
	RETURN yr.YearName AS Year, ev.StartDate AS CompDate, cmp.CompetitionName AS Comp, MIN(toFloat(att.QualificationScore)) AS FastestQual, MAX(toFloat(att.QualificationScore)) AS SlowestQual
	ORDER BY FastestQual
	'''
	
	#run the queries and put the answer in dataframes
	dtf_1 = pd.DataFrame([dict(_) for _ in conn.query(query_1)])
	dtf_2 = pd.DataFrame([dict(_) for _ in conn.query(query_2)])
	dtf_3 = pd.DataFrame([dict(_) for _ in conn.query(query_3)])
	dtf_4 = pd.DataFrame([dict(_) for _ in conn.query(query_4)])
	dtf_5 = pd.DataFrame([dict(_) for _ in conn.query(query_5)])
	dtf_6 = pd.DataFrame([dict(_) for _ in conn.query(query_6)])
	dtf_7 = pd.DataFrame([dict(_) for _ in conn.query(query_7)])
	dtf_8 = pd.DataFrame([dict(_) for _ in conn.query(query_8)])
	dtf_9 = pd.DataFrame([dict(_) for _ in conn.query(query_9)])
	dtf_10 = pd.DataFrame([dict(_) for _ in conn.query(query_10)])
	dtf_11 = pd.DataFrame([dict(_) for _ in conn.query(query_11)])
	dtf_12 = pd.DataFrame([dict(_) for _ in conn.query(query_12)])
	dtf_13 = pd.DataFrame([dict(_) for _ in conn.query(query_13)])
	dtf_14 = pd.DataFrame([dict(_) for _ in conn.query(query_14)])
	#dtf_15 = pd.DataFrame([dict(_) for _ in conn.query(query_15)])
	dtf_16 = pd.DataFrame([dict(_) for _ in conn.query(query_16)])
	dtf_17 = pd.DataFrame([dict(_) for _ in conn.query(query_17)])
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
	#dtf_28 = pd.DataFrame([dict(_) for _ in conn.query(query_28)])
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
	dtf_38 = pd.DataFrame([dict(_) for _ in conn.query(query_38)])
	dtf_39 = pd.DataFrame([dict(_) for _ in conn.query(query_39)])
	dtf_40 = pd.DataFrame([dict(_) for _ in conn.query(query_40)])
	dtf_41 = pd.DataFrame([dict(_) for _ in conn.query(query_41)])
	dtf_42 = pd.DataFrame([dict(_) for _ in conn.query(query_42)])
	dtf_43 = pd.DataFrame([dict(_) for _ in conn.query(query_43)])
	dtf_44 = pd.DataFrame([dict(_) for _ in conn.query(query_44)])
		
	WCTotEv = dtf_1.at[0,'Total']
	
	# get the total WC per discipline, there is one row per discipline in disciplien order
	WCBoulderEv = dtf_5.at[0,'NumComps']
	WCBoulderLeadEv = dtf_5.at[1,'NumComps']
	WCLeadEv = dtf_5.at[2,'NumComps']
	WCSpeedEv = dtf_5.at[3,'NumComps']

	data = {'StatName': ['Number of World Cup Events', 'Number of Boulder Competitions', 'Number of Boulder-Lead Competitions', 'Number of Lead Competitions', 'Number of Speed Competitions'],
		'theStats': [WCTotEv, WCBoulderEv, WCBoulderLeadEv, WCLeadEv, WCSpeedEv]}
	#print (data)
	big_number_df = pd.DataFrame(data)

	dtf_4_9 = pd.merge( dtf_4, dtf_9, how="outer", on=["Year"])
	dtf_4_9 = dtf_4_9.fillna(0)
	#print (dtf_4_9.info)

	#Need to create dummy rows for all combinations of year and country that don't exist and set NumAthletes to Zero
	#create a second dataframe of all combinations, concatenate and then groupby to get all rows.
	Countries8 = list(dtf_8['Country'].unique())
	NumCountries = len(Countries8)
	Years8 = list(dtf_8['Year'].unique())
	dts_8all = []
	for i in Years8:
		for j in Countries8:
			dts_8all.append({'Year' : i, 'Country' : j})
	dtf_8all = pd.DataFrame(dts_8all)
	dtf_8all['NumAthletes'] = 0
	dtf_8all.sort_values(by=['Year','Country'], inplace=True)
	dtf_8all['Year'] = dtf_8all['Year'].astype(int)
	#print (dtf_8.dtypes)
	#print (dtf_8all.dtypes)
	dtf_8concat = pd.concat([dtf_8, dtf_8all], axis=0)
	dtf_8final = dtf_8concat.groupby(['Year','Country']).agg({'NumAthletes': ['sum']})
	dtf_8final.columns = ['NumAthletes']
	dtf_8final = dtf_8final.reset_index()

	
	dtf_10_11 = pd.merge( dtf_11, dtf_10, how="outer", on=["Country","Discipline"])
	dtf_10_11 = dtf_10_11.fillna(0)
	dtf_10_11['NumAthleteswithWCupWins'] = dtf_10_11['NumAthleteswithWCupWins'].astype(int)
	dtf_10_11.index = dtf_10_11.index + 1
	
	#join tables, change col from float to int, sort by wins then podiums and tidy up the index
	dtf_16_17 = pd.merge( dtf_17, dtf_16, how="outer", on=["Country"])
	dtf_16_17 = dtf_16_17.fillna(0)
	dtf_16_17['NumAthleteswithWCupWins'] = dtf_16_17['NumAthleteswithWCupWins'].astype(int)
	dtf_16_17.sort_values(by = ['NumAthleteswithWCupWins','NumAthleteswithWCupPodiums'], ascending = False, inplace = True)
	dtf_16_17.reset_index(drop=True, inplace=True)
	dtf_16_17.index = dtf_16_17.index + 1

	#split into the 3 disciplines
	dtf_10_11_lead = dtf_10_11[dtf_10_11['Discipline'] == 'Lead']
	dtf_10_11_speed = dtf_10_11[dtf_10_11['Discipline'] == 'Speed']
	dtf_10_11_boulder = dtf_10_11[dtf_10_11['Discipline'] == 'Boulder']
	dtf_10_11_lead.reset_index(drop=True, inplace=True); dtf_10_11_lead.index = dtf_10_11_lead.index +1
	dtf_10_11_speed.reset_index(drop=True, inplace=True); dtf_10_11_speed.index = dtf_10_11_speed.index +1
	dtf_10_11_boulder.reset_index(drop=True, inplace=True); dtf_10_11_boulder.index = dtf_10_11_boulder.index +1

	dtf_12_lead = dtf_12[dtf_12['Discipline'] == 'Lead']
	dtf_12_speed = dtf_12[dtf_12['Discipline'] == 'Speed']
	dtf_12_boulder = dtf_12[dtf_12['Discipline'] == 'Boulder']
	dtf_12_lead.reset_index(drop=True, inplace=True); dtf_12_lead.index = dtf_12_lead.index + 1
	dtf_12_speed.reset_index(drop=True, inplace=True); dtf_12_speed.index = dtf_12_speed.index + 1
	dtf_12_boulder.reset_index(drop=True, inplace=True); dtf_12_boulder.index = dtf_12_boulder.index + 1
	dtf_13.reset_index(drop=True, inplace=True); dtf_13.index = dtf_13.index + 1

	dtf_14_Lead = dtf_14[dtf_14['CompType'] == 'Lead']
	dtf_14_Boulder = dtf_14[dtf_14['CompType'] == 'Boulder']
	dtf_14_Lead.drop(['CompType'], axis = 1)
	dtf_14_Boulder.drop(['CompType'], axis = 1)

	dtf_18_lead = dtf_18[dtf_18['Discipline'] == 'Lead']
	dtf_18_speed = dtf_18[dtf_18['Discipline'] == 'Speed']
	dtf_18_boulder = dtf_18[dtf_18['Discipline'] == 'Boulder']
	dtf_18_lead.reset_index(drop=True, inplace=True); dtf_18_lead.index = dtf_18_lead.index + 1
	dtf_18_speed.reset_index(drop=True, inplace=True); dtf_18_speed.index = dtf_18_speed.index + 1
	dtf_18_boulder.reset_index(drop=True, inplace=True); dtf_18_boulder.index = dtf_18_boulder.index + 1
	dtf_19.reset_index(drop=True, inplace=True); dtf_19.index = dtf_19.index + 1

	# add a column to current atletes to indicate they are currently competing
	dtf_29F['Status'] = ' (Current)'
	dtf_29M['Status'] = ' (Current)'

	#create a function to combine the name and the status field
	def combine_Athlete_Status (ath,stat):
		if stat == ' (Current)':
			athstat = ath+stat
			return athstat
		else:
			return ath

	# add current flag to the global list
	dtf_20_gbl = pd.merge(dtf_20, dtf_29F, how="left", on=["Athlete", "Country"])
	dtf_20_gbl['Athlete'] = dtf_20_gbl.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_20_gbl.drop(columns=['Status'], inplace = True)

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_20_temp = dtf_20.groupby('Country').head(3).reset_index(drop=True)
	dtf_20_temp.sort_values(by=['Country','NumWCups'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_20_cur = pd.merge(dtf_20_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_20_country = dtf_20_cur.loc[dtf_20_cur['Status'] == ' (Current)','Country']
	dtf_20_country.drop_duplicates(keep='first',inplace=True)
	l20 = dtf_20_country.values.tolist()
	#use the list to filter for countries
	dtf_20_filtered = dtf_20_cur[dtf_20_cur['Country'].isin(l20)]
	dtf_20_filtered = dtf_20_filtered.fillna('')
	dtf_20_filtered['Athlete'] = dtf_20_filtered.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_20_filtered.drop(columns=['Status'], inplace = True)
	
	# add current flag to the global list
	dtf_21_gbl = pd.merge(dtf_21, dtf_29M, how="left", on=["Athlete", "Country"])
	dtf_21_gbl['Athlete'] = dtf_21_gbl.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_21_gbl.drop(columns=['Status'], inplace = True)

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_21_temp = dtf_21.groupby('Country').head(3).reset_index(drop=True)
	dtf_21_temp.sort_values(by=['Country','NumWCups'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_21_cur = pd.merge(dtf_21_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_21_country = dtf_21_cur.loc[dtf_21_cur['Status'] == ' (Current)','Country']
	dtf_21_country.drop_duplicates(keep='first',inplace=True)
	l21 = dtf_21_country.values.tolist()
	#use the list to filter for countries
	dtf_21_filtered = dtf_21_cur[dtf_21_cur['Country'].isin(l21)]
	dtf_21_filtered = dtf_21_filtered.fillna('')
	dtf_21_filtered['Athlete'] = dtf_21_filtered.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_21_filtered.drop(columns=['Status'], inplace = True)

	# add current flag to the global list
	dtf_22_gbl = pd.merge(dtf_22, dtf_29F, how="left", on=["Athlete", "Country"])
	dtf_22_gbl['Athlete'] = dtf_22_gbl.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_22_gbl.drop(columns=['Status'], inplace = True)

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_22_temp = dtf_22.groupby('Country').head(3).reset_index(drop=True)
	dtf_22_temp.sort_values(by=['Country','NumWCups'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_22_cur = pd.merge(dtf_22_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_22_country = dtf_22_cur.loc[dtf_22_cur['Status'] == ' (Current)','Country']
	dtf_22_country.drop_duplicates(keep='first',inplace=True)
	l22 = dtf_22_country.values.tolist()
	#use the list to filter for countries
	dtf_22_filtered = dtf_22_cur[dtf_22_cur['Country'].isin(l22)]
	dtf_22_filtered = dtf_22_filtered.fillna('')
	dtf_22_filtered['Athlete'] = dtf_22_filtered.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_22_filtered.drop(columns=['Status'], inplace = True)

	# add current flag to the global list
	dtf_23_gbl = pd.merge(dtf_23, dtf_29M, how="left", on=["Athlete", "Country"])
	dtf_23_gbl['Athlete'] = dtf_23_gbl.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_23_gbl.drop(columns=['Status'], inplace = True)

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_23_temp = dtf_23.groupby('Country').head(3).reset_index(drop=True)
	dtf_23_temp.sort_values(by=['Country','NumWCups'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_23_cur = pd.merge(dtf_23_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_23_country = dtf_23_cur.loc[dtf_23_cur['Status'] == ' (Current)','Country']
	dtf_23_country.drop_duplicates(keep='first',inplace=True)
	l23 = dtf_23_country.values.tolist()
	#use the list to filter for countries
	dtf_23_filtered = dtf_23_cur[dtf_23_cur['Country'].isin(l23)]
	dtf_23_filtered = dtf_23_filtered.fillna('')
	dtf_23_filtered['Athlete'] = dtf_23_filtered.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_23_filtered.drop(columns=['Status'], inplace = True)

	# add current flag to the global list
	dtf_24_gbl = pd.merge(dtf_24, dtf_29F, how="left", on=["Athlete", "Country"])
	dtf_24_gbl['Athlete'] = dtf_24_gbl.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_24_gbl.drop(columns=['Status'], inplace = True)

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_24_temp = dtf_24.groupby('Country').head(3).reset_index(drop=True)
	dtf_24_temp.sort_values(by=['Country','NumWCups'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_24_cur = pd.merge(dtf_24_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_24_country = dtf_24_cur.loc[dtf_24_cur['Status'] == ' (Current)','Country']
	dtf_24_country.drop_duplicates(keep='first',inplace=True)
	l24 = dtf_24_country.values.tolist()
	#use the list to filter for countries
	dtf_24_filtered = dtf_24_cur[dtf_24_cur['Country'].isin(l24)]
	dtf_24_filtered = dtf_24_filtered.fillna('')
	dtf_24_filtered['Athlete'] = dtf_24_filtered.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_24_filtered.drop(columns=['Status'], inplace = True)

	# add current flag to the global list
	dtf_25_gbl = pd.merge(dtf_25, dtf_29M, how="left", on=["Athlete", "Country"])
	dtf_25_gbl['Athlete'] = dtf_25_gbl.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_25_gbl.drop(columns=['Status'], inplace = True)

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_25_temp = dtf_25.groupby('Country').head(3).reset_index(drop=True)
	dtf_25_temp.sort_values(by=['Country','NumWCups'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_25_cur = pd.merge(dtf_25_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_25_country = dtf_25_cur.loc[dtf_25_cur['Status'] == ' (Current)','Country']
	dtf_25_country.drop_duplicates(keep='first',inplace=True)
	l25 = dtf_25_country.values.tolist()
	#use the list to filter for countries
	dtf_25_filtered = dtf_25_cur[dtf_25_cur['Country'].isin(l25)]
	dtf_25_filtered = dtf_25_filtered.fillna('')
	dtf_25_filtered['Athlete'] = dtf_25_filtered.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_25_filtered.drop(columns=['Status'], inplace = True)

	# add current flag to the global list
	dtf_26_gbl = pd.merge(dtf_26, dtf_29F, how="left", on=["Athlete", "Country"])
	dtf_26_gbl['Athlete'] = dtf_26_gbl.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_26_gbl.drop(columns=['Status'], inplace = True)

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_26_temp = dtf_26.groupby('Country').head(3).reset_index(drop=True)
	dtf_26_temp.sort_values(by=['Country','NumWCups'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_26_cur = pd.merge(dtf_26_temp, dtf_29F, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_26_country = dtf_26_cur.loc[dtf_26_cur['Status'] == ' (Current)','Country']
	dtf_26_country.drop_duplicates(keep='first',inplace=True)
	l26 = dtf_26_country.values.tolist()
	#use the list to filter for countries
	dtf_26_filtered = dtf_26_cur[dtf_26_cur['Country'].isin(l26)]
	dtf_26_filtered = dtf_26_filtered.fillna('')
	dtf_26_filtered['Athlete'] = dtf_26_filtered.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_26_filtered.drop(columns=['Status'], inplace = True)

	# add current flag to the global list
	dtf_27_gbl = pd.merge(dtf_27, dtf_29M, how="left", on=["Athlete", "Country"])
	dtf_27_gbl['Athlete'] = dtf_27_gbl.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_27_gbl.drop(columns=['Status'], inplace = True)

	# get dataframe sorted by NumWCups in each Country, and then get top 3 for each Country
	dtf_27_temp = dtf_27.groupby('Country').head(3).reset_index(drop=True)
	dtf_27_temp.sort_values(by=['Country','NumWCups'], ascending = [True,False], inplace=True)
	#join the current competitors to the most attends, so you can see new records
	dtf_27_cur = pd.merge(dtf_27_temp, dtf_29M, how="left", on=["Athlete", "Country"])
	#filter so only countries where someone is current is left
	#create a list of countries with a current
	dtf_27_country = dtf_27_cur.loc[dtf_27_cur['Status'] == ' (Current)','Country']
	dtf_27_country.drop_duplicates(keep='first',inplace=True)
	l27 = dtf_27_country.values.tolist()
	#use the list to filter for countries
	dtf_27_filtered = dtf_27_cur[dtf_27_cur['Country'].isin(l27)]
	dtf_27_filtered = dtf_27_filtered.fillna('')
	dtf_27_filtered['Athlete'] = dtf_27_filtered.apply(lambda x: combine_Athlete_Status(x.Athlete, x.Status), axis=1)
	dtf_27_filtered.drop(columns=['Status'], inplace = True)

	#Group the best fish dataframes together
	
	dtf_30_trim = dtf_30.sort_values('FinPosn',ascending=True).groupby('Country').head(10)
	dtf_31_trim = dtf_31.sort_values('FinPosn',ascending=True).groupby('Country').head(10)
	dtf_32_trim = dtf_32.sort_values('FinPosn',ascending=True).groupby('Country').head(10)
	dtf_33_trim = dtf_33.sort_values('FinPosn',ascending=True).groupby('Country').head(10)
	dtf_34_trim = dtf_34.sort_values('FinPosn',ascending=True).groupby('Country').head(10)
	dtf_35_trim = dtf_35.sort_values('FinPosn',ascending=True).groupby('Country').head(10)
	dtf_30_35 = pd.concat([dtf_30_trim, dtf_31_trim, dtf_32_trim, dtf_33_trim, dtf_34_trim, dtf_35_trim], axis=0)

	#Get rid of results before 2012 as they skew the y-axis
	dtf_36_trim = dtf_36[dtf_36['Year'] > 2011]
	dtf_37_trim = dtf_37[dtf_37['Year'] > 2011]
	#get rid of outlier times
	dtf_36_fin = dtf_36_trim[dtf_36_trim['QualTime'] < 21]
	dtf_37_fin = dtf_37_trim[dtf_37_trim['QualTime'] < 34]

	dtf_38_39 = pd.merge( dtf_38, dtf_39, how="outer", on=["Year","Gender"])
	dtf_38_39 = dtf_38_39.fillna(0)
	dtf_38_39['NumTops'] = dtf_38_39['NumTops_x'] + dtf_38_39['NumTops_y']

	#dtf_38_Male = dtf_38[dtf_38['Gender'] == 'Male']
	#dtf_38_Female = dtf_38[dtf_38['Gender'] == 'Female']
	#dtf_39_Male = dtf_39[dtf_39['Gender'] == 'Male']
	#dtf_39_Female = dtf_39[dtf_39['Gender'] == 'Female']

	# set the indexes ready for display to start at 1
	dtf_2.index = dtf_2.index + 1
	dtf_3.index = dtf_3.index + 1
	dtf_20_gbl.index = dtf_20_gbl.index + 1
	dtf_21_gbl.index = dtf_21_gbl.index + 1
	dtf_22_gbl.index = dtf_22_gbl.index + 1
	dtf_23_gbl.index = dtf_23_gbl.index + 1
	dtf_24_gbl.index = dtf_24_gbl.index + 1
	dtf_25_gbl.index = dtf_25_gbl.index + 1
	dtf_26_gbl.index = dtf_26_gbl.index + 1
	dtf_27_gbl.index = dtf_27_gbl.index + 1

	dtf_40A = dtf_40.pivot(index=['Year'],columns=['Gender','Position'], values='Athlete')
	dtf_41A = dtf_41.pivot(index=['Year'],columns=['Gender','Position'], values='Athlete')
	dtf_42A = dtf_42.pivot(index=['Year'],columns=['Gender','Position'], values='Athlete')
	dtf_40B = dtf_40A.sort_index(ascending = False)
	dtf_41B = dtf_41A.sort_index(ascending = False)
	dtf_42B = dtf_42A.sort_index(ascending = False)

	#produce csv files

	#title="Event and Country Statistics"	
	dtf_3.to_csv('Top_20_WCup_venues.csv', header=True, index=True)
	dtf_2.to_csv('Top_20_Num_of_WCup_Events_by_Country.csv', header=True, index=True)
	big_number_df.to_csv('WCup_big_numbers.csv', header=True, index=True)
	dtf_4_9.to_csv('Number_WCup_events_countries_by_Year.csv', header=True, index=True)
	dtf_6.to_csv('Number_WCup_events_discipline_by_Year.csv', header=True, index=True)
			
	#title="World Cup Competition and Athlete Participation Statistics Global"

	dtf_20_gbl.to_csv('Number_of_Boulder_World_Cups_attended_female_Top_20.csv', header=True, index=True)
	dtf_21_gbl.to_csv('Number_of_Boulder_World_Cups_attended_male_Top_20.csv', header=True, index=True)
	dtf_22_gbl.to_csv('Number_of_Lead_World_Cups_attended_female_Top_20.csv', header=True, index=True)
	dtf_23_gbl.to_csv('Number_of_Lead_World_Cups_attended_fale_Top_20.csv', header=True, index=True)
	dtf_24_gbl.to_csv('Number_of_Speed_World_Cups_attended_female_Top_20.csv', header=True, index=True)
	dtf_25_gbl.to_csv('Number_of_Speed_World_Cups_attended_male_Top_20.csv', header=True, index=True)
	dtf_26_gbl.to_csv('Number_of_all_disciplines_World_Cups_attended_female_Top_20.csv', header=True, index=True)
	dtf_27_gbl.to_csv('Number_of_all_disciplines_World_Cups_attended_male_Top_20.csv', header=True, index=True)
	dtf_8final.to_csv('Number_of_athletes_representing_Country_by_Year.csv', header=True, index=True)
	#title="World Cup Competition and Athlete Participation Statistics by Country"


	dtf_20_filtered.to_csv('Number_of_Boulder_World_Cups_attended_by_Country_female_Top_3.csv', header=True, index=True)
	dtf_21_filtered.to_csv('Number_of_Boulder_World_Cups_attended_by_Country_male_Top_3.csv', header=True, index=True)
	dtf_22_filtered.to_csv('Number_of_Lead_World_Cups_attended_by_Country_female_Top_3.csv', header=True, index=True)
	dtf_23_filtered.to_csv('Number_of_Lead_World_Cups_attended_by_Country_male_Top_3.csv', header=True, index=True)
	dtf_24_filtered.to_csv('Number_of_Speed_World_Cups_attended_by_Country_female_Top_3.csv', header=True, index=True)
	dtf_25_filtered.to_csv('Number_of_Speed_World_Cups_attended_by_Country_male_Top_3.csv', header=True, index=True)
	dtf_26_filtered.to_csv('Number_of_all_disciplines_World_Cups_attended_by_Country_female_Top_3.csv', header=True, index=True)
	dtf_27_filtered.to_csv('Number_of_all_disciplines_World_Cups_attended_by_Country_male_Top_3.csv', header=True, index=True)

	#title="Country World Cup Medals Table"
	dtf_12_boulder.to_csv('World_Cups_Medal_Table_for_Boulder.csv', header=True, index=True)
	dtf_12_lead.to_csv('World_Cups_Medal_Table_for_Lead.csv', header=True, index=True)
	dtf_12_speed.to_csv('World_Cups_Medal_Table_for_Speed.csv', header=True, index=True)
	dtf_13.to_csv('World_Cups_Medal_Table_for_All_disciplines.csv', header=True, index=True)
	dtf_10_11_boulder.to_csv('Number_of_athletes_per_Country_with_World_Cup_wins_and_podiums_for_Boulder.csv', header=True, index=True)
	dtf_10_11_lead.to_csv('Number_of_athletes_per_Country_with_World_Cup_wins_and_podiums_for_Lead.csv', header=True, index=True)
	dtf_10_11_speed.to_csv('Number_of_athletes_per_Country_with_World_Cup_wins_and_podiums_for_Speed.csv', header=True, index=True)
	dtf_16_17.to_csv('Number_of_athletes_per_Country_with_World_Cup_wins_and_podiums_all_disciplines.csv', header=True, index=True)
	dtf_14_Boulder.to_csv('Country_lock_out_of_the_podium_in_boulder_World_Cup_and_World_Champs.csv', header=True, index=True)
	dtf_14_Lead.to_csv('Country_lock_out_of_the_podium_in_lead_World_Cup_and_World_Champs.csv', header=True, index=True)

	dtf_30_35.to_csv('World_Cup_Series_best_ever_performance_by_gender_and_discipline.csv', header=True, index=True)

	#title="Country World Cup Series Medal Table"
	dtf_18_boulder.to_csv('World_Cup_Series_Medal_Table_for_Boulder.csv', header=True, index=True)
	dtf_18_lead.to_csv('World_Cup_Series_Medal_Table_for_Lead.csv', header=True, index=True)
	dtf_18_speed.to_csv('World_Cup_Series_Medal_Table_for_Speed.csv', header=True, index=True)
	dtf_19.to_csv('World_Cup_Series_Medal_Table_all_Disciplines.csv', header=True, index=True)
	dtf_40B.to_csv('World_Cup_Series_Boulder_podium_list_male_and_female.csv', header=True, index=True)
	dtf_41B.to_csv('World_Cup_Series_Lead_podium_list_male_and_female.csv', header=True, index=True)
	dtf_42B.to_csv('World_Cup_Series_Speed_podium_list_male_and_female.csv', header=True, index=True)

	#title="Special Analysis World Cups"
	dtf_36_fin.to_csv('Male_Speed_Qualifying_times_by_Year', header=True, index=True)
	dtf_37_fin.to_csv('Female_Speed_Qualifying_times_by_Year', header=True, index=True)
	dtf_38.to_csv('Lead_Tops_in_Finals_by_Year', header=True, index=True)
	dtf_39.to_csv('Lead_Tops_in_Semi_Finals_by_Year', header=True, index=True)
	dtf_38_39.to_csv('Lead_Tops_in_Finals_Semi_Finals_by_Year', header=True, index=True)
	dtf_7.to_csv('Number_of_athletes_competing_per_discipline_by_year', header=True, index=True)
	dtf_43.to_csv('Male_Speed_Qualifying_per_Event_fastest_and_slowest.csv', header=True, index=True)
	dtf_44.to_csv('Female_Speed_Qualifying_per_Event_fastest_and_slowest.csv', header=True, index=True)
	#
	# how to close the connection to the database
	#
	conn.close()
	print("thanks for all the fish")




