import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# import the files
df_boulder_medals = pd.read_csv('WorldCups/report_files/World_Cups_Medal_Table_for_Boulder.csv')
df_lead_medals = pd.read_csv('WorldCups/report_files/World_Cups_Medal_Table_for_Lead.csv')
df_speed_medals = pd.read_csv('WorldCups/report_files/World_Cups_Medal_Table_for_Speed.csv')
df_all_medals= pd.read_csv('WorldCups/report_files/World_Cups_Medal_Table_for_All_disciplines.csv')

df_boulder_num_athletes = pd.read_csv('WorldCups/report_files/Number_of_athletes_per_Country_with_World_Cup_wins_and_podiums_for_Boulder.csv')
df_lead_num_athletes = pd.read_csv('WorldCups/report_files/Number_of_athletes_per_Country_with_World_Cup_wins_and_podiums_for_Lead.csv')
df_speed_num_athletes = pd.read_csv('WorldCups/report_files/Number_of_athletes_per_Country_with_World_Cup_wins_and_podiums_for_Speed.csv')
df_all_num_athletes = pd.read_csv('WorldCups/report_files/Number_of_athletes_per_Country_with_World_Cup_wins_and_podiums_all_disciplines.csv')
df_boulder_lock_out = pd.read_csv('WorldCups/report_files/Country_lock_out_of_the_podium_in_boulder_World_Cup_and_World_Champs.csv')
df_lead_lock_out = pd.read_csv('WorldCups/report_files/Country_lock_out_of_the_podium_in_lead_World_Cup_and_World_Champs.csv')
df_series_best = pd.read_csv('WorldCups/report_files/World_Cup_Series_best_ever_performance_by_gender_and_discipline.csv')

#create the plots

# streamlit stuff

st.set_page_config(
    page_title="Country World Cup Medal Table",
    page_icon="👋",
	layout="wide",
)

st.header ("Country World Cup Medal Table")

tab1, tab2, tab3, tab4 = st.tabs (["World Cup country medal tables",
    "Number of athletes by Country with World Cup wins and podiums",
    "Podium lockouts",
    "All discplines World Cup events attended"])

with tab1:
	col1, col2 = st.columns([1, 1])
	with col1:
		st.caption(":blue[Boulder World Cup country medal table]")
		st.dataframe (df_boulder_medals,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, width=1300, hide_index=True)
		st.caption(":blue[Lead World Cup country medal table]")
		st.dataframe (df_lead_medals,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, width=1300, hide_index=True)
	with col2:
		st.caption(":blue[Speed World Cup country medal table]")
		st.dataframe (df_speed_medals,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, width=1300, hide_index=True)
		st.caption(":blue[All disciplines World Cup country medal table]")
		st.dataframe (df_all_medals,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, width=1300, hide_index=True)
with tab2:
	col1, col2 = st.columns([1, 1])
	with col1:
	    st.caption(":blue[Boulder: Number of athletes by Country with World Cup wins and podiums]")
	    st.dataframe (df_boulder_num_athletes,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=700, width=1300, hide_index=True)
	    st.caption(":blue[Lead: Number of athletes by Country with World Cup wins and podiums]")
	    st.dataframe (df_lead_num_athletes,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=700, width=1300, hide_index=True)
	with col2:
	    st.caption(":blue[Speed: Number of athletes by Country with World Cup wins and podiums]")
	    st.dataframe (df_speed_num_athletes,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=700, width=1300, hide_index=True)
	    st.caption(":blue[All disciplines: Number of athletes by Country with World Cup wins and podiums]")
	    st.dataframe (df_all_num_athletes,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=700, width=1300, hide_index=True)
with tab3:
    col1, col2 = st.columns([1, 1])
    with col1:
	    st.caption(":blue[Boulder Podium lockouts]")
	    st.dataframe (df_boulder_lock_out,
			column_order=("Country","CompType","WCupComp","Athletes"),
			height=750, width=1300, hide_index=True)
    with col2:
	    st.caption(":blue[Lead Podium lockouts]")
	    st.dataframe (df_lead_lock_out,
			column_order=("Country","CompType","WCupComp","Athletes"),
			height=750, width=1300, hide_index=True)
with tab4:
	st.caption(":blue[World Cup Series best]")
	st.dataframe (df_series_best, hide_index=True)


st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")



