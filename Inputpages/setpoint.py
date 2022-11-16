import streamlit as st

#user input

def setpoint_input():
	original_title = '<p style="font-family:Sans serif; color:Yellow; font-size: 30px;"><b>Annual Average T & RH (Maximum)</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col1, col2, col3, col4 = st.columns(4)
	with col1:
		temperature = st.slider("Select Temperaure",min_value=16,max_value=19,step=1,value=18,key='t')
	col5, col6, col7, col8 = st.columns(4)
	with col5:
		rel_humid = st.slider("Select RH",min_value=45,max_value=55,step=5,value=50,key='rh')

	original_title = '<p style="font-family:Sans serif; color:Yellow; font-size: 30px;"><b>Type of Fluctuation Allowed in Setpoints</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	fluctype = st.radio("Select range type for fluctuation",('Very Small','Medium','Archival Limit with Safety Tolerance'),index=1,help='The fluctuation type indicates a probable range for how widely Temperature & Relative Humidity can fluctuate inside repository')

	
	if(fluctype=='Medium' or fluctype=='Archival Limit with Safety Tolerance'):
		if(rel_humid!=55):
			original_title = '<p style="font-family:Sans serif; color:Yellow; font-size: 20px;"><b>Seasonal Control</b></p>'
			st.markdown(original_title, unsafe_allow_html=True)
			rh_check = st.checkbox('Enable Seasonal Control',value=True, help='An option to define for users to possible limit rapid fluctuations in Relative Humidity between Seasons')