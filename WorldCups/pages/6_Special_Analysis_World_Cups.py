import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# import the files
df_male_speed_times = pd.read_csv('WorldCups/report_files/Male_Speed_Qualifying_times_by_Year')
df_female_speed_times = pd.read_csv('WorldCups/report_files/Female_Speed_Qualifying_times_by_Year')
df_lead_tops_in_finals = pd.read_csv('WorldCups/report_files/Lead_Tops_in_Finals_by_Year')
df_lead_tops_in_semifinals = pd.read_csv('WorldCups/report_files/Lead_Tops_in_Semi_Finals_by_Year')
df_lead_tops_in_finals_and_semis = pd.read_csv('WorldCups/report_files/Lead_Tops_in_Finals_Semi_Finals_by_Year')
df_athletes_competing = pd.read_csv('WorldCups/report_files/Number_of_athletes_competing_per_discipline_by_year')

#create the plots
pic_male_speed_times = px.box(df_male_speed_times, x="Year", y="QualTime", notched=True)
pic_male_speed_times.update_layout(xaxis={"dtick":1},margin={"t":0,"b":0}, height=800)

pic_female_speed_times = px.box(df_female_speed_times, x="Year", y="QualTime", notched=True)
pic_female_speed_times.update_layout(xaxis={"dtick":1},margin={"t":0,"b":0}, height=800)

pic_lead_tops_in_finals = px.bar(df_lead_tops_in_finals, x="Year", y="NumTops", color='Gender')
pic_lead_tops_in_finals.update_layout(xaxis={"dtick":1},margin={"t":0,"b":0})
pic_lead_tops_in_finals.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=True)
pic_lead_tops_in_finals.update_xaxes(tickangle=90)

pic_lead_tops_in_semifinals = px.bar(df_lead_tops_in_semifinals, x="Year", y="NumTops", color='Gender')
pic_lead_tops_in_semifinals.update_layout(xaxis={"dtick":1},margin={"t":0,"b":0})
pic_lead_tops_in_semifinals.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=True)
pic_lead_tops_in_semifinals.update_xaxes(tickangle=90)

pic_lead_tops_in_finals_and_semis = px.bar(df_lead_tops_in_finals_and_semis, x="Year", y="NumTops", color='Gender')
pic_lead_tops_in_finals_and_semis.update_layout(xaxis={"dtick":1},margin={"t":0,"b":0})
pic_lead_tops_in_finals_and_semis.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=True)
pic_lead_tops_in_finals_and_semis.update_xaxes(tickangle=90)

pic_athletes_competing = go.Figure()
pic_athletes_competing.add_trace(go.Scatter(x=df_athletes_competing.query('Discipline=="Boulder"')['Athletes'], y=df_athletes_competing.Country,
								name='Boulder Competitions',
								marker=dict(color="crimson", size=12),
    							mode="markers"
 					))
pic_athletes_competing.add_trace(go.Scatter(x=df_athletes_competing.query('Discipline=="Lead"')['Athletes'], y=df_athletes_competing.Country,
								name='Lead Competitions',
								marker=dict(color="gold", size=12),
    							mode="markers",
								))
pic_athletes_competing.add_trace(go.Scatter(x=df_athletes_competing.query('Discipline=="Speed"')['Athletes'], y=df_athletes_competing.Country,
								name='Speed Competitions',
								marker=dict(color="blue", size=12),
    							mode="markers",
								))
pic_athletes_competing.update_layout(xaxis={"dtick":1},margin={"t":0,"b":0},height=500)
pic_athletes_competing.update_xaxes(tickangle=90)
pic_athletes_competing.update_layout(title="Number of athletes competing per discipline by year")
#pic_athletes_competing.show()

# streamlit stuff

st.set_page_config(
    page_title="Special Analysis for World Cups",
    page_icon="👋",
	layout="wide",
)

st.header ("Special Analysis for World Cups")

tab1, tab2, tab3, tab4 = st.tabs (["Male speed qualyfing times by year",
    "Female speed qualyfing times by year", "Lead Tops Analysis", 
    "Number of athletes competing by discipline by year"])

with tab1:
	    st.caption(":blue[World Cup speed qualifying analysis]")
	    st.plotly_chart (pic_male_speed_times, hide_index=True)
with tab2:
	    st.caption(":blue[World Cup speed qualifying analysis]")
	    st.plotly_chart (pic_female_speed_times, hide_index=True)
with tab3:
	    st.caption(":blue[World Cup Lead tops analysis]")
	    st.plotly_chart (pic_lead_tops_in_finals, hide_index=True)
	    st.caption(":blue[World Cup Lead tops analysis]")
	    st.plotly_chart (pic_lead_tops_in_semifinals, hide_index=True)
	    st.caption(":blue[World Cup Lead tops analysis]")
	    st.plotly_chart (pic_lead_tops_in_finals_and_semis, hide_index=True)
with tab4:
	    st.caption(":blue[Number of athletes competing by discipline by year]")
	    st.plotly_chart (pic_athletes_competing, hide_index=True)

st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")



