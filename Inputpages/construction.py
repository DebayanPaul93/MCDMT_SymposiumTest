import streamlit as st

#user input

def construction_input():
	insulationlevel_list=['No','Low','Medium','High']
	infiltrationlevel_list=['Low','Medium','High','Custom']
	original_title = '<p style="font-family:Sans serif; color:deeppink; font-size: 30px;"><b>Building Construction Insulation Level</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)

	wallinsulationselection_check = st.checkbox('Do you want to add custom Rc values for constructions?')
	if(wallinsulationselection_check):
		colp, colq, colr = st.columns(3)
		with colp:
			wallrc = st.number_input("Enter Wall Rc",min_value=0.0,max_value=7.0,step=0.5,format="%.1f")
		with colq:
			roofrc = st.number_input("Enter Roof Rc",min_value=0.0,max_value=7.0,step=0.5,format="%.1f")
		with colr:
			floorrc = st.number_input("Enter Floor Rc",min_value=0.0,max_value=7.0,step=0.5,format="%.1f")

	if(wallinsulationselection_check is False):
		col1, col2, col3 =st.columns(3)
		with col1:
			wallinslevel = st.selectbox("Select Wall Insulation Level", insulationlevel_list)

		with col2:
			roofinslevel = st.selectbox("Select Roof Insulation Level", insulationlevel_list)

		with col3:
			floorinslevel = st.selectbox("Select Floor Insulation Level", insulationlevel_list)

	original_title = '<p style="font-family:Sans serif; color:deeppink; font-size: 30px;"><b>Building Construction Infiltration Level</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col4, col5, col6 = st.columns(3)
	with col4:
		infiltrationlevel = st.selectbox("Select Building Infiltration Level", infiltrationlevel_list)
	if(infiltrationlevel == 'Custom'):
		col8, col9, col10 = st.columns(3)
		with col8:
			wallrc = st.number_input("Enter Infiltration Rate (ACH)",min_value=0.2,max_value=2.0,step=0.2)
