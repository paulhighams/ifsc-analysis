#from neo4j import __version__ as neo4j_version
#print(neo4j_version)

from neo4j import GraphDatabase
import pandas as pd

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
	query_string3 = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Boulder"
	WITH cntry.CountryName AS Nation, ath.PersonName AS Winner, COUNT(att.FinOne) as Wins, (Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent
	WHERE Wins > 0
	RETURN Nation, Winner, Wins, WinPercent
	ORDER BY Nation, Winner, Wins DESC, WinPercent DESC
	'''
	dtf_data3 = pd.DataFrame([dict(_) for _ in conn.query(query_string3)])

	query_string4 = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Lead"
	WITH cntry.CountryName AS Nation, ath.PersonName AS Winner, COUNT(att.FinOne) as Wins, (Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent
	WHERE Wins > 0
	RETURN Nation, Winner, Wins, WinPercent
	ORDER BY Nation, Winner, Wins DESC, WinPercent DESC
	'''
	dtf_data4 = pd.DataFrame([dict(_) for _ in conn.query(query_string4)])
	#
	query_string5 = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Speed"
	WITH cntry.CountryName AS Nation, ath.PersonName AS Winner, COUNT(att.FinOne) as Wins, (Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent
	WHERE Wins > 0
	RETURN Nation, Winner, Wins, WinPercent
	ORDER BY Nation, Winner, Wins DESC, WinPercent DESC
	'''
	dtf_data5 = pd.DataFrame([dict(_) for _ in conn.query(query_string5)])
	#
	# This produces a GOAT table
	# reproduce for Male/female for all 3 disciplines.
	query_stringms = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Speed"
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third, (Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS Total,
	 COUNT(att.FinishPosition) AS Entered,(Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent,
	 ((Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) *100 / COUNT(att.FinishPosition)) AS PodiumPercent
	ORDER BY First DESC, Second DESC, Third DESC, WinPercent DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datams = pd.DataFrame([dict(_) for _ in conn.query(query_stringms)])
	#discard rows where they have never podiumed
	dtms = dtf_datams[(dtf_datams.First != 0) | (dtf_datams.Second != 0) | (dtf_datams.Third != 0)]

	query_stringfs = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Speed"
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third, (Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS Total,
	 COUNT(att.FinishPosition) AS Entered,(Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent,
	 ((Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) *100 / COUNT(att.FinishPosition)) AS PodiumPercent
	ORDER BY First DESC, Second DESC, Third DESC, WinPercent DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datafs = pd.DataFrame([dict(_) for _ in conn.query(query_stringfs)])
	#discard rows where they have never podiumed
	dtfs = dtf_datafs[(dtf_datafs.First != 0) | (dtf_datafs.Second != 0) | (dtf_datafs.Third != 0)]

	query_stringml = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Lead"
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third, (Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS Total,
	 COUNT(att.FinishPosition) AS Entered,(Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent,
	 ((Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) *100 / COUNT(att.FinishPosition)) AS PodiumPercent
	ORDER BY First DESC, Second DESC, Third DESC, WinPercent DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_dataml = pd.DataFrame([dict(_) for _ in conn.query(query_stringml)])
	#discard rows where they have never podiumed
	dtml = dtf_dataml[(dtf_dataml.First != 0) | (dtf_dataml.Second != 0) | (dtf_dataml.Third != 0)]

	query_stringfl = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Lead"
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third, (Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS Total,
	 COUNT(att.FinishPosition) AS Entered,(Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent,
	 ((Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) *100 / COUNT(att.FinishPosition)) AS PodiumPercent
	ORDER BY First DESC, Second DESC, Third DESC, WinPercent DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datafl = pd.DataFrame([dict(_) for _ in conn.query(query_stringfl)])
	#discard rows where they have never podiumed
	dtfl = dtf_datafl[(dtf_datafl.First != 0) | (dtf_datafl.Second != 0) | (dtf_datafl.Third != 0)]


	query_stringmb = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Boulder"
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third, (Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS Total,
	 COUNT(att.FinishPosition) AS Entered,(Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent,
	 ((Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) *100 / COUNT(att.FinishPosition)) AS PodiumPercent
	ORDER BY First DESC, Second DESC, Third DESC, WinPercent DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datamb = pd.DataFrame([dict(_) for _ in conn.query(query_stringmb)])
	#discard rows where they have never podiumed
	dtmb = dtf_datamb[(dtf_datamb.First != 0) | (dtf_datamb.Second != 0) | (dtf_datamb.Third != 0)]

	#
	query_stringfb = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName = "Boulder"
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third, (Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS Total,
	 COUNT(att.FinishPosition) AS Entered,(Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent,
	 ((Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) *100 / COUNT(att.FinishPosition)) AS PodiumPercent
	ORDER BY First DESC, Second DESC, Third DESC, WinPercent DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datafb = pd.DataFrame([dict(_) for _ in conn.query(query_stringfb)])
	#discard rows where they have never podiumed
	dtfb = dtf_datafb[(dtf_datafb.First != 0) | (dtf_datafb.Second != 0) | (dtf_datafb.Third != 0)]

	query_stringma = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third, (Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS Total,
	 COUNT(att.FinishPosition) AS Entered,(Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent,
	 ((Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) *100 / COUNT(att.FinishPosition)) AS PodiumPercent
	ORDER BY First DESC, Second DESC, Third DESC, WinPercent DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datama = pd.DataFrame([dict(_) for _ in conn.query(query_stringma)])
	#discard rows where they have never podiumed
	dtma = dtf_datama[(dtf_datama.First != 0) | (dtf_datama.Second != 0) | (dtf_datama.Third != 0)]

	#
	query_stringfa = '''
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third, (Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS Total,
	 COUNT(att.FinishPosition) AS Entered,(Count(att.FinOne) *100 / COUNT(att.FinishPosition)) AS WinPercent,
	 ((Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) *100 / COUNT(att.FinishPosition)) AS PodiumPercent
	ORDER BY First DESC, Second DESC, Third DESC, WinPercent DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datafa = pd.DataFrame([dict(_) for _ in conn.query(query_stringfa)])
	#discard rows where they have never podiumed
	dtfa = dtf_datafa[(dtf_datafa.First != 0) | (dtf_datafa.Second != 0) | (dtf_datafa.Third != 0)]

	#########################
	# now get wcup series results
	#########################
	query_mb_wcs = '''
	MATCH (ct:CompType {CompTypeName: 'Boulder'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete {Sex: 'Male'})-[:REPRESENTS]->(c)
	where r.FinishPosition < 6
	RETURN ath.PersonName+' ('+c.IOCAlpha3+')' AS Athlete, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS WCSeriesWins, count(r.FinishPosition) as WCSeriesTop5
	ORDER BY WCSeriesWins DESC, WCSeriesTop5 DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datamb_wcs = pd.DataFrame([dict(_) for _ in conn.query(query_mb_wcs)])

	query_fb_wcs = '''
	MATCH (ct:CompType {CompTypeName: 'Boulder'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete {Sex: 'Female'})-[:REPRESENTS]->(c)
	where r.FinishPosition < 6
	RETURN ath.PersonName+' ('+c.IOCAlpha3+')' AS Athlete, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS WCSeriesWins, count(r.FinishPosition) as WCSeriesTop5
	ORDER BY WCSeriesWins DESC, WCSeriesTop5 DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datafb_wcs = pd.DataFrame([dict(_) for _ in conn.query(query_fb_wcs)])

	query_ml_wcs = '''
	MATCH (ct:CompType {CompTypeName: 'Lead'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete {Sex: 'Male'})-[:REPRESENTS]->(c)
	where r.FinishPosition < 6
	RETURN ath.PersonName+' ('+c.IOCAlpha3+')' AS Athlete, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS WCSeriesWins, count(r.FinishPosition) as WCSeriesTop5
	ORDER BY WCSeriesWins DESC, WCSeriesTop5 DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_dataml_wcs = pd.DataFrame([dict(_) for _ in conn.query(query_ml_wcs)])

	query_fl_wcs = '''
	MATCH (ct:CompType {CompTypeName: 'Lead'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete {Sex: 'Female'})-[:REPRESENTS]->(c)
	where r.FinishPosition < 6
	RETURN ath.PersonName+' ('+c.IOCAlpha3+')' AS Athlete, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS WCSeriesWins, count(r.FinishPosition) as WCSeriesTop5
	ORDER BY WCSeriesWins DESC, WCSeriesTop5 DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datafl_wcs = pd.DataFrame([dict(_) for _ in conn.query(query_fl_wcs)])
	
	query_ms_wcs = '''
	MATCH (ct:CompType {CompTypeName: 'Speed'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete {Sex: 'Male'})-[:REPRESENTS]->(c)
	where r.FinishPosition < 6
	RETURN ath.PersonName+' ('+c.IOCAlpha3+')' AS Athlete, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS WCSeriesWins, count(r.FinishPosition) as WCSeriesTop5
	ORDER BY WCSeriesWins DESC, WCSeriesTop5 DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datams_wcs = pd.DataFrame([dict(_) for _ in conn.query(query_ms_wcs)])

	query_fs_wcs = '''
	MATCH (ct:CompType {CompTypeName: 'Speed'})-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete {Sex: 'Female'})-[:REPRESENTS]->(c)
	where r.FinishPosition < 6
	RETURN ath.PersonName+' ('+c.IOCAlpha3+')' AS Athlete, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS WCSeriesWins, count(r.FinishPosition) as WCSeriesTop5
	ORDER BY WCSeriesWins DESC, WCSeriesTop5 DESC
	'''

	#run the query and put the answer in a dataframe
	dtf_datafs_wcs = pd.DataFrame([dict(_) for _ in conn.query(query_fs_wcs)])

	query_ma_wcs = '''
	MATCH (wcs:WCSeries)<-[r:RANKS]-(ath:Athlete {Sex: 'Male'})-[:REPRESENTS]->(c)
	where r.FinishPosition < 6
	RETURN ath.PersonName+' ('+c.IOCAlpha3+')' AS Athlete, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS WCSeriesWins, count(r.FinishPosition) as WCSeriesTop5
	ORDER BY WCSeriesWins DESC, WCSeriesTop5 DESC
	'''
	#run the query and put the answer in a dataframe
	dtf_datama_wcs = pd.DataFrame([dict(_) for _ in conn.query(query_ma_wcs)])

	query_fa_wcs = '''
	MATCH (ct:CompType)-[cl:CLASSIFIES]->(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete {Sex: 'Female'})-[:REPRESENTS]->(c)
	where r.FinishPosition < 6
	RETURN ath.PersonName+' ('+c.IOCAlpha3+')' AS Athlete, SUM(CASE r.FinishPosition WHEN 1 THEN 1 ELSE 0 END) AS WCSeriesWins, count(r.FinishPosition) as WCSeriesTop5
	ORDER BY WCSeriesWins DESC, WCSeriesTop5 DESC
	'''

	#run the query and put the answer in a dataframe
	dtf_datafa_wcs = pd.DataFrame([dict(_) for _ in conn.query(query_fa_wcs)])
	

	# WChamp win and podiums by athlete, by discipline for Male
	query_1 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ct.CompTypeName as Discipline, ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as WChampGold, Count(att.FinTwo) as WChampSilver, Count(att.FinThree) as WChampBronze,
	(Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS WChampTotal
	ORDER BY WChampGold DESC, WChampSilver DESC, WChampBronze DESC
	'''

	# WChamp win and podiums by athlete, by discipline for Female
	query_2 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ct.CompTypeName as Discipline, ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as WChampGold, Count(att.FinTwo) as WChampSilver, Count(att.FinThree) as WChampBronze,
	(Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS WChampTotal
	ORDER BY WChampGold DESC, WChampSilver DESC, WChampBronze DESC
	'''
	# WChamp win and podiums by athlete, all discipline for Male
	query_3 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Male"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as WChampGold, Count(att.FinTwo) as WChampSilver, Count(att.FinThree) as WChampBronze,
	(Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS WChampTotal
	ORDER BY WChampGold DESC, WChampSilver DESC, WChampBronze DESC
	'''

	# WChamp win and podiums by athlete, all discipline for Female
	query_4 = '''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {Sex: "Female"})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Championship"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	RETURN ath.PersonName+' ('+cntry.IOCAlpha3+')' as Athlete, COUNT(att.FinOne) as WChampGold, Count(att.FinTwo) as WChampSilver, Count(att.FinThree) as WChampBronze,
	(Count(att.FinOne)+Count(att.FinTwo)+Count(att.FinThree)) AS WChampTotal
	ORDER BY WChampGold DESC, WChampSilver DESC, WChampBronze DESC
	'''
    
	#data for country sankey
	query_5='''MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete)-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType {EventTypeName: "World Cup"})
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ct.CompTypeName in ["Boulder","Lead","Speed"]
	RETURN ath.PersonName  as Athlete, cntry.IOCAlpha3 as Country, ath.Sex as Gender, ct.CompTypeName as Discipline, COUNT(att.FinOne) as First, COUNT(att.FinTwo) AS Second,
	 COUNT(att.FinThree) AS Third
	ORDER BY First DESC, Second DESC, Third DESC
    '''

	#run the queries and put the answer in dataframes
	dtf_1 = pd.DataFrame([dict(_) for _ in conn.query(query_1)])
	dtf_2 = pd.DataFrame([dict(_) for _ in conn.query(query_2)])
	dtf_3 = pd.DataFrame([dict(_) for _ in conn.query(query_3)])
	dtf_4 = pd.DataFrame([dict(_) for _ in conn.query(query_4)])
	dtf_5 = pd.DataFrame([dict(_) for _ in conn.query(query_5)])

	#get rid of people with 0 medals
	dtf_1_trim = dtf_1[(dtf_1.WChampGold != 0) | (dtf_1.WChampSilver != 0) | (dtf_1.WChampBronze != 0)]
	#split into the 4 disciplines
	dtf_1_lead = dtf_1_trim[dtf_1_trim['Discipline'] == 'Lead'].copy()
	dtf_1_speed = dtf_1_trim[dtf_1_trim['Discipline'] == 'Speed'].copy()
	dtf_1_boulder = dtf_1_trim[dtf_1_trim['Discipline'] == 'Boulder'].copy()
	dtf_1_combined = dtf_1_trim[dtf_1_trim['Discipline'] == 'Combined'].copy()
	dtf_1_boulderlead = dtf_1_trim[dtf_1_trim['Discipline'] == 'Boulder-Lead'].copy()
	#drop the discipline column as we dont want to show it
	dtf_1_lead.drop(columns=['Discipline'], inplace=True)
	dtf_1_speed.drop(columns=['Discipline'], inplace=True)
	dtf_1_boulder.drop(columns=['Discipline'], inplace=True)
	dtf_1_combined.drop(columns=['Discipline'], inplace=True)
	dtf_1_boulderlead.drop(columns=['Discipline'], inplace=True)

	#get rid of people with 0 medals
	dtf_2_trim = dtf_2[(dtf_2.WChampGold != 0) | (dtf_2.WChampSilver != 0) | (dtf_2.WChampBronze != 0)]
	#split into the 4 disciplines
	dtf_2_lead = dtf_2_trim[dtf_2_trim['Discipline'] == 'Lead'].copy()
	dtf_2_speed = dtf_2_trim[dtf_2_trim['Discipline'] == 'Speed'].copy()
	dtf_2_boulder = dtf_2_trim[dtf_2_trim['Discipline'] == 'Boulder'].copy()
	dtf_2_combined = dtf_2_trim[dtf_2_trim['Discipline'] == 'Combined'].copy()
	dtf_2_boulderlead = dtf_2_trim[dtf_2_trim['Discipline'] == 'Boulder-Lead'].copy()
	#drop the discipline column as we dont want to show it
	dtf_2_lead.drop(columns=['Discipline'], inplace=True)
	dtf_2_speed.drop(columns=['Discipline'], inplace=True)
	dtf_2_boulder.drop(columns=['Discipline'], inplace=True)
	dtf_2_combined.drop(columns=['Discipline'], inplace=True)

	#get rid of people with 0 medals
	dtf_3_trim = dtf_3[(dtf_3.WChampGold != 0) | (dtf_3.WChampSilver != 0) | (dtf_3.WChampBronze != 0)]

	#get rid of people with 0 medals
	dtf_4_trim = dtf_4[(dtf_4.WChampGold != 0) | (dtf_4.WChampSilver != 0) | (dtf_4.WChampBronze != 0)]

	############################################
	# now merge the wcup and wcseries and wchamp
	############################################
	dtmb_fin1 = pd.merge( dtf_datamb_wcs, dtmb, how="outer", on=["Athlete"])
	dtmb_fin1.rename(columns = {'WCSeriesWins':'WC Series Wins','WCSeriesTop5':'WC Series Top 5','First':'WCup 1st',
								'Second':'WCup 2nd','Third':'WCup 3rd','Total':'WCup Total','Entered':'WCup competed','WinPercent':'WCup Win %',
								'PodiumPercent':'WCup Podium %'}, inplace = True)
	dtmb_fin1 = dtmb_fin1.fillna(0)
	dtmb_fin = pd.merge( dtmb_fin1, dtf_1_boulder, how="outer", on=["Athlete"])
	dtmb_fin = dtmb_fin.fillna(0)
	dtmb_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']] = \
			dtmb_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']].astype(int)
	dtmb_fin = dtmb_fin.sort_values(['WC Series Wins','WChampGold','WCup 1st','WC Series Top 5','WChampSilver','WCup 2nd','WChampBronze','WCup 3rd'],
									ascending = (False,False,False,False,False,False,False,False), ignore_index = True)
	dtmb_final = dtmb_fin.iloc[:, [0,1,2,10,11,12,13,3,4,5,6,7,8,9]]
	dtmb_final.index = dtmb_final.index + 1
	###
	dtfb_fin1 = pd.merge( dtf_datafb_wcs, dtfb, how="outer", on=["Athlete"])
	dtfb_fin1.rename(columns = {'WCSeriesWins':'WC Series Wins','WCSeriesTop5':'WC Series Top 5','First':'WCup 1st',
								'Second':'WCup 2nd','Third':'WCup 3rd','Total':'WCup Total','Entered':'WCup competed','WinPercent':'WCup Win %',
								'PodiumPercent':'WCup Podium %'}, inplace = True)
	dtfb_fin1 = dtfb_fin1.fillna(0)
	dtfb_fin = pd.merge( dtfb_fin1, dtf_2_boulder, how="outer", on=["Athlete"])
	dtfb_fin = dtfb_fin.fillna(0)
	dtfb_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']] = \
		dtfb_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']].astype(int)
	dtfb_fin = dtfb_fin.sort_values(['WC Series Wins','WChampGold','WCup 1st','WC Series Top 5','WChampSilver','WCup 2nd','WChampBronze','WCup 3rd'],
									ascending = (False,False,False,False,False,False,False,False), ignore_index = True)
	dtfb_final = dtfb_fin.iloc[:, [0,1,2,10,11,12,13,3,4,5,6,7,8,9]]
	dtfb_final.index = dtfb_final.index + 1
	###
	dtml_fin1 = pd.merge( dtf_dataml_wcs, dtml, how="outer", on=["Athlete"])
	dtml_fin1.rename(columns = {'WCSeriesWins':'WC Series Wins','WCSeriesTop5':'WC Series Top 5','First':'WCup 1st',
								'Second':'WCup 2nd','Third':'WCup 3rd','Total':'WCup Total','Entered':'WCup competed','WinPercent':'WCup Win %',
								'PodiumPercent':'WCup Podium %'}, inplace = True)
	dtml_fin1 = dtml_fin1.fillna(0)
	dtml_fin = pd.merge( dtml_fin1, dtf_1_lead, how="outer", on=["Athlete"])
	dtml_fin = dtml_fin.fillna(0)
	dtml_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']] = \
		dtml_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']].astype(int)
	dtml_fin = dtml_fin.sort_values(['WC Series Wins','WChampGold','WCup 1st','WC Series Top 5','WChampSilver','WCup 2nd','WChampBronze','WCup 3rd'],
									ascending = (False,False,False,False,False,False,False,False), ignore_index = True)
	dtml_final = dtml_fin.iloc[:, [0,1,2,10,11,12,13,3,4,5,6,7,8,9]]
	dtml_final.index = dtml_final.index + 1
	###
	dtfl_fin1 = pd.merge( dtf_datafl_wcs, dtfl, how="outer", on=["Athlete"])
	dtfl_fin1.rename(columns = {'WCSeriesWins':'WC Series Wins','WCSeriesTop5':'WC Series Top 5','First':'WCup 1st',
								'Second':'WCup 2nd','Third':'WCup 3rd','Total':'WCup Total','Entered':'WCup competed','WinPercent':'WCup Win %',
								'PodiumPercent':'WCup Podium %'}, inplace = True)
	dtfl_fin1 = dtfl_fin1.fillna(0)
	dtfl_fin = pd.merge( dtfl_fin1, dtf_2_lead, how="outer", on=["Athlete"])
	dtfl_fin = dtfl_fin.fillna(0)
	dtfl_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']] = \
		dtfl_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']].astype(int)
	dtfl_fin = dtfl_fin.sort_values(['WC Series Wins','WChampGold','WCup 1st','WC Series Top 5','WChampSilver','WCup 2nd','WChampBronze','WCup 3rd'],
									ascending = (False,False,False,False,False,False,False,False), ignore_index = True)
	dtfl_final = dtfl_fin.iloc[:, [0,1,2,10,11,12,13,3,4,5,6,7,8,9]]
	dtfl_final.index = dtfl_final.index + 1
	###
	dtms_fin1 = pd.merge( dtf_datams_wcs, dtms, how="outer", on=["Athlete"])
	dtms_fin1.rename(columns = {'WCSeriesWins':'WC Series Wins','WCSeriesTop5':'WC Series Top 5','First':'WCup 1st',
								'Second':'WCup 2nd','Third':'WCup 3rd','Total':'WCup Total','Entered':'WCup competed','WinPercent':'WCup Win %',
								'PodiumPercent':'WCup Podium %'}, inplace = True)
	dtms_fin1 = dtms_fin1.fillna(0)
	dtms_fin = pd.merge( dtms_fin1, dtf_1_speed, how="outer", on=["Athlete"])
	dtms_fin = dtms_fin.fillna(0)
	dtms_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']] = \
		dtms_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']].astype(int)
	dtms_fin = dtms_fin.sort_values(['WC Series Wins','WChampGold','WCup 1st','WC Series Top 5','WChampSilver','WCup 2nd','WChampBronze','WCup 3rd'],
									ascending = (False,False,False,False,False,False,False,False), ignore_index = True)
	dtms_final = dtms_fin.iloc[:, [0,1,2,10,11,12,13,3,4,5,6,7,8,9]]
	dtms_final.index = dtms_final.index + 1
	###
	dtfs_fin1 = pd.merge( dtf_datafs_wcs, dtfs, how="outer", on=["Athlete"])
	dtfs_fin1.rename(columns = {'WCSeriesWins':'WC Series Wins','WCSeriesTop5':'WC Series Top 5','First':'WCup 1st',
								'Second':'WCup 2nd','Third':'WCup 3rd','Total':'WCup Total','Entered':'WCup competed','WinPercent':'WCup Win %',
								'PodiumPercent':'WCup Podium %'}, inplace = True)
	dtfs_fin1 = dtfs_fin1.fillna(0)
	dtfs_fin = pd.merge( dtfs_fin1, dtf_2_speed, how="outer", on=["Athlete"])
	dtfs_fin = dtfs_fin.fillna(0)
	dtfs_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']] = \
		dtfs_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']].astype(int)
	dtfs_fin = dtfs_fin.sort_values(['WC Series Wins','WChampGold','WCup 1st','WC Series Top 5','WChampSilver','WCup 2nd','WChampBronze','WCup 3rd'],
									ascending = (False,False,False,False,False,False,False,False), ignore_index = True)
	dtfs_final = dtfs_fin.iloc[:, [0,1,2,10,11,12,13,3,4,5,6,7,8,9]]
	dtfs_final.index = dtfs_final.index + 1
	###
	dtma_fin1 = pd.merge( dtf_datama_wcs, dtma, how="outer", on=["Athlete"])
	dtma_fin1.rename(columns = {'WCSeriesWins':'WC Series Wins','WCSeriesTop5':'WC Series Top 5','First':'WCup 1st',
								'Second':'WCup 2nd','Third':'WCup 3rd','Total':'WCup Total','Entered':'WCup competed','WinPercent':'WCup Win %',
								'PodiumPercent':'WCup Podium %'}, inplace = True)
	dtma_fin1 = dtma_fin1.fillna(0)
	dtma_fin = pd.merge( dtma_fin1, dtf_3_trim, how="outer", on=["Athlete"])
	dtma_fin = dtma_fin.fillna(0)
	dtma_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']] = \
		dtma_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']].astype(int)
	dtma_fin = dtma_fin.sort_values(['WC Series Wins','WChampGold','WCup 1st','WC Series Top 5','WChampSilver','WCup 2nd','WChampBronze','WCup 3rd'],
									ascending = (False,False,False,False,False,False,False,False), ignore_index = True)
	dtma_final = dtma_fin.iloc[:, [0,1,2,10,11,12,13,3,4,5,6,7,8,9]]
	dtma_final.index = dtma_final.index + 1
	###
	dtfa_fin1 = pd.merge( dtf_datafa_wcs, dtfa, how="outer", on=["Athlete"])
	dtfa_fin1.rename(columns = {'WCSeriesWins':'WC Series Wins','WCSeriesTop5':'WC Series Top 5','First':'WCup 1st',
								'Second':'WCup 2nd','Third':'WCup 3rd','Total':'WCup Total','Entered':'WCup competed','WinPercent':'WCup Win %',
								'PodiumPercent':'WCup Podium %'}, inplace = True)
	dtfa_fin1 = dtfa_fin1.fillna(0)
	dtfa_fin = pd.merge( dtfa_fin1, dtf_4_trim, how="outer", on=["Athlete"])
	dtfa_fin = dtfa_fin.fillna(0)
	dtfa_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']] = \
		dtfa_fin[['WC Series Wins','WC Series Top 5','WCup 1st','WCup 2nd','WCup 3rd','WCup Total','WCup competed','WCup Win %','WCup Podium %','WChampGold','WChampSilver','WChampBronze','WChampTotal']].astype(int)
	dtfa_fin = dtfa_fin.sort_values(['WC Series Wins','WChampGold','WCup 1st','WC Series Top 5','WChampSilver','WCup 2nd','WChampBronze','WCup 3rd'],
									ascending = (False,False,False,False,False,False,False,False), ignore_index = True)
	dtfa_final = dtfa_fin.iloc[:, [0,1,2,10,11,12,13,3,4,5,6,7,8,9]]
	dtfa_final.index = dtfa_final.index + 1
	
	#collect the data to build the sankey diagram
	# dtf5 has all the data in
	#get rid of people with 0 medals
	dtf_5_trim = dtf_5[(dtf_5.First != 0) | (dtf_5.Second != 0) | (dtf_5.Third != 0)]

	# get series data for racecharts

	# create the dataframe of positions ans scores
	dtf_posn_points = pd.DataFrame ({"Position": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
		41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80],
		"points": [1000,805,690,610,545,495,455,415,380,350,325,300,280,260,240,220,205,185,170,155,145,130,120,105,95,84,73,63,56,48,42,37,33,30,27,24,21,19,17,15,
		14,13,12,11,11,10,9,9,8,8,7,7,7,6,6,6,5,5,5,4,4,4,4,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1]})
	
	# Get top 10 athletes per gender per discipline, then get their results for the year
	query_11 = '''MATCH (yr:Year)-[tp:TAKES_PLACE_IN]-(wcs:WCSeries)<-[r:RANKS]-(ath:Athlete)-[:REPRESENTS]->(c)
	MATCH (ct:CompType)-[cl:CLASSIFIES]->(wcs:WCSeries)
	WHERE r.FinishPosition < 11
	AND yr.YearName = 2025
	AND ct.CompTypeName IN ["Boulder","Lead","Speed"]
	WITH ct.CompTypeName AS Discipline, ath.PersonName AS Competitor
	MATCH (cntry:Country)<-[r:REPRESENTS]-(ath:Athlete {PersonName: Competitor})-[att:ATTENDS]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[oc:OCCURS_IN]->(yr:Year)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType {CompTypeName: Discipline})
	WHERE yr.YearName in [2025]
	RETURN ath.PersonName AS Athlete, ct.CompTypeName AS CompType, ev.EndDate AS TheDate ,att.FinishPosition AS FinPosn
	ORDER BY Athlete, CompType, TheDate ASC
	'''

	#run the queries and put the answer in dataframes
	dtf_11 = pd.DataFrame([dict(_) for _ in conn.query(query_11)])

	# add the points for each posn to the dataframe
	dtf_11['EvPoints'] = dtf_11.FinPosn.map(dtf_posn_points.set_index('Position')['points'])
	
	# cumulative sum the points per person, discipline, relies on the order by in the neo4j query
	dtf_11['CumPoints'] = dtf_11.groupby(['Athlete','CompType'])['EvPoints'].cumsum()

	#print(dtf_11)

	#generate report files

	#title="Boulder"

	dtfb_final.to_csv('athlete_stats_bouder_female.csv', header=True, index=True)
	dtmb_final.to_csv('athlete_stats_bouder_male.csv', header=True, index=True)
	dtf_data3.to_csv('boulder_wins_by_athlete_by_country.csv', header=True, index=True)

	#title="Lead"

	dtfl_final.to_csv('athlete_stats_lead_female.csv', header=True, index=True)
	dtml_final.to_csv('athlete_stats_lead_male.csv', header=True, index=True)
	dtf_data4.to_csv('lead_wins_by_athlete_by_country.csv', header=True, index=True)	  

	#title="Speed"

	dtfs_final.to_csv('athlete_stats_speed_female.csv', header=True, index=True)
	dtms_final.to_csv('athlete_stats_speed_male.csv', header=True, index=True)
	dtf_data5.to_csv('speed_wins_by_athlete_by_country.csv', header=True, index=True)	  

	#title="All disciplines"

	dtfa_final.to_csv('athlete_stats_all_disciplines_female.csv', header=True, index=True)
	dtma_final.to_csv('athlete_stats_all_disciplines_male.csv', header=True, index=True)
	dtf_5_trim.to_csv('athlete_stats_all_disciplines.csv', header=True, index=True)

	# output the barchart race file
	dtf_11.to_csv('series_barchart_race.csv', header=True, index=True)

	#
	# how to close the connection to the database
	#
	conn.close()
	print("thanks for all the fish")




