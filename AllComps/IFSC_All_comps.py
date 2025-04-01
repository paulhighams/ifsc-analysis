import streamlit as st

st.set_page_config(
    page_title="All comps",
    page_icon="👋",
	layout="centered"
)

st.write("# Welcome to statistics about Athletes for sport Climbing! 👋")

st.sidebar.success("Select an analysis above.")

st.markdown(
    """
    On the menu on the left are a set of statistics organised by topic. Within each topic you will find multiple tabs
    **👈 Pick a category and get started
    ### For all the tables of data the buttons on the top right allow you to:
    - Download the table as a csv
    - Search for a value within the table
    - Make the table fullscreen
    ### If you want to change the order of the table
    - Click on the column header of the column you wish to sort on
    - Click once for ascending order, and click again for descending order
"""
)