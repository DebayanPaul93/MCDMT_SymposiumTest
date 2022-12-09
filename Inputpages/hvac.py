import streamlit as st
from streamlit.components.v1 import html


#Improt weather file for one test
import Inputpages.weather

#user input
def hvac_input():
	heatingsource_list = ['Electric Boiler','Geothermal Heat Pump']
	coolingsource_list = ['Direct Expansion Coil','Geothermal Heat Pump','Water-Cooled Chiller']
	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>HVAC System Selection</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	hvacselection_check = st.checkbox('Do you want to select a HVAC System?',help='This checkbox allows user to set sources for heating/cooling from a list of pre-selected options. Otherwise, the model automatically selects them')
	if(hvacselection_check):
		col1, col2 =st.columns(2)
		with col1:
			heatingsource = st.selectbox("Select a Heating Source", heatingsource_list)
		with col2:
			coolingsource = st.selectbox("Select a Cooling Source", coolingsource_list)

	mechventselection_check = st.checkbox('Do you want to modify mechanical ventilation rate?', help= 'This checkbox allows user to define additional fresh air change rate per hour through a dedicated mechanical ventilation system. otherwise, the model runs on a very limited amount of mechanical ventilation as per archival guidelines')
	if(mechventselection_check):
		col3, col4 = st.columns(2)
		with col3:
			mechventrate = st.number_input("Enter Mechanical Ventilation Rate (ACH)",min_value=0.2,max_value=2.0,step=0.2,format="%.1f")

	fanselection_check = st.checkbox('Do you want to add filters for particulate matter?', help = 'An additional option for user to enable increased pressure drops in Air Handling Unit due to particualte filters instalaltion')

	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>HVAC System Sizing</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)

	
	refweatheryear = Inputpages.weather.refweatheryear    #return the scenario variable from weather page
	counter = 1 # Define a counter variable for scenario condition test (Intentionally Set it 1 for the IPCC cases)

	if(refweatheryear == 2018):
		counter = 0                 #Set it 0 when it's not IPCC Case
		if(counter == 0):
			sizingoption = st.radio("Select sizing method",('Adequately Sized','Sized for Climate Adversity','Manual Sizing'), help ='An advanced option for user to set adequate or increaseed/limited sizing capacity of heating & cooling source')
	if(counter!=0):
		sizingoption = st.radio("Select sizing method",('Adequately Sized','Manual Sizing'), help ='An advanced option for user to set adequate or limited sizing capacity of heating & cooling source')


	if(sizingoption == 'Manual Sizing'):
		col7, col8 = st.columns(2)
		with col7:
			heatingsourcesize = st.number_input("Enter Minimum % Hours of Met Heating Load",min_value=50,max_value=95,step=5)
		with col8:
			coolingsourcesize = st.number_input("Enter Minimum % Hours of Met Cooling Load",min_value=50,max_value=95,step=5)
