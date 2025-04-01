import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df_Female_athlete_stats = pd.read_csv('AllComps/report_files/athlete_stats_all_disciplines_female.csv')
df_Male_athlete_stats = pd.read_csv('AllComps/report_files/athlete_stats_all_disciplines_male.csv')
df_athlete_stats_all_disciplines = pd.read_csv('AllComps/report_files/athlete_stats_all_disciplines.csv') 

# set the indexes to start at 1
df_Female_athlete_stats.index = df_Female_athlete_stats.index + 1
df_Male_athlete_stats.index = df_Male_athlete_stats.index + 1

# generate graphs
# add in the code to generate the sankey diagrams.
	# filter for a nation
country_list = ['KOR','ITA','FRA','GBR','GER','AUT','JPN','USA','BEL','SUI','SLO','RUS','UKR','ESP','CZE','POL','CHN','INA']
for cntry_idx in country_list:
	filter_country = cntry_idx
	df_country = df_athlete_stats_all_disciplines[df_athlete_stats_all_disciplines['Country'] == filter_country]
	df_country = df_country.reset_index()
	#
	# get the unique list of athletes
	list_node_1 = list(df_country['Athlete'].unique())
	uninum_dict = {}
	for uninum in range(len(list_node_1)):
		uninum_dict [list_node_1[uninum]] = uninum+10

	# Define a function to map the values
	def set_value(row_number, assigned_value):
		return assigned_value[row_number]
	#ADD A Column with a unique athlete number, then use this rather than ind to build the lists of links
	df_country['uninum'] = df_country['Athlete'].apply(set_value, args =(uninum_dict, ))

	fixed_pt1 = [filter_country, "BoulderGold", "BoulderSilver", "BoulderBronze", "LeadGold", "LeadSilver","LeadBronze","SpeedGold","SpeedSilver","SpeedBronze"]
	fixed_pt2 = ["Male","Female"]
	final_nodes = fixed_pt1 + list_node_1 + fixed_pt2
	colours_pt1 = ["olive","gold","silver","rosybrown","gold","silver","rosybrown","gold","silver","rosybrown"]
	colours_pt2 = ["lightskyblue","lightpink"]
	athletes_list = []
	for i in range(len(list_node_1)):
		athletes_list.append("grey")
	final_colours = colours_pt1 + athletes_list + colours_pt2

	headers = [final_nodes,final_colours]

	# then build the links
	# build from country to disc/medals
	Boulder_first = 0
	Boulder_second = 0
	Boulder_third = 0
	Lead_first = 0
	Lead_second = 0
	Lead_third = 0
	Speed_first = 0
	Speed_second = 0
	Speed_third = 0

	for ind in range(len(df_country)):
		#ind = ind +10
		if df_country.loc[ind, "Discipline"] == 'Boulder':
			Boulder_first = Boulder_first + df_country.loc[ind, "First"]
			Boulder_second = Boulder_second + df_country.loc[ind, "Second"]
			Boulder_third = Boulder_third + df_country.loc[ind, "Third"]
		elif df_country.loc[ind, "Discipline"] == 'Lead':
			Lead_first = Lead_first + df_country.loc[ind, "First"]
			Lead_second = Lead_second + df_country.loc[ind, "Second"]
			Lead_third = Lead_third + df_country.loc[ind, "Third"]
		elif df_country.loc[ind, "Discipline"] == 'Speed':
			Speed_first = Speed_first + df_country.loc[ind, "First"]
			Speed_second = Speed_second + df_country.loc[ind, "Second"]
			Speed_third = Speed_third + df_country.loc[ind, "Third"]
		else:
			fred = 0

	link_source_pt1 = [0,0,0,0,0,0,0,0,0]
	link_target_pt1 = [1,2,3,4,5,6,7,8,9]
	link_value_pt1 = [Boulder_first,Boulder_second,Boulder_third,Lead_first,Lead_second,Lead_third,Speed_first,Speed_second,Speed_third]
	link_colour_pt1 = ["gold","silver","rosybrown","gold","silver","rosybrown","gold","silver","rosybrown"]

	#build from disc/medals to athlete
	# can get this by extracting the columns from df_country and then getting rid of rows where first/second/third is null
	CompAthsource = []
	CompAthtarget = []
	CompAthvalue = []
	CompAthcolour = []
	for ind in range(len(df_country)):
		#ind = ind +10
		if df_country.loc[ind, "First"] > 0:
			if df_country.loc[ind, "Discipline"] == 'Boulder':
				CompAthsource.append(1)
				CompAthcolour.append("gold")
			if df_country.loc[ind, "Discipline"] == 'Lead':
				CompAthsource.append(4)
				CompAthcolour.append("gold")
			if df_country.loc[ind, "Discipline"] == 'Speed':
				CompAthsource.append(7)
				CompAthcolour.append("gold")
			CompAthtarget.append(df_country.loc[ind, "uninum"])
			CompAthvalue.append(df_country.loc[ind, "First"])
		if df_country.loc[ind, "Second"] > 0:
			if df_country.loc[ind, "Discipline"] == 'Boulder':
				CompAthsource.append(2)
				CompAthcolour.append("silver")
			if df_country.loc[ind, "Discipline"] == 'Lead':
				CompAthsource.append(5)
				CompAthcolour.append("silver")
			if df_country.loc[ind, "Discipline"] == 'Speed':
				CompAthsource.append(8)
				CompAthcolour.append("silver")
			CompAthtarget.append(df_country.loc[ind, "uninum"])
			CompAthvalue.append(df_country.loc[ind, "Second"])
		if df_country.loc[ind, "Third"] > 0:
			if df_country.loc[ind, "Discipline"] == 'Boulder':
				CompAthsource.append(3)
				CompAthcolour.append("rosybrown")
			if df_country.loc[ind, "Discipline"] == 'Lead':
				CompAthsource.append(6)
				CompAthcolour.append("rosybrown")
			if df_country.loc[ind, "Discipline"] == 'Speed':
				CompAthsource.append(9)
				CompAthcolour.append("rosybrown")
			CompAthtarget.append(df_country.loc[ind, "uninum"])
			CompAthvalue.append(df_country.loc[ind, "Third"])

	#build athlete to gender
	# use the df from step above and loop through to count up by athlete to male/female
	GenderAthsource = []
	GenderAthtarget = []
	GenderAthvalue = []
	GenderAthcolour = []
	for ind in range(len(df_country)):
		#ind = ind +10
		if df_country.loc[ind, "Gender"] == 'Male':
			GenderAthtarget.append(len(list_node_1)+10)
			GenderAthcolour.append("lightskyblue")
		if df_country.loc[ind, "Gender"] == 'Female':
			GenderAthtarget.append(len(list_node_1)+11)
			GenderAthcolour.append("lightpink")
		GenderAthsource.append(df_country.loc[ind, "uninum"])
		GenderAthvalue.append(df_country.loc[ind, "First"]+df_country.loc[ind, "Second"]+df_country.loc[ind, "Third"])

	#put all the bits together
	FinalSource = link_source_pt1 + CompAthsource + GenderAthsource
	FinalTarget = link_target_pt1 + CompAthtarget + GenderAthtarget
	FinalValue = link_value_pt1 + CompAthvalue + GenderAthvalue
	FinalColour = link_colour_pt1 + CompAthcolour + GenderAthcolour

	data = [ FinalSource, FinalTarget, FinalValue, FinalColour]
	# now plot the sankey diagram
	df = pd.DataFrame (data)
	dfh = pd.DataFrame (headers)
    
	fig = go.Figure(data=[go.Sankey(
	valueformat = ".0f",
	node = dict(pad = 15, thickness = 60, line = dict(color = "black", width = 0.5), label = dfh.iloc[0], color = dfh.iloc[1]),
	link = dict(source = df.iloc[0], target = df.iloc[1], value = df.iloc[2], color = df.iloc[3])
    )])

	fig.update_layout(title_text="World Cup Medal Breakdown for (" + filter_country + ")", font_size=10)
	globals()[f'{cntry_idx}_fig'] = fig


