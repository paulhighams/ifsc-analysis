import streamlit as st
import pandas as pd

df_latest_comps = pd.read_csv('WorldChamps/report_files/latest_comps.csv')
df_world_champs = df_latest_comps[df_latest_comps['theEventType'] == 'World Championship']

st.set_page_config(
    page_title="World Championships",
    page_icon="👋",
	layout="centered"
)

st.write("# Welcome to statistics about the World Championships for sport Climbing! :person_climbing:")

st.sidebar.success("Select an analysis above.")

st.subheader ("Latest event results included")

st.dataframe (df_world_champs, height=300, width=1300, hide_index=True)

st.markdown(
    """
    On the menu on the left are a set of statistics organised by topic. Within each topic you will find multiple tabs
    **👈 Pick a category and get started
    ### For all the tables of data the buttons on the top right allow you to:
    - Download the table as a csv
    - Search for a value within the table
    - Make the table fullscreen
    ### If you want to change the order of the table
    - Click on the column header of the column you wish to sort on
    - Click once for ascending order, and click again for descending order
"""
)