import streamlit as st
import pandas as pd
#import os


#current_dir = os.getcwd()

#import the data files
df_Boulder_wins_and_podiums_female = pd.read_csv("WorldChamps/report_files/World_Championship_Boulder_wins_and_podiums_female.csv")
df_Boulder_wins_and_podiums_male = pd.read_csv("WorldChamps/report_files/World_Championship_Boulder_wins_and_podiums_male.csv")
df_Lead_wins_and_podiums_female = pd.read_csv("WorldChamps/report_files/World_Championship_Lead_wins_and_podiums_female.csv")
df_Lead_wins_and_podiums_male = pd.read_csv("WorldChamps/report_files/World_Championship_Lead_wins_and_podiums_male.csv")
df_Speed_wins_and_podiums_female = pd.read_csv("WorldChamps/report_files/World_Championship_Speed_wins_and_podiums_female.csv")
df_Speed_wins_and_podiums_male = pd.read_csv("WorldChamps/report_files/World_Championship_Speed_wins_and_podiums_male.csv")
df_Combined_wins_and_podiums_female = pd.read_csv("WorldChamps/report_files/World_Championship_Combined_wins_and_podiums_female.csv")
df_Combined_wins_and_podiums_male = pd.read_csv("WorldChamps/report_files/World_Championship_Combined_wins_and_podiums_male.csv")
df_Boulder_Lead_wins_and_podiums_female = pd.read_csv("WorldChamps/report_files/World_Championship_BoulderLead_wins_and_podiums_female.csv")
df_Boulder_Lead_wins_and_podiums_male = pd.read_csv("WorldChamps/report_files/World_Championship_BoulderLead_wins_and_podiums_male.csv")
df_All_Disciplines_wins_and_podiums_female = pd.read_csv("WorldChamps/report_files/World_Championship_all_disciplines_wins_and_podiums_female.csv")
df_All_Disciplines_wins_and_podiums_male = pd.read_csv("WorldChamps/report_files/World_Championship_all_disciplines_wins_and_podiums_male.csv")
df_Boulder_podium_list_male_and_female = pd.read_csv('WorldChamps/report_files/World_Championship_Boulder_podium_list_male_and_female.csv')
df_Lead_podium_list_male_and_female = pd.read_csv('WorldChamps/report_files/World_Championship_Lead_podium_list_male_and_female.csv')
df_Speed_podium_list_male_and_female = pd.read_csv('WorldChamps/report_files/World_Championship_Speed_podium_list_male_and_female.csv')
df_youngest_athletes = pd.read_csv('WorldChamps/report_files/World_Championship_youngest_athletes.csv')
df_oldest_athletes = pd.read_csv('WorldChamps/report_files/World_Championship_oldest_athletes.csv')

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
df_Boulder_podium_list_male_and_female.index = df_Boulder_podium_list_male_and_female.index + 1
df_Lead_podium_list_male_and_female.index = df_Lead_podium_list_male_and_female.index + 1
df_Speed_podium_list_male_and_female.index = df_Speed_podium_list_male_and_female.index + 1

st.set_page_config(
    page_title="World Championships - Athlete Medal Table",
    page_icon=":person_climbing:",
	layout="wide",
)

st.header ("Athlete wins and Podiums by discipline")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs (["Boulder","Lead","Speed","Combined","Boulder Lead","All disciplines", "Youngest and oldest Athletes"])

with tab1:
	col1, col2 = st.columns(2)
	col1.dataframe (df_Boulder_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	col2.dataframe (df_Boulder_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	col1.dataframe (df_Boulder_podium_list_male_and_female,
		column_config={
			"Gender": st.column_config.Column(""),
			"Female.1": st.column_config.Column(""),
			"Female.2": st.column_config.Column(""),
			"Male.1": st.column_config.Column(""),
			"Male.2": st.column_config.Column("")
		},
		height=600, width=1300, hide_index=True)
with tab2:
	col1, col2 = st.columns(2)
	col1.dataframe (df_Lead_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	col2.dataframe (df_Lead_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	col1.dataframe (df_Lead_podium_list_male_and_female,
		column_config={
			"Gender": st.column_config.Column(""),
			"Female.1": st.column_config.Column(""),
			"Female.2": st.column_config.Column(""),
			"Male.1": st.column_config.Column(""),
			"Male.2": st.column_config.Column("")
		},
		height=600, width=1300, hide_index=True)
with tab3:
	col1, col2 = st.columns(2)
	col1.dataframe (df_Speed_wins_and_podiums_female,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	col2.dataframe (df_Speed_wins_and_podiums_male,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	col1.dataframe (df_Speed_podium_list_male_and_female,
		column_config={
			"Gender": st.column_config.Column(""),
			"Female.1": st.column_config.Column(""),
			"Female.2": st.column_config.Column(""),
			"Male.1": st.column_config.Column(""),
			"Male.2": st.column_config.Column("")
		},
		height=600, width=1300, hide_index=True)
with tab4:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Combined_wins_and_podiums_female,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=600, hide_index=True)
	with col2:
		st.dataframe (df_Combined_wins_and_podiums_male,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=600, hide_index=True)
with tab5:
	col1, col2 = st.columns(2)
	with col1:
		st.dataframe (df_Boulder_Lead_wins_and_podiums_female,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=400, hide_index=True)
	with col2:
		st.dataframe (df_Boulder_Lead_wins_and_podiums_male,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=400, hide_index=True)
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
with tab7:
	st.subheader("Youngest athletes in World Championships :blue[(winners and podiums are 99.5% complete, for finalists and attends there are some athletes without a D.O.B)]")
	st.dataframe (df_youngest_athletes,
		column_order=("Discipline","Gender","Winner","Podium","Finalist","Attendee"),
		height=400, width=2000)
	st.subheader("Oldest athletes in World Championships  :blue[(winners and podiums are 99.5% complete, for finalists and attends there are some athletes without a D.O.B)]")
	st.dataframe (df_oldest_athletes,
		column_order=("Discipline","Gender","Winner","Podium","Finalist","Attendee"),
		height=400, width=2000)
    
st.divider ()
st.write("# You can sort any of the tables by clicking on the column header and choosing the sort direction")
#st.write ('working:', current_dir)
