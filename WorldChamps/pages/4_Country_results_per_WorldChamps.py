import streamlit as st
import pandas as pd

df_Medal_Table_per_Boulder = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_Boulder.csv')
df_Medal_Table_per_Lead = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_Lead.csv')
df_Medal_Table_per_Speed = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_Speed.csv')
df_Medal_Table_per_Combined = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_Combined.csv')
df_Medal_Table_per_BoulderLead = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_BoulderLead.csv')
df_Medal_Table_per_All_disciplines = pd.read_csv('WorldChamps/report_files/World_Championships_Medal_Table_for_All_disciplines_per_World_Championship.csv')

#update the indexes
df_Medal_Table_per_Boulder.index = df_Medal_Table_per_Boulder.index + 1
df_Medal_Table_per_Lead.index = df_Medal_Table_per_Lead.index + 1
df_Medal_Table_per_Speed.index = df_Medal_Table_per_Speed.index + 1
df_Medal_Table_per_Combined.index = df_Medal_Table_per_Combined.index + 1
df_Medal_Table_per_BoulderLead.index = df_Medal_Table_per_BoulderLead.index + 1
df_Medal_Table_per_All_disciplines.index = df_Medal_Table_per_All_disciplines.index + 1

st.set_page_config(
    page_title="Country Results per World Championships",
    page_icon="👋",
	layout="wide",
)

st.header ("Country Results per World Championships")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs (["Boulder","Lead","Speed","Combined","Boulder Lead","All disciplines"])

with tab1:
	st.dataframe (df_Medal_Table_per_Boulder,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab2:
	st.dataframe (df_Medal_Table_per_Lead,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab3:
	st.dataframe (df_Medal_Table_per_Speed,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab4:
	st.dataframe (df_Medal_Table_per_Combined,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab5:
    st.dataframe (df_Medal_Table_per_BoulderLead,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)
with tab6:
	st.dataframe (df_Medal_Table_per_All_disciplines,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=800, hide_index=True)

st.divider ()

st.caption("# You can sort any of the tables by clicking on the column header and choosing the sort direction")
