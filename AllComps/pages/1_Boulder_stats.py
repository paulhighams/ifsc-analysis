import streamlit as st
import pandas as pd
import plotly.express as px

df_Female_athlete_stats = pd.read_csv('AllComps/report_files/athlete_stats_bouder_female.csv')
df_Male_athlete_stats = pd.read_csv('AllComps/report_files/athlete_stats_bouder_male.csv')
df_wins_by_athlete_by_country = pd.read_csv('AllComps/report_files/boulder_wins_by_athlete_by_country.csv')
df_last_3_years_world_cups = pd.read_csv('AllComps/report_files/last_3_years_world_cups_boulder.csv') 
df_last_3_years_world_champs = pd.read_csv('AllComps/report_files/last_3_years_world_champs_boulder.csv') 

# set the indexes to start at 1
df_Female_athlete_stats.index = df_Female_athlete_stats.index + 1
df_Male_athlete_stats.index = df_Male_athlete_stats.index + 1
df_last_3_years_world_cups.index = df_last_3_years_world_cups.index + 1
df_last_3_years_world_champs.index = df_last_3_years_world_champs.index + 1

# generate graphs
pic1 = px.treemap(df_wins_by_athlete_by_country,path=['Nation','Winner'],
			values='Wins',
			color='WinPercent',
			color_continuous_scale='RdBu')


st.set_page_config(
    page_title="Boulder Athlete Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("Boulder Athlete Statistics")

tab1, tab2, tab3, tab4 = st.tabs (["Female Career Stats","Male Career Stats","Athlete wins graphic","Last 3 years World cups and Championships Podiums"])

with tab1:
	st.dataframe (df_Female_athlete_stats,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	st.caption(":blue[The ranking is based on WC Series wins, then WChamp Golds, then WCup wins]")

with tab2:
	st.dataframe (df_Male_athlete_stats,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	st.caption(":blue[The ranking is based on WC Series wins, then WChamp Golds, then WCup wins]")
with tab3:
	st.plotly_chart (pic1)
with tab4:
	st.dataframe (df_last_3_years_world_cups,
		column_config={
			"Gender": st.column_config.Column(""),
			"Unnamed: 1": st.column_config.Column("Start Date"),
			"Unnamed: 2": st.column_config.Column("Event"),
			"Female": st.column_config.Column("Female 1st"),
			"Female.1": st.column_config.Column("2nd"),
			"Female.2": st.column_config.Column("3rd"),
			"Male": st.column_config.Column("Male 1st"),
			"Male.1": st.column_config.Column("2nd"),
			"Male.2": st.column_config.Column("3rd"),
		},
		height=750, hide_index=True)
	st.dataframe (df_last_3_years_world_champs,
		column_config={
			"Gender": st.column_config.Column("Start Date"),
			"Unnamed: 1": st.column_config.Column("Event"),
			"Female": st.column_config.Column("Female 1st"),
			"Female.1": st.column_config.Column("2nd"),
			"Female.2": st.column_config.Column("3rd"),
			"Male": st.column_config.Column("Male 1st"),
			"Male.1": st.column_config.Column("2nd"),
			"Male.2": st.column_config.Column("3rd"),
		},
		height=300, hide_index=True)


st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")
