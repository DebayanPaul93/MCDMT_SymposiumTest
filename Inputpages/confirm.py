import streamlit as st, time

#import files
import Outputpages.trh
import Outputpages.energy
import Outputpages.paperlife
import Outputpages.pvresults

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

#user input
def confirm_input():
	st.session_state['buttonclick'] = 'Not Done'
	original_title = '<p style="font-family:Sans serif; color:Red; font-size: 30px;"><b>Confirm All Inputs Selection for Simulation</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	alloptionselection_check = st.checkbox('Confirm all necessary inputs have been selected')
	if(alloptionselection_check):
		calbutton = st.button("Calculate", key='simlcalbutton')
		if(calbutton):
			with st.spinner('Wait for the Results...'):
				time.sleep(5)
			st.success('Simulations Successfully Done!')
			st.success('Results are being prepared for visualization...')
			time.sleep(2) # Just to add a delay to show up visualization

	resultmenu = ['Conditioned Space T & RH','Utility Consumption','Collection Lifetime','PV Performance']           #added a blank selection field
	resultchoice = st.sidebar.selectbox('Select Result Page',resultmenu)

	match resultchoice:
	    case 'Conditioned Space T & RH': Outputpages.trh.trh_output()
	    case 'Utility Consumption': Outputpages.energy.energy_output()
	    case 'Collection Lifetime': Outputpages.paperlife.paperlife_output()
	    case 'PV Performance': Outputpages.pvresults.pv_output()



	    




		
			
			
				
				

				

		




			
			
    			
	