import streamlit as st, time

#import files
import Outputpages.trh
import Outputpages.energy
import Outputpages.paperlife
import Outputpages.pvresults


def resultmenu():
	resultmenu = ['Conditioned Space T & RH','Utility Consumption','Collection Lifetime','PV Performance']           #added a blank selection field
	resultchoice = st.sidebar.selectbox('Select Result Page',resultmenu)

	match resultchoice:
	    case 'Conditioned Space T & RH': Outputpages.trh.trh_output()
	    case 'Utility Consumption': Outputpages.energy.energy_output()
	    case 'Collection Lifetime': Outputpages.paperlife.paperlife_output()
	    case 'PV Performance': Outputpages.pvresults.pv_output()



	    




		
			
			
				
				

				

		




			
			
    			
	