import streamlit as st
import pandas as pd

df_last_3_years_world_cups = pd.read_csv('AllComps/report_files/last_3_years_world_cups_boulderlead.csv') 
df_last_3_years_world_champs = pd.read_csv('AllComps/report_files/last_3_years_world_champs_boulderlead.csv') 

# set the indexes to start at 1
df_last_3_years_world_cups.index = df_last_3_years_world_cups.index + 1
df_last_3_years_world_champs.index = df_last_3_years_world_champs.index + 1


st.set_page_config(
    page_title="Boulder Lead Athlete Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("Boulder Lead Athlete Statistics")

st.caption(":blue[Last 3 years World Cup podiums]")
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
	height=200, hide_index=True)
st.caption(":blue[Last 3 years Championship podiums]")
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
	height=600, hide_index=True)

st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")
