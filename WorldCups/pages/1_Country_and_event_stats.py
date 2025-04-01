import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# import the files
df_venue_events = pd.read_csv('WorldCups/report_files/Top_20_WCup_venues.csv')
df_country_events = pd.read_csv('WorldCups/report_files/Top_20_Num_of_WCup_Events_by_Country.csv')
df_big_numbers = pd.read_csv('WorldCups/report_files/WCup_big_numbers.csv')
df4 = pd.read_csv('WorldCups/report_files/Number_WCup_events_countries_by_Year.csv')
df6 = pd.read_csv('WorldCups/report_files/Number_WCup_events_discipline_by_Year.csv')

# create the graphs
pic4 = go.Figure()
pic4.add_trace(go.Scatter(x=df4.NumEvents, y=df4.Year,
							name='Number of Events',
							marker=dict(color="crimson", size=12),
    						mode="markers"
 				))
pic4.add_trace(go.Scatter(x=df4.NumCountries, y=df4.Year,
							name='Number of Countries Competing',
							marker=dict(color="gold", size=12),
    						mode="markers",
				))
pic4.update_layout(yaxis={"dtick":1},margin={"t":0,"b":0},height=500)
pic4.update_layout(title="Number of events and countries participating by year",)
#pic4.show()
	
pic6 = px.bar(df6, x="Year", y="NumEvents", color="Discipline",
             facet_row="Discipline")
pic6.update_layout(xaxis={"dtick":1},margin={"t":0,"b":0})
pic6.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=True)
pic6.update_xaxes(tickangle=90)

# streamlit setup

st.set_page_config(
    page_title="Country and Event Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("Country and Event Statistics")

tab1, tab2, tab3 = st.tabs (["Event details",
                      "Number of World Cup Events and Countries participating by Year",
                      "Number of World Cup Events by Discipline by Year"])

with tab1:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
	    st.caption(":blue[World Cup venues]")
	    st.dataframe (df_venue_events,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=850, width=800, hide_index=True)
    with col2:
	    st.caption(":blue[Number of countries per event]")
	    st.dataframe (df_country_events,
			column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
			height=8500, width=800, hide_index=True)
    with col3:
	    st.caption(":blue[Number of athletes per event]")
	    st.metric(label=df_big_numbers['StatName'].iloc[0], value= df_big_numbers['theStats'].iloc[0])
	    st.metric(label=df_big_numbers['StatName'].iloc[1], value= df_big_numbers['theStats'].iloc[1])
	    st.metric(label=df_big_numbers['StatName'].iloc[2], value= df_big_numbers['theStats'].iloc[2])
	    st.metric(label=df_big_numbers['StatName'].iloc[3], value= df_big_numbers['theStats'].iloc[3])
	    st.metric(label=df_big_numbers['StatName'].iloc[4], value= df_big_numbers['theStats'].iloc[4])
with tab2:
    st.plotly_chart (pic4)
with tab3:
    st.plotly_chart (pic6)

st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")
