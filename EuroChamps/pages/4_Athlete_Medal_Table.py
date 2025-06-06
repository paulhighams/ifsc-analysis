import streamlit as st
import pandas as pd
#import os


#current_dir = os.getcwd()

#import the data files
df_Boulder_wins_and_podiums_female = pd.read_csv("EuroChamps/report_files/European_Championship_Boulder_wins_and_podiums_female.csv")
df_Boulder_wins_and_podiums_male = pd.read_csv("EuroChamps/report_files/European_Championship_Boulder_wins_and_podiums_male.csv")
df_Lead_wins_and_podiums_female = pd.read_csv("EuroChamps/report_files/European_Championship_Lead_wins_and_podiums_female.csv")
df_Lead_wins_and_podiums_male = pd.read_csv("EuroChamps/report_files/European_Championship_Lead_wins_and_podiums_male.csv")
df_Speed_wins_and_podiums_female = pd.read_csv("EuroChamps/report_files/European_Championship_Speed_wins_and_podiums_female.csv")
df_Speed_wins_and_podiums_male = pd.read_csv("EuroChamps/report_files/European_Championship_Speed_wins_and_podiums_male.csv")
df_Combined_wins_and_podiums_female = pd.read_csv("EuroChamps/report_files/European_Championship_combined_wins_and_podiums_female.csv")
df_Combined_wins_and_podiums_male = pd.read_csv("EuroChamps/report_files/European_Championship_combined_wins_and_podiums_male.csv")
df_Boulder_Lead_wins_and_podiums_female = pd.read_csv("EuroChamps/report_files/European_Championship_Boulder_Lead_wins_and_podiums_female.csv")
df_Boulder_Lead_wins_and_podiums_male = pd.read_csv("EuroChamps/report_files/European_Championship_Boulder_Lead_wins_and_podiums_male.csv")
df_All_Disciplines_wins_and_podiums_female = pd.read_csv("EuroChamps/report_files/European_Championship_all_disciplines_wins_and_podiums_female.csv")
df_All_Disciplines_wins_and_podiums_male = pd.read_csv("EuroChamps/report_files/European_Championship_all_disciplines_wins_and_podiums_male.csv")

#set indexes
df_Boulder_wins_and_podiums_female.index = df_Boulder_wins_and_podiums_female.index + 1
df_Boulder_wins_and_podiums_male.index = df_Boulder_wins_and_podiums_male.index + 1
df_Lead_wins_and_podiums_female.index = df_Lead_wins_and_podiums_female.index + 1
df_Lead_wins_and_podiums_male.index = df_Lead_wins_and_podiums_male.index + 1
df_Speed_wins_and_podiums_female.index = df_Speed_wins_and_podiums_female.index + 1
df_Speed_wins_and_podiums_male.index = df_Speed_wins_and_podiums_male.index + 1
df_Combined_wins_and_podiums_female.index = df_Combined_wins_and_podiums_female.index + 1
df_Combined_wins_and_podiums_male.index = df_Combined_wins_and_podiums_male.index + 1
df_Boulder_Lead_wins_and_podiums_female.index = df_Boulder_Lead_wins_and_podiums_female.index + 1
df_Boulder_Lead_wins_and_podiums_male.index = df_Boulder_Lead_wins_and_podiums_male.index + 1
df_All_Disciplines_wins_and_podiums_female.index = df_All_Disciplines_wins_and_podiums_female.index + 1
df_All_Disciplines_wins_and_podiums_male.index = df_All_Disciplines_wins_and_podiums_male.index + 1

st.set_page_config(
    page_title="European Championships - Athlete Medal Table",
    page_icon=":person_climbing:",
	layout="wide",
)

st.header ("Athlete wins and Podiums by discipline")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs (["Boulder","Lead","Speed","Combined","Boulder Lead","All disciplines"])

with tab1:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Boulder_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	with col2:
		st.dataframe (df_Boulder_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
with tab2:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Lead_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	with col2:
		st.dataframe (df_Lead_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
with tab3:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Speed_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	with col2:
		st.dataframe (df_Speed_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
with tab4:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Combined_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		hide_index=True)
	with col2:
		st.dataframe (df_Combined_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		hide_index=True)
with tab5:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Boulder_Lead_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		hide_index=True)
	with col2:
		st.dataframe (df_Boulder_Lead_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		hide_index=True)
with tab6:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_All_Disciplines_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	with col2:
		st.dataframe (df_All_Disciplines_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)

st.divider ()
st.write("# You can sort any of the tables by clicking on the column header and choosing the sort direction")
#st.write ('working:', current_dir)
