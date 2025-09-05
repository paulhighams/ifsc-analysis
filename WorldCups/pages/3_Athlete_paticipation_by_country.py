import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# import the files
df_boulder_female = pd.read_csv('WorldCups/report_files/Number_of_Boulder_World_Cups_attended_by_Country_female_Top_3.csv')
df_boulder_male = pd.read_csv('WorldCups/report_files/Number_of_Boulder_World_Cups_attended_by_Country_male_Top_3.csv')
df_lead_female = pd.read_csv('WorldCups/report_files/Number_of_Lead_World_Cups_attended_by_Country_female_Top_3.csv')
df_lead_male = pd.read_csv('WorldCups/report_files/Number_of_Lead_World_Cups_attended_by_Country_male_Top_3.csv')
df_speed_female = pd.read_csv('WorldCups/report_files/Number_of_Speed_World_Cups_attended_by_Country_female_Top_3.csv')
df_speed_male = pd.read_csv('WorldCups/report_files/Number_of_Speed_World_Cups_attended_by_Country_male_Top_3.csv')
df_all_female = pd.read_csv('WorldCups/report_files/Number_of_all_disciplines_World_Cups_attended_by_Country_female_Top_3.csv')
df_all_male = pd.read_csv('WorldCups/report_files/Number_of_all_disciplines_World_Cups_attended_by_Country_male_Top_3.csv')

#increment the indexes
df_boulder_female.index = df_boulder_female.index + 1
df_boulder_male.index = df_boulder_male.index + 1
df_lead_female.index = df_lead_female.index + 1
df_lead_male.index = df_lead_male.index + 1
df_speed_female.index = df_speed_female.index + 1
df_speed_male.index = df_speed_male.index + 1
df_all_female.index = df_all_female.index + 1
df_all_male.index = df_all_male.index + 1

# streamlit stuff

st.set_page_config(
    page_title="Athlete participation by Country Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("Athlete participation Statistics")
st.subheader (":blue[this only has a subset of countries where there are active athletes - use the Athlete Participation Global option for global rankings]", divider=True)

tab1, tab2, tab3, tab4 = st.tabs (["Boulder World Cup events attended",
    "Lead World Cup events attended",
    "Speed World Cup events attended",
    "All discplines World Cup events attended"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
	    st.caption(":blue[Boulder World Cup events attended]")
	    st.dataframe (df_boulder_female,
			column_order=("_index","Athlete","Country","NumWCups"),
			column_config={ "_index": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=False)
    with col2:
	    st.caption(":blue[Boulder World Cup events attended]")
	    st.dataframe (df_boulder_male,
			column_order=("_index","Athlete","Country","NumWCups"),
			column_config={ "_index": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=False)
with tab2:
    col1, col2 = st.columns([1, 1])
    with col1:
	    st.caption(":blue[Lead World Cup events attended]")
	    st.dataframe (df_lead_female,
			column_order=("_index","Athlete","Country","NumWCups"),
			column_config={ "_index": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=False)
    with col2:
	    st.caption(":blue[Lead World Cup events attended]")
	    st.dataframe (df_lead_male,
			column_order=("_index","Athlete","Country","NumWCups"),
			column_config={ "_index": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=False)
with tab3:
    col1, col2 = st.columns([1, 1])
    with col1:
	    st.caption(":blue[Speed World Cup events attended]")
	    st.dataframe (df_speed_female,
			column_order=("_index","Athlete","Country","NumWCups"),
			column_config={ "_index": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=False)
    with col2:
	    st.caption(":blue[Speed World Cup events attended]")
	    st.dataframe (df_speed_male,
			column_order=("_index","Athlete","Country","NumWCups"),
			column_config={ "_index": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=False)
with tab4:
	col1, col2 = st.columns([1, 1])
	with col1:
		st.caption(":blue[All disciplines World Cup events attended]")
		st.dataframe (df_all_female,
		column_order=("_index","Athlete","Country","NumWCups"),
		column_config={ "_index": st.column_config.Column("ranking")},
		height=850, width=1300, hide_index=False)
	with col2:
		st.caption(":blue[All disciplines World Cup events attended]")
		st.dataframe (df_all_male,
			column_order=("_index","Athlete","Country","NumWCups"),
			column_config={ "_index": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=False)

st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")



