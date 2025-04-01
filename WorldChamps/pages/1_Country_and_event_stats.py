import streamlit as st
import pandas as pd

df_euro_champs = pd.read_csv('WorldChamps/report_files/list_of_world_championships.csv')
df_country_count = pd.read_csv('WorldChamps/report_files/Countries_competing_at_World_Championships.csv')
df_athlete_count = pd.read_csv('WorldChamps/report_files/Athletes_competing_at_World_Championships.csv')
df_team_sizes = pd.read_csv('WorldChamps/report_files/20_Largest_Total_Team_size_at_World_Championships.csv')

df_team_sizes.index = df_team_sizes.index + 1

st.set_page_config(
    page_title="Country and Event Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("Country and Event Statistics")

tab1, tab2 = st.tabs (["Event details","20 largest teams at World Champs"])

with tab1:
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
	    st.caption(":blue[World Championship event details]")
	    st.dataframe (df_euro_champs,
			column_order=("Country","EventName","Start","Finish","Venue","NumComps"),
			height=800, hide_index=True)
    with col2:
	    st.caption(":blue[Number of countries per event]")
	    st.dataframe (df_country_count,
			column_order=("Event","NumCountries"),
			height=800, hide_index=True)
    with col3:
	    st.caption(":blue[Number of athletes per event]")
	    st.dataframe (df_athlete_count,
			column_order=("Event","NumAthletes","Boulder","Lead","Speed","Boulder-Lead","Combined"),
			height=800, hide_index=True)
with tab2:
    st.dataframe (df_team_sizes,
			column_order=("_index","Event","TotalTeam"),
			column_config={ "_index": st.column_config.Column("ranking")},
			height=800)

st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")
