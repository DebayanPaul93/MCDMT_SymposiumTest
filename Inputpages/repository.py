import streamlit as st,pandas as pd,os, math
import streamlit_ext as ste

#user input

def size_input():
	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Collection Amount</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col1, col2, col3 = st.columns(3)
	with col1:
		collectionsize = ste.number_input("Enter Size of Collection (in km)",min_value=5,max_value=200,value=15,step=5, key='collectionsize')
	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Storage Filling Type</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	fillperct = ste.radio("Select filling percentage",('Mobile rack (80%)','Fixed rack (35%)','Custom Filling Percentage'))
	if(fillperct == 'Custom Filling Percentage'):
		colp, colq, colr = st.columns(3)
		with colp:
			fillperctvalue = ste.number_input("Enter Filling Percentage",min_value=10,max_value=80,value=50,step=5,key='customfillpercentage')
	else:
		fillperctvalue = int(fillperct[-4:-2])

	original_title = '<p style="font-family:Sans serif; color:White; font-size: 30px;"><b>Repository Dimension</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col5, col6, col7 = st.columns(3)
	with col5:
		repo_length = ste.number_input("Enter Length of Repository (in m)",min_value=5,max_value=100,value=15,step=5,key='length')
	with col6:
		repo_width = ste.number_input("Enter Width of Repository (in m)",min_value=5,max_value=100,value=10,step=5,key='width')
	with col7:
		repo_floorheight = ste.number_input("Enter Height of each Floor (in m)",min_value=3.5,max_value=6.0,value=4.0,step=0.5,key='height',format="%.1f")

	collection_volume = collectionsize*1000*0.4*0.26
	building_volume = (collection_volume*100)/fillperctvalue
	totalinitialheight = (building_volume/(repo_width*repo_length))
	number_of_floors = math.ceil(totalinitialheight/repo_floorheight)

	if(number_of_floors > 3):
		st.error("Calculated number of floors for the archive is higher than 3. Please change length/width or filling type of repository to make the budiling of max 3 floors", icon="⚠️")

	for i in range(3):
		st.write("")

	if(number_of_floors <= 3):
		save = st.checkbox('Save Inputs (*)', value=False, key='repositorysave')
	

