import streamlit as st,pandas as pd,os, math
import streamlit_ext as ste

refweatheryear = 2018   #Default value

#user input
def weather_input():
	
	scenario_list = ['NEN 5060:2018','NEN 5060:2018 (1% Extreme)', 'NEN 5060:2018 (5% Extreme)', 'IPCC A1B', 'IPCC A2', 'IPCC B1']
	
	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Weather Scenario</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col1, col2, col3 = st.columns(3)
	with col1:
		refscenario = ste.selectbox("Select a weather scenario", scenario_list,help='Whole Building Energy Simualtion are dependant on climatic data of the location. Based on the selected location current Dutch reference weather data or IPCC-based future weather data can be used', key='scenariolist')
	if(refscenario in ['IPCC A1B', 'IPCC A2', 'IPCC B1']):
		original_title = '<p style="font-family:Sans serif; color:White; font-size: 20px;"><b>IPCC Future Reference Year</b></p>'
		st.markdown(original_title, unsafe_allow_html=True)
		ipccyear = ste.radio("Select a reference future year",('2050','2100'), horizontal=True, key='ipccyear')
		global refweatheryear 
		refweatheryear = ipccyear

	for i in range(3):
		st.write("")
	save = st.checkbox('Save Inputs (*)', value=False, key='weathersave')

	if(save):
		valuelist = [refscenario,refweatheryear]
		columnlist = ['Weather Scenario', 'Reference Year']


		#Current working directory
		cwd = os.getcwd()
		#set path to subdirectory and inputfilename
		inputfilesnamewithpath = cwd+'\\Inputfiles\\WeatherUserInputs.csv'

		#Write the inputs to a csv file
		inputdf = pd.DataFrame([valuelist], columns = columnlist)

		inputdf.to_csv(inputfilesnamewithpath, index=False)
		


