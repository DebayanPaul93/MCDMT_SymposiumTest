import streamlit as st
from streamlit.components.v1 import html

#user input
def hvac_input():
	heatingsource_list = ['Electric Boiler','Geothermal Heat Pump']
	coolingsource_list = ['Direct Expansion Coil','Geothermal Heat Pump','Water-Cooled Chiller']
	original_title = '<p style="font-family:Sans serif; font-size: 30px;"><b>HVAC System Selection</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	hvacselection_check = ste.checkbox('Do you want to select a HVAC System?',help='This checkbox allows user to set sources for heating/cooling from a list of pre-selected options. Otherwise, the model automatically selects them', key='hvacselectioncheck')

	if(hvacselection_check):
		col1, col2 =st.columns(2)
		with col1:
			heatingsource = ste.selectbox("Select a Heating Source", heatingsource_list, key='heatsourcelist')
		with col2:
			coolingsource = ste.selectbox("Select a Cooling Source", coolingsource_list, key='coolsourcelist')

	mechventselection_check = ste.checkbox('Do you want to modify mechanical ventilation rate?', help= 'This checkbox allows user to define additional fresh air change rate per hour through a dedicated mechanical ventilation system. otherwise, the model runs on a very limited amount of mechanical ventilation as per archival guidelines', key='mechventselectioncheck')
	if(mechventselection_check):
		col3, col4 = st.columns(2)
		with col3:
			mechventrate = ste.number_input("Enter Mechanical Ventilation Rate (ACH)",min_value=0.0,max_value=2.0,step=0.1,format="%.1f", key='custommechvent')

	fanselection_check = ste.checkbox('Do you want to add filters for particulate matter?', help = 'An additional option for user to enable increased pressure drops in Air Handling Unit due to particualte filters instalaltion', key='fanselectioncheck')

	original_title = '<p style="font-family:Sans serif; font-size: 30px;"><b>HVAC System Sizing</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)


	sizingoption = ste.radio("Select sizing method",('Adequately Sized','Manual Sizing'), help ='An advanced option for user to set adequate or increaseed/limited sizing capacity of heating & cooling source', key='sizing1')


	if(sizingoption == 'Manual Sizing'):
		col7, col8 = st.columns(2)
		with col7:
			heatingsourcesize = ste.number_input("Enter Minimum % Hours of Met Heating Load",min_value=50,max_value=95,step=5, key='customheatsize')
		with col8:
			coolingsourcesize = ste.number_input("Enter Minimum % Hours of Met Cooling Load",min_value=50,max_value=95,step=5, key='customcoolsize')

