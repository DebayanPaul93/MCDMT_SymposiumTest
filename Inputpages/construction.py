import streamlit as st,pandas as pd,os, math
import streamlit_ext as ste

#user input

def construction_input():
	#Defining default null values
	wallrc, roofrc, floorrc = None, None, None
	wallinslevel, roofinslevel, floorinslevel = None, None, None
	custominfiltrationrate = None

	insulationlevel_list=['No','Low','Medium','High']
	infiltrationlevel_list=['Low','Medium','High','Custom']
	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Building Construction Insulation Level</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)

	wallinsulationselection_check = ste.checkbox('Do you want to add custom Rc values for constructions?',key='rccheck')
	if(wallinsulationselection_check):
		colp, colq, colr = st.columns(3)
		with colp:
			wallrc = ste.number_input("Enter Wall Rc",min_value=1,max_value=8,step=1,key='wallrc')
		with colq:
			roofrc = ste.number_input("Enter Roof Rc",min_value=1,max_value=8,step=1,key='roofrc')
		with colr:
			floorrc = ste.number_input("Enter Floor Rc",min_value=1,max_value=8,step=1,key='floorrc')

	if(not wallinsulationselection_check):
		col1, col2, col3 =st.columns(3)
		with col1:
			wallinslevel = ste.selectbox("Select Wall Insulation Level", insulationlevel_list,key='wallinsl')

		with col2:
			roofinslevel = ste.selectbox("Select Roof Insulation Level", insulationlevel_list,key='roofinsl')

		with col3:
			floorinslevel = ste.selectbox("Select Floor Insulation Level", insulationlevel_list,key='floorinsl')

	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Building Construction Infiltration Level</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col4, col5, col6 = st.columns(3)
	with col4:
		infiltrationlevel = ste.selectbox("Select Building Infiltration Level", infiltrationlevel_list,key='infiltration')
	if(infiltrationlevel == 'Custom'):
		col8, col9, col10 = st.columns(3)
		with col8:
			custominfiltrationrate = st.number_input("Enter Infiltration Rate (ACH)",min_value=0.05,max_value=2.0,value=0.2,step=0.05,key='custominfiltration')

	for i in range(3):
		st.write("")
	save = st.checkbox('Save Inputs (*)', value=False, key='constructionsave')
