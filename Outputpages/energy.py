import streamlit as st,sys
from pathlib import Path
import lxml
from PIL import Image
import esoreader as esr, pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
pd.set_option('mode.chained_assignment', None)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.simplefilter(action = 'ignore')
plt.rcParams['xtick.direction'] = 'inout'
plt.rcParams['ytick.direction'] = 'inout'
plt.rcParams['axes.linewidth'] = 3.0
plt.rcParams['lines.linewidth'] = 4

def energy_output():
	expander = st.expander("Building-level Energy Consumption", expanded=False)
	expander.write("")

	#read html file and convert it to dataframe object
	areadf_table = pd.read_html('eplustbl.htm',
                   match='Total Building Area', header=0)[1]
	areadf_table.set_index('Unnamed: 0', inplace=True)
	area = round(areadf_table.loc['Net Conditioned Building Area']['Area [m2]'])

	enduse_table = pd.read_html('eplustbl.htm',
               match='Heating', header=0)[1]

	enduse_table.set_index('Unnamed: 0', inplace=True)
	typeofuselist = ['Heating','Cooling','Fans','Pumps','Humidification']
	valueslist = []
	for use in typeofuselist:
	    valueslist.append(round(enduse_table.loc[use]['Electricity [kWh]'] / area,2))
	    
	usevaluedf = pd.DataFrame(valueslist,columns=['Consumption (kWh/m2)'],index=typeofuselist)
	misc = usevaluedf.loc[['Fans', 'Pumps']].sum()[0]
	valueslist.append(misc)
	del valueslist[2]
	del valueslist[2]

	typeofuselist = ['Heating','Cooling','Humidification','Miscellaneous (Fans & Pumps)']
	usevaluedf.drop(usevaluedf.index[[2,3]], inplace=True)

	#recreate the dataframe
	usevaluedf = pd.DataFrame(valueslist,columns=['Consumption (kWh/m2)'],index=typeofuselist)
	totalutilityconsumption = round(usevaluedf['Consumption (kWh/m2)'].sum(),2)

	if (Path('EndUse.jpg').is_file() is False):                
		#End-Use Plot creater
		fig = plt.figure(figsize = (24,12))
		ax = fig.add_axes([0,0,1,1])
		usetypes = usevaluedf.index.tolist()
		ax.bar(usetypes,valueslist)
		ax.grid(axis = 'y')
		ax.grid(axis = 'x')
		ax.set_ylabel('End-Use Consumption (kWh/$m^2$)', fontsize = 30, labelpad=20)

		plt.tick_params(
		    axis='x',          # changes apply to the x-axis
		    which='both',      # both major and minor ticks are affected
		    bottom=False,      # ticks along the bottom edge are off
		    top=False)         # ticks along the top edge are off

		fig.tight_layout()
		ax.autoscale(enable=True)

		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)

		for tick in ax.yaxis.get_major_ticks():
		      tick.label.set_fontsize(25)
		        
		for tick in ax.xaxis.get_major_ticks():
		      tick.label.set_fontsize(25)
		        
		plt.legend(['Total End-use Consumption (kWh/$m^2$): '+str(totalutilityconsumption)], fontsize = 25,loc='best', frameon=False, ncol=1, bbox_to_anchor=(1.0, 1.0))
		plt.savefig('EndUse.jpg', bbox_inches='tight', pad_inches=0.1)

	#plot through streamlit
	enduseimg = Image.open("EndUse.jpg")
	expander.image(enduseimg)

	#Display the dataframe as table
	col1, col2, col3 = st.columns(3)
	with col1:
		st.write("")
	with col2:
		st.dataframe(usevaluedf, width=400)
	with col3:
		st.write("")
