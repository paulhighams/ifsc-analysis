import streamlit as st
import pandas as pd

df_euro_champs = pd.read_csv('EuroChamps/report_files/List_of_European_Championships.csv')
df_country_count = pd.read_csv('EuroChamps/report_files/Num_of_Countries_at_European_Championships.csv')
df_athlete_count = pd.read_csv('EuroChamps/report_files/Num_of_Athletes_at_European_Championships.csv')

st.set_page_config(
    page_title="Country and Event Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("Country and Event Statistics")

col1, col2, col3 = st.columns([4, 1, 1])
with col1:
	st.caption(":blue[European Championship event details]")
	st.dataframe (df_euro_champs, height=850, width=1300, hide_index=True)
with col2:
	st.caption(":blue[Number of countries per event]")
	st.dataframe (df_country_count, height=700, hide_index=True)
with col3:
	st.caption(":blue[Number of athletes per event]")
	st.dataframe (df_athlete_count, height=700, hide_index=True)

st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")
