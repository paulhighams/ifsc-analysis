import streamlit as st
import pandas as pd

df_Medal_Table_for_Boulder = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_Boulder.csv')
df_Medal_Table_for_Lead = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_Lead.csv')
df_Medal_Table_for_Speed = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_Speed.csv')
df_Medal_Table_for_Combined = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_Combined.csv')
df_Medal_Table_for_BoulderLead = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_BoulderLead.csv')
df_Medal_Table_for_All_disciplines = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_All_disciplines.csv')
df_athlete_wins_and_podiums_for_Boulder = pd.read_csv('WorldChamps/report_files/Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_Boulder.csv')
df_athlete_wins_and_podiums_for_Lead = pd.read_csv('WorldChamps/report_files/Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_Lead.csv')
df_athlete_wins_and_podiums_for_Speed = pd.read_csv('WorldChamps/report_files/Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_Speed.csv')
df_athlete_wins_and_podiums_for_Combined = pd.read_csv('WorldChamps/report_files/Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_Combined.csv')
df_athlete_wins_and_podiums_for_BoulderLead = pd.read_csv('WorldChamps/report_files/Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_for_BoulderLead.csv')
df_athlete_wins_and_podiums_for_all_disciplines = pd.read_csv('WorldChamps/report_files/Number_of_athletes_per_Country_with_World_Championship_wins_and_podiums_all_disciplines.csv')
df_Country_best_finishes_by_gender_and_discipline = pd.read_csv('WorldChamps/report_files/Country_best_finishes_by_gender_and_discipline.csv')

#update the indexes
df_Medal_Table_for_Boulder.index = df_Medal_Table_for_Boulder.index + 1
df_Medal_Table_for_Lead.index = df_Medal_Table_for_Lead.index + 1
df_Medal_Table_for_Speed.index = df_Medal_Table_for_Speed.index + 1
df_Medal_Table_for_Combined.index = df_Medal_Table_for_Combined.index + 1
df_Medal_Table_for_BoulderLead.index = df_Medal_Table_for_BoulderLead.index + 1
df_Medal_Table_for_All_disciplines.index = df_Medal_Table_for_All_disciplines.index + 1
df_athlete_wins_and_podiums_for_Boulder.index = df_athlete_wins_and_podiums_for_Boulder.index + 1
df_athlete_wins_and_podiums_for_Lead.index = df_athlete_wins_and_podiums_for_Lead.index + 1
df_athlete_wins_and_podiums_for_Speed.index = df_athlete_wins_and_podiums_for_Speed.index + 1
df_athlete_wins_and_podiums_for_Combined.index = df_athlete_wins_and_podiums_for_Combined.index + 1
df_athlete_wins_and_podiums_for_BoulderLead.index = df_athlete_wins_and_podiums_for_BoulderLead.index + 1
df_athlete_wins_and_podiums_for_all_disciplines.index = df_athlete_wins_and_podiums_for_all_disciplines.index + 1
df_Country_best_finishes_by_gender_and_discipline.index = df_Country_best_finishes_by_gender_and_discipline.index + 1

st.set_page_config(
    page_title="Country Results",
    page_icon="👋",
	layout="wide",
)

st.header ("Country Results")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs (["Boulder","Lead","Speed","Combined","Boulder Lead","All disciplines","Country best finish by an athlete"])

with tab1:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Medal_Table_for_Boulder,
			column_order=("WChampEvent","Country","Discipline","Gold","Silver","Bronze","Total"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_athlete_wins_and_podiums_for_Boulder,
			column_order=("Country","Discipline","NumAthleteswithWChampWins","NumAthleteswithWChampPodiums"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab2:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Medal_Table_for_Lead,
			column_order=("WChampEvent","Country","Discipline","Gold","Silver","Bronze","Total"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_athlete_wins_and_podiums_for_Lead,
			column_order=("Country","Discipline","NumAthleteswithWChampWins","NumAthleteswithWChampPodiums"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab3:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Medal_Table_for_Speed,
			column_order=("WChampEvent","Country","Discipline","Gold","Silver","Bronze","Total"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_athlete_wins_and_podiums_for_Speed,
			column_order=("Country","Discipline","NumAthleteswithWChampWins","NumAthleteswithWChampPodiums"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab4:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Medal_Table_for_Combined,
			column_order=("WChampEvent","Country","Discipline","Gold","Silver","Bronze","Total"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_athlete_wins_and_podiums_for_Combined,
			column_order=("Country","Discipline","NumAthleteswithWChampWins","NumAthleteswithWChampPodiums"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab5:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Medal_Table_for_BoulderLead,
			column_order=("WChampEvent","Country","Discipline","Gold","Silver","Bronze","Total"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=400)
	with col2:
		st.dataframe (df_athlete_wins_and_podiums_for_BoulderLead,
			column_order=("Country","Discipline","NumAthleteswithWChampWins","NumAthleteswithWChampPodiums"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=400, hide_index=True)
with tab6:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Medal_Table_for_All_disciplines,
			column_order=("WChampEvent","Country","Gold","Silver","Bronze","Total"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_athlete_wins_and_podiums_for_all_disciplines,
			column_order=("Country","NumAthleteswithWChampWins","NumAthleteswithWChampPodiums"),
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab7:
    st.dataframe (df_Country_best_finishes_by_gender_and_discipline, height=800, hide_index=True)

st.divider ()

st.caption("# You can sort any of the tables by clicking on the column header and choosing the sort direction")
