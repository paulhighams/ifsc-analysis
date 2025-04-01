import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# import the files
df_boulder_female = pd.read_csv('WorldCups/report_files/Number_of_Boulder_World_Cups_attended_female_Top_20.csv')
df_boulder_male = pd.read_csv('WorldCups/report_files/Number_of_Boulder_World_Cups_attended_male_Top_20.csv')
df_lead_female = pd.read_csv('WorldCups/report_files/Number_of_Lead_World_Cups_attended_female_Top_20.csv')
df_lead_male = pd.read_csv('WorldCups/report_files/Number_of_Lead_World_Cups_attended_fale_Top_20.csv')
df_speed_female = pd.read_csv('WorldCups/report_files/Number_of_Speed_World_Cups_attended_female_Top_20.csv')
df_speed_male = pd.read_csv('WorldCups/report_files/Number_of_Speed_World_Cups_attended_male_Top_20.csv')
df_all_female = pd.read_csv('WorldCups/report_files/Number_of_all_disciplines_World_Cups_attended_female_Top_20.csv')
df_all_male = pd.read_csv('WorldCups/report_files/Number_of_all_disciplines_World_Cups_attended_male_Top_20.csv')
df_pic8 = pd.read_csv('WorldCups/report_files/Number_of_athletes_representing_Country_by_Year.csv')

#create the plots
pic8 = go.Figure()
	
CountryList8 = list(df_pic8['Country'].unique())
	
for Country8 in CountryList8:
	pic8.add_trace(
		go.Scatter(
			x = df_pic8['Year'][df_pic8['Country']==Country8],
			y = df_pic8['NumAthletes'][df_pic8['Country']==Country8],
			name = Country8, visible = True
		)
	)
	
buttons8 =[]
	
for i, Country8 in enumerate(CountryList8):
	args = [False] * len(CountryList8)
	args[i] = True
	button8 = dict(label = Country8,
					method = "update",
					args=[{"visible": args}])
	buttons8.append(button8)

pic8.update_layout(xaxis={"dtick":1},margin={"t":0,"b":0},height=500)
pic8.update_xaxes(tickangle=90)

pic8.update_layout(
	updatemenus=[dict(
					active=0,
					type="dropdown",
					buttons=buttons8,
					x = 0,
					y = 1.1,
					xanchor = 'left',
					yanchor = 'bottom',
				)],
	autosize=True
)
#pic8.show()

# streamlit stuff

st.set_page_config(
    page_title="Athlete participation Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("Athlete participation Statistics")

tab1, tab2, tab3, tab4, tab5 = st.tabs (["Boulder World Cup events attended",
    "Lead World Cup events attended",
    "Speed World Cup events attended",
    "All discplines World Cup events attended",
    "Number of athletes representing a country by year"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
	    st.caption(":blue[Boulder World Cup events attended]")
	    st.dataframe (df_boulder_female,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=True)
    with col2:
	    st.caption(":blue[Boulder World Cup events attended]")
	    st.dataframe (df_boulder_male,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=True)
with tab2:
    col1, col2 = st.columns([1, 1])
    with col1:
	    st.caption(":blue[Lead World Cup events attended]")
	    st.dataframe (df_lead_female,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=True)
    with col2:
	    st.caption(":blue[Lead World Cup events attended]")
	    st.dataframe (df_lead_male,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=True)
with tab3:
    col1, col2 = st.columns([1, 1])
    with col1:
	    st.caption(":blue[Speed World Cup events attended]")
	    st.dataframe (df_speed_female,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=True)
    with col2:
	    st.caption(":blue[Speed World Cup events attended]")
	    st.dataframe (df_speed_male,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=True)
with tab4:
    col1, col2 = st.columns([1, 1])
    with col1:
	    st.caption(":blue[All disciplines World Cup events attended]")
	    st.dataframe (df_all_female,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=True)
    with col2:
	    st.caption(":blue[All disciplines World Cup events attended]")
	    st.dataframe (df_all_male,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=1300, hide_index=True)
with tab5:
    st.plotly_chart (pic8)

st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")



