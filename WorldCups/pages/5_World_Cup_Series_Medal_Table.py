import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# import the files
df_boulder_medals = pd.read_csv('WorldCups/report_files/World_Cup_Series_Medal_Table_for_Boulder.csv')
df_lead_medals = pd.read_csv('WorldCups/report_files/World_Cup_Series_Medal_Table_for_Lead.csv')
df_speed_medals = pd.read_csv('WorldCups/report_files/World_Cup_Series_Medal_Table_for_Speed.csv')
df_all_medals = pd.read_csv('WorldCups/report_files/World_Cup_Series_Medal_Table_all_Disciplines.csv')
df_boulder_list = pd.read_csv('WorldCups/report_files/World_Cup_Series_Boulder_podium_list_male_and_female.csv')
df_lead_list = pd.read_csv('WorldCups/report_files/World_Cup_Series_Lead_podium_list_male_and_female.csv')
df_speed_list = pd.read_csv('WorldCups/report_files/World_Cup_Series_Speed_podium_list_male_and_female.csv')

#create the plots

# streamlit stuff

st.set_page_config(
    page_title="Country World Cup Series Medal Table",
    page_icon="👋",
	layout="wide",
)

st.header ("Country World Cup Series Medal Table")

tab1, tab2 = st.tabs (["World Cup series medal tables",
    "World Cup Series podium list"])

with tab1:
	col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
	with col1:
	    st.caption(":blue[Boulder World Cup series medal table]")
	    st.dataframe (df_boulder_medals,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, width=400, hide_index=True)
	with col2:
	    st.caption(":blue[Lead World Cup series medal table]")
	    st.dataframe (df_lead_medals,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, width=400, hide_index=True)
	with col3:
	    st.caption(":blue[Speed World Cup series medal table]")
	    st.dataframe (df_speed_medals,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, width=400, hide_index=True)
	with col4:
	    st.caption(":blue[All disciplines World Cup series medal table]")
	    st.dataframe (df_all_medals,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, width=400, hide_index=True)
with tab2:
	    st.caption(":blue[Boulder: World Cup Series wins and podiums male and female]")
	    st.dataframe (df_boulder_list, height=500, hide_index=True)
	    st.caption(":blue[Lead: World Cup Series wins and podiums male and female]")
	    st.dataframe (df_lead_list, height=500, hide_index=True)
	    st.caption(":blue[Speed: World Cup Series wins and podiums male and female]")
	    st.dataframe (df_speed_list, height=500, hide_index=True)

st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")



