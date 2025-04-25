#calculate the latest comps for information
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
	MATCH (ath:Athlete)-[win:WINNER]->(cmp:Competition)<-[cs:CONSISTS_OF]-(ev:Event)-[:IDENTIFIED_BY]->(e:EventType)
	MATCH (cmp:Competition)<-[cl:CLASSIFIES]-(ct:CompType)
	WHERE ath IS NOT NULL
	WITH e.EventTypeName as theEventTypeName, ct.CompTypeName AS theCompTypeName, MAX(ev.StartDate) AS theMaxStart
	MATCH (cmp2:Competition)<-[cs2:CONSISTS_OF]-(ev2:Event {StartDate: theMaxStart})-[:IDENTIFIED_BY]->(e2:EventType {EventTypeName: theEventTypeName})
	MATCH (cmp2:Competition)<-[cl2:CLASSIFIES]-(ct2:CompType {CompTypeName: theCompTypeName})
	RETURN DISTINCT e2.EventTypeName AS theEventType, ct2.CompTypeName AS theDiscipline, ev2.EventName AS theEventName

	'''
	df_latest_events = pd.DataFrame([dict(_) for _ in conn.query(query_string3)])

	df_latest_events.to_csv('../AllComps/report_files/latest_comps.csv', header=True, index=False)
	df_latest_events.to_csv('../EuroChamps/report_files/latest_comps.csv', header=True, index=False)
	df_latest_events.to_csv('../WorldChamps/report_files/latest_comps.csv', header=True, index=False)
	df_latest_events.to_csv('../WorldCups/report_files/latest_comps.csv', header=True, index=False)
		#
	# how to close the connection to the database
	#
	conn.close()
	print("thanks for all the fish")

