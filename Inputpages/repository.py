import streamlit as st

#user input

def size_input():
	original_title = '<p style="font-family:Sans serif; color:Magenta; font-size: 30px;"><b>Collection Amount</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col1, col2, col3 = st.columns(3)
	with col1:
		collectionsize = st.number_input("Enter Size of Collection (in km)",min_value=10,max_value=150,step=10)
	original_title = '<p style="font-family:Sans serif; color:Magenta; font-size: 30px;"><b>Storage Filling Percentage (%)</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	fillperct = st.radio("Select filling percentage",('Fixed rack (35%)','Mobile rack (80%)','Custom Filling Percentage'))
	if(fillperct == 'Custom Filling Percentage'):
		colp, colq, colr = st.columns(3)
		with colp:
			fillperctvalue = st.number_input("Enter Filling Percentage",min_value=10,max_value=80,step=5)

	original_title = '<p style="font-family:Sans serif; color:Magenta; font-size: 30px;"><b>Repository Dimesnion</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col5, col6, col7 = st.columns(3)
	with col5:
		repo_length = st.number_input("Enter Length of Repository (in m)",min_value=10,max_value=30,step=2,key='length')
	with col6:
		repo_width = st.number_input("Enter Width of Repository (in m)",min_value=10,max_value=30,step=2,key='width')
	with col7:
		repo_floorheight = st.number_input("Enter Height of each Floor (in m)",min_value=3.5,max_value=5.5,step=0.5,key='height',format="%.1f")

	for i in range (5):
		st.write("")
	st.markdown("### Confirm the ranges of dimension and paper size!!!")