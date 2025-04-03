import streamlit as st
import pandas as pd

df_num_attend_female_boulder = pd.read_csv('EuroChamps/report_files/Number_of_Boulder_European_Champs_attended_female_Top_20.csv')
df_num_attend_male_boulder = pd.read_csv('EuroChamps/report_files/Number_of_Boulder_European_Champs_attended_male_Top_20.csv')
df_num_attend_female_lead = pd.read_csv('EuroChamps/report_files/Number_of_Lead_European_Champs_attended_female_Top_20.csv')
df_num_attend_male_lead = pd.read_csv('EuroChamps/report_files/Number_of_Lead_European_Champs_attended_male_Top_20.csv')
df_num_attend_female_speed = pd.read_csv('EuroChamps/report_files/Number_of_Speed_European_Champs_attended_female_Top_20')
df_num_attend_male_speed = pd.read_csv('EuroChamps/report_files/Number_of_Speed_European_Champs_attended_male_Top_20.csv')
df_num_attend_female_combined = pd.read_csv('EuroChamps/report_files/Number_of_combined_European_Champs_attended_female_Top_20.csv')
df_num_attend_male_combined = pd.read_csv('EuroChamps/report_files/Number_of_combined_European_Champs_attended_male_Top_20.csv')
df_num_attend_female_boulder_lead = pd.read_csv('EuroChamps/report_files/Number_of_Boulder_Lead_European_Champs_attended_female_Top_20.csv')
df_num_attend_male_boulder_lead = pd.read_csv('EuroChamps/report_files/Number_of_Boulder_Lead_European_Champs_attended_male_Top_20.csv')
df_num_attend_female_all_disciplines = pd.read_csv('EuroChamps/report_files/Number_of_all_disciplines_European_Champs_attended_female_Top_20.csv')
df_num_attend_male_all_disciplines = pd.read_csv('EuroChamps/report_files/Number_of_all_disciplines_European_Champs_attended_male_Top_20.csv')

df_num_attend_female_boulder.index = df_num_attend_female_boulder.index + 1
df_num_attend_male_boulder.index = df_num_attend_male_boulder.index + 1
df_num_attend_female_lead.index = df_num_attend_female_lead.index + 1
df_num_attend_male_lead.index = df_num_attend_male_lead.index + 1
df_num_attend_female_speed.index = df_num_attend_female_speed.index + 1
df_num_attend_male_speed.index = df_num_attend_male_speed.index + 1
df_num_attend_female_combined.index = df_num_attend_female_combined.index + 1
df_num_attend_male_combined.index = df_num_attend_male_combined.index + 1
df_num_attend_female_boulder_lead.index = df_num_attend_female_boulder_lead.index + 1
df_num_attend_male_boulder_lead.index = df_num_attend_male_boulder_lead.index + 1
df_num_attend_female_all_disciplines.index = df_num_attend_female_all_disciplines.index + 1
df_num_attend_male_all_disciplines.index = df_num_attend_male_all_disciplines.index + 1

st.set_page_config(
    page_title="Athlete Participation Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("Athlete Participation Statistics")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs (["Boulder","Lead","Speed","Combined","Boulder Lead","All disciplines"])

with tab1:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_num_attend_female_boulder,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_num_attend_male_boulder,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab2:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_num_attend_female_lead,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_num_attend_male_lead,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab3:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_num_attend_female_speed,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_num_attend_male_speed,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab4:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_num_attend_female_combined,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_num_attend_male_combined,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab5:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_num_attend_female_boulder_lead,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_num_attend_male_boulder_lead,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab6:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_num_attend_female_all_disciplines,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
	with col2:
		st.dataframe (df_num_attend_male_all_disciplines,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
st.divider ()

st.caption("# You can sort any of the tables by clicking on the column header and choosing the sort direction")

