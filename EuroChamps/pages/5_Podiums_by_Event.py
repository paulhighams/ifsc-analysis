import streamlit as st
import pandas as pd


#import the data files
df_Lead_Podiums_by_Event_male = pd.read_csv('EuroChamps/report_files/European_Championship_Lead_Podiums_by_Event_male.csv')
df_Lead_Podiums_by_Event_female = pd.read_csv('EuroChamps/report_files/European_Championship_Lead_Podiums_by_Event_female.csv')
df_Speed_Podiums_by_Event_male = pd.read_csv('EuroChamps/report_files/European_Championship_Speed_Podiums_by_Event_male.csv')
df_Speed_Podiums_by_Event_female = pd.read_csv('EuroChamps/report_files/European_Championship_Speed_Podiums_by_Event_female.csv')
df_Boulder_Podiums_by_Event_male = pd.read_csv('EuroChamps/report_files/European_Championship_Boulder_Podiums_by_Event_male.csv')
df_Boulder_Podiums_by_Event_female = pd.read_csv('EuroChamps/report_files/European_Championship_Boulder_Podiums_by_Event_female.csv')
df_combined_Podiums_by_Event_male = pd.read_csv('EuroChamps/report_files/European_Championship_combined_Podiums_by_Event_male.csv')
df_combined_Podiums_by_Event_female = pd.read_csv('EuroChamps/report_files/European_Championship_combined_Podiums_by_Event_female.csv')
df_Boulder_Lead_Podiums_by_Event_male = pd.read_csv('EuroChamps/report_files/European_Championship_Boulder_Lead_Podiums_by_Event_male.csv')
df_Boulder_Lead_Podiums_by_Event_female = pd.read_csv('EuroChamps/report_files/European_Championship_Boulder_Lead_Podiums_by_Event_female.csv')

#set indexes
df_Lead_Podiums_by_Event_male.index = df_Lead_Podiums_by_Event_male.index + 1
df_Lead_Podiums_by_Event_female.index = df_Lead_Podiums_by_Event_female.index + 1
df_Speed_Podiums_by_Event_male.index = df_Speed_Podiums_by_Event_male.index + 1
df_Speed_Podiums_by_Event_female.index = df_Speed_Podiums_by_Event_female.index + 1
df_Boulder_Podiums_by_Event_male.index = df_Boulder_Podiums_by_Event_male.index + 1
df_Boulder_Podiums_by_Event_female.index = df_Boulder_Podiums_by_Event_female.index + 1
df_combined_Podiums_by_Event_male.index = df_combined_Podiums_by_Event_male.index + 1
df_combined_Podiums_by_Event_female.index = df_combined_Podiums_by_Event_female.index + 1
df_Boulder_Lead_Podiums_by_Event_male.index = df_Boulder_Lead_Podiums_by_Event_male.index + 1
df_Boulder_Lead_Podiums_by_Event_female.index = df_Boulder_Lead_Podiums_by_Event_female.index + 1

st.set_page_config(
    page_title="European Championships - Podiums by Event",
    page_icon=":person_climbing:",
	layout="wide",
)

st.header ("Athlete podiums by Event")

tab1, tab2, tab3, tab4, tab5 = st.tabs (["Lead","Speed","Boulder","Combined","Boulder Lead"])

with tab1:
	st.caption(":blue[European Championship podium list male]")
	st.dataframe (df_Lead_Podiums_by_Event_male,
	column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
	},
	height=700, width=1300, hide_index=True)

	st.caption(":blue[European Championship podium list female]")
	st.dataframe (df_Lead_Podiums_by_Event_female,
	column_order=("Competition","Year","Athlete","FinishPosition"),
	column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",)},
	height=700, width=1300, hide_index=True)
with tab2:
	col1, col2 = st.columns(2)
	with col1:
		st.caption(":blue[European Championship podium list male]")
		st.dataframe (df_Speed_Podiums_by_Event_male,
		column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
		},
		height=700, width=1300, hide_index=True)
	with col2:
		st.caption(":blue[European Championship podium list female]")
		st.dataframe (df_Speed_Podiums_by_Event_female,
		column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
		},
		height=700, width=1300, hide_index=True)
with tab3:
	col1, col2 = st.columns(2)
	with col1:
		st.caption(":blue[European Championship podium list male]")
		st.dataframe (df_Boulder_Podiums_by_Event_male,
		column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
		},
		height=700, width=1300, hide_index=True)
	with col2:
		st.caption(":blue[European Championship podium list female]")
		st.dataframe (df_Boulder_Podiums_by_Event_female,
		column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
		},
		height=700, width=1300, hide_index=True)
with tab4:
	col1, col2 = st.columns(2)
	with col1:
		st.caption(":blue[European Championship podium list male]")
		st.dataframe (df_combined_Podiums_by_Event_male,
		column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
		},
		width=1300, hide_index=True)
	with col2:
		st.caption(":blue[European Championship podium list female]")
		st.dataframe (df_combined_Podiums_by_Event_female,
		column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
		},
		width=1300, hide_index=True)
with tab5:
	col1, col2 = st.columns(2)
	with col1:
		st.caption(":blue[European Championship podium list male]")
		st.dataframe (df_Boulder_Lead_Podiums_by_Event_male,
		column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
		},
		width=1300, hide_index=True)
	with col2:
		st.caption(":blue[European Championship podium list female]")
		st.dataframe (df_Boulder_Lead_Podiums_by_Event_female,
		column_config={
		"Year": st.column_config.NumberColumn("Year",format="%d",),
		"1":  st.column_config.Column("Gold"),
		"2":  st.column_config.Column("Silver"),
		"3":  st.column_config.Column("Bronze"),
		},
		width=1300, hide_index=True)

st.divider ()
st.write("# You can sort any of the tables by clicking on the column header and choosing the sort direction")
#st.write ('working:', current_dir)