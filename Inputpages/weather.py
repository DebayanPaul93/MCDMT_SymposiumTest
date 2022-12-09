import streamlit as st

refweatheryear = 2018
#user input
def weather_input():
	
	scenario_list = ['NEN 5060:2018','NEN 5060:2018 (1% Extreme)', 'IPCC A1B', 'IPCC A2', 'IPCC B1']
	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Location of Archive</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)

	location = st.radio("Select a location",('Netherlands','Netherlands Antilles'),help='Physical Location of the archive')
	if(location == 'Netherlands'):
		original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Weather Scenario</b></p>'
		st.markdown(original_title, unsafe_allow_html=True)
		col1, col2, col3 = st.columns(3)
		with col1:
			refscenario = st.selectbox("Select a weather scenario", scenario_list,help='Whole Building Energy Simualtion are dependant on climatic data of the location. Based on the selected location current Dutch reference weather data or IPCC-based future weather data can be used')
		if(refscenario in scenario_list[2:]):
			original_title = '<p style="font-family:Sans serif; color:White; font-size: 20px;"><b>IPCC Future Reference Year</b></p>'
			st.markdown(original_title, unsafe_allow_html=True)
			ipccyear = st.radio("Select a reference future year",('2050','2100'), horizontal=True)
			global refweatheryear 
			refweatheryear = ipccyear
		


