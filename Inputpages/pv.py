#import packages
import streamlit as st, time

inputconfirm = False

#user input

def pv_input():
	southpanel_list=['Beaut Solar (36 Cells)','Solarge (72 Cells)','MHI (120 Cells)']
	ewpanel_list=['Solarge Duo(72 Cells)']
	original_title = '<p style="font-family:Sans serif; color:chartreuse; font-size: 30px;"><b>System Information of Rooftop Photovoltaic Panels</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	panel_orientation = st.radio("Orientation of Panels",('South','East-West'), help='An option for user to select from most two common structural orientations for rooftop Photovoltaic Systems')
	col1, col2 = st.columns(2)
	with col1:
		non_activearea = st.number_input("Enter Non-active area for PV installation (%)",min_value=10,max_value=30,step=5, help='User can define a possible amount of area (% of total roof area) which are unaccessible for Photovoltaic Panels installation ')
	
	if(panel_orientation == 'South'):
		tiltselection_check = st.checkbox('Do you want to select tilt angle of panels?', help='User can define the surface tilt of installed panels or model will optimize the angle amount based on location')
		if(tiltselection_check):
			col5, col6, col7, col8 = st.columns(4)
			with col5:
				tiltangle = st.number_input("Enter tilt angle (in °)",min_value=10,max_value=70,step=2)

	if(panel_orientation == 'South'):
		col9, col10= st.columns(2)
		with col9:
			panelname = st.selectbox("Select a panel from list of selected manufactures", southpanel_list, help='To simplify design a limited amount of pre-selected list of PV panels avaibale in market have been supplied')

	if(panel_orientation == 'East-West'):
		col9, col10= st.columns(2)
		with col9:
			panelname = st.selectbox("Select a panel from list of selected manufactures", ewpanel_list, help='To simplify design a limited amount of pre-selected list of PV panels avaibale in market have been supplied')

	advdatatselection_check = st.checkbox('Do you want to select electrical sizing of PV Systems?', help='User can customize the electrical sizing of the Photovoltaic Systems assembly or model will work with default values of such sizing')
	if(advdatatselection_check):
		col12, col14, col15= st.columns(3)
		with col12:
			dcacratio = st.number_input("Enter DC/AC Ratio",min_value=1.0,max_value=1.3,step=0.05,format="%.2f")
		with col14:
			inverternomeff = st.number_input("Enter Inverter Nominal Efficiency (%)",min_value=92,max_value=98,step=1)

	
	pdfreport_check = st.checkbox('Do you want to create a PDF Report of Performance Summary?')
	for i in range(3):
		st.write("")

	#Styling the Button
	button_style = """
	        <style>
	        .stButton > button {
	            color: black;
	            background: white;
	            width: 150px;
	            height: 50px;
	        }
	        </style>
	        """
	st.markdown(button_style, unsafe_allow_html=True)

	alloptionselection_check = st.checkbox('Confirm all necessary inputs have been selected',key='select')
	if(alloptionselection_check):
		calbutton = st.button("Calculate", key='simlcalbutton')
		if(calbutton):
			with st.spinner('Wait for the Results...'):
				time.sleep(5)
			st.success('Simulations Successfully Done!')
			st.success('Results are being prepared for visualization...')
			time.sleep(2) # Just to add a delay to show up visualization

		global inputconfirm 
		inputconfirm = alloptionselection_check


    





   	
   	
   		

   	


    





   	
   	
   		

   	