# now do the streamlit report
st.set_page_config(
    page_title="All Disciplines Athlete Statistics",
    page_icon="👋",
	layout="wide",
)

st.header ("All Disciplines Athlete Statistics")

tab1, tab2, tab3 = st.tabs (["Female Career Stats","Male Career Stats","World Cup Medal Breakdown by Country"])

with tab1:
	st.dataframe (df_Female_athlete_stats,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	st.caption(":blue[The ranking is based on WC Series wins, then WChamp Golds, then WCup wins]")
with tab2:
	st.dataframe (df_Male_athlete_stats,
		column_config={ "Unnamed: 0": st.column_config.Column("ranking")},
		height=800, hide_index=True)
	st.caption(":blue[The ranking is based on WC Series wins, then WChamp Golds, then WCup wins]")
with tab3:
    option = st.selectbox (
        "Which Country do you want a medal breakdown for",
        ("ITA","FRA","GER","GBR","AUT","BEL","SUI","SLO","ESP","CZE","POL","UKR","RUS",
         "USA","KOR","CHN","INA","JPN"),
        index=None,
        placeholder="Choose a Country",
    )

    if option == 'ITA':
        st.plotly_chart (ITA_fig)
    elif option == 'FRA':
        st.plotly_chart (FRA_fig)
    elif option == 'GER':
        st.plotly_chart (GER_fig)
    elif option == 'GBR':
        st.plotly_chart (GBR_fig)
    elif option == 'AUT':
        st.plotly_chart (AUT_fig)
    elif option == 'BEL':
        st.plotly_chart (BEL_fig)
    elif option == 'SUI':
        st.plotly_chart (SUI_fig)
    elif option == 'SLO':
        st.plotly_chart (SLO_fig)
    elif option == 'ESP':
        st.plotly_chart (ESP_fig)
    elif option == 'CZE':
        st.plotly_chart (CZE_fig)
    elif option == 'POL':
        st.plotly_chart (POL_fig)
    elif option == 'UKR':
        st.plotly_chart (UKR_fig)
    elif option == 'RUS':
        st.plotly_chart (RUS_fig)
    elif option == 'USA':
        st.plotly_chart (USA_fig)
    elif option == 'KOR':
        st.plotly_chart (KOR_fig)
    elif option == 'CHN':
        st.plotly_chart (CHN_fig)
    elif option == 'INA':
        st.plotly_chart (INA_fig)
    elif option == 'JPN':
        st.plotly_chart (JPN_fig)
    else:
        st.caption(":red[# Sorry something went wrong]")


st.divider ()

st.caption(":violet[# You can sort any of the tables by clicking on the column header and choosing the sort direction]")
