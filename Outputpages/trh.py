import streamlit as st,sys
from pathlib import Path
from PIL import Image
import esoreader as esr, pandas as pd
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

def trh_output():
	original_title = '<p style="font-family:Sans serif; color:cyan; font-size: 30px;"><b>Mean Air Temperature in Conditioned Zones</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)

	no_of_zones = 3           # find this from zone calcualtion
	# data retrieving
	list_variables=['Zone Mean Air Temperature','Zone Air Relative Humidity']           #Name the exact variables you want to retrieve
	if(no_of_zones == 1):
	    list_columnnames = ['Zone 1 T','Zone 1 RH']
	elif(no_of_zones == 2):
	    list_columnnames = ['Zone 2 T','Zone 2 RH']
	else:
	    list_columnnames = ['Zone 1 T','Zone 2 T', 'Zone 3 T','Zone 1 RH','Zone 2 RH', 'Zone 3 RH']   
	list_hourlyoutput=[]

	#read eso file and convert to dataframe object
	dd, data = esr.read(r'3_zones.eso')
	for var in list_variables:
	    for i in range(3):
	        frequency, key, variable = dd.find_variable(var)[i] 
	        idx = dd.index[frequency, key, variable]
	        hourly_temptime_series = data[idx]
	        list_hourlyoutput.append(hourly_temptime_series)
    
	df = pd.DataFrame(list_hourlyoutput)
	df_transposed = df.transpose()
	df_transposed.columns = list_columnnames
	timeindex=pd.date_range(start='01/01/2021/00:00:00', end='31/12/2021/23:00:00',freq='H')
	df_transposed.index = timeindex
	df_transposed_zone1 = df_transposed[['Zone 1 T','Zone 1 RH']]
	df_transposed_zone2 = df_transposed[['Zone 2 T','Zone 2 RH']]
	df_transposed_zone3 = df_transposed[['Zone 3 T','Zone 3 RH']]

	#check if already file exists (Simulation is done)
	#if (Path('Temperature.jpg').is_file() is False):        
		#T Plot creater
	fig1 = plt.figure(figsize = (24,12))
	axes = fig1.add_subplot(111)
	axes.plot(df_transposed_zone1.index, df_transposed_zone1['Zone 1 T'], color="green", linestyle='solid', label='')
	axes.plot(df_transposed_zone2.index, df_transposed_zone2['Zone 2 T'], color="orange", linestyle='dashed', label='')
	axes.plot(df_transposed_zone3.index, df_transposed_zone3['Zone 3 T'], color="blue", linestyle='dotted', label='')
	axes.grid(axis = 'y')
	axes.grid(axis = 'x')
	axes.set_ylabel('Temperature [°C]', fontsize = 30, labelpad=20)

	fig1.tight_layout()
	axes.autoscale(enable=True)
	axes.set_xticks(df_transposed_zone1.index, minor = True)
	axes.legend(['Ground Floor', '$2^{nd}$ Floor', '$3^{rd}$ Floor'], fontsize=24, frameon=False)

	locator = mdates.MonthLocator()
	myFmt = mdates.DateFormatter('%b')
	X = plt.gca().xaxis
	X.set_major_locator(locator)
	X.set_major_formatter(myFmt)

	for tick in axes.xaxis.get_major_ticks():
	      tick.label.set_fontsize(20) 
	for tick in axes.yaxis.get_major_ticks():
	      tick.label.set_fontsize(20)

	plt.ylim(10,25)
	plt.text(0.50, 0.16, 'Lower Temperature Limit',verticalalignment='bottom', horizontalalignment='right',transform=axes.transAxes, color='red', fontsize=25)
	plt.text(0.25, 0.82, 'Upper Temperature Limit',verticalalignment='bottom', horizontalalignment='right',transform=axes.transAxes, color='red', fontsize=25)
	plt.text(0.25, 0.50, 'Working Temperature Limit',verticalalignment='bottom', horizontalalignment='right',transform=axes.transAxes, color='green', fontsize=25)
	plt.axhline(y=13, color='r', linestyle='--')
	plt.axhline(y=22, color='r', linestyle='--')
	plt.axhline(y=18, color='green', linestyle='--')
	plt.savefig('Temperature.jpg', bbox_inches='tight', pad_inches=0.1)

	#plot through streamlit
	timg = Image.open("Temperature.jpg")
	st.image(timg, width=None)
		


	for i in range(3):
		st.write("")

	original_title = '<p style="font-family:Sans serif; color:cyan; font-size: 30px;"><b>Mean Air Relative Humidity in Conditioned Zones</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)

	#check if already file exists (Simulation is done)
	#if (Path('RH.jpg').is_file() is False):                
		#RH Plot creater
	fig2 = plt.figure(figsize = (24,12))
	axes1 = fig2.add_subplot(111)
	axes1.plot(df_transposed_zone1.index, df_transposed_zone1['Zone 1 RH'], color="green", linestyle='solid', label='')
	axes1.plot(df_transposed_zone2.index, df_transposed_zone2['Zone 2 RH'], color="orange", linestyle='dashed', label='')
	axes1.plot(df_transposed_zone3.index, df_transposed_zone3['Zone 3 RH'], color="blue", linestyle='dotted', label='')
	axes1.grid(axis = 'y')
	axes1.grid(axis = 'x')
	axes1.set_ylabel('Relative Humidity [%]', fontsize = 30, labelpad=20)

	fig2.tight_layout()
	axes1.autoscale(enable=True)
	axes1.set_xticks(df_transposed_zone1.index, minor = True)
	axes1.legend(['Ground Floor', '$2^{nd}$ Floor', '$3^{rd}$ Floor'], fontsize=24, frameon=False)

	locator = mdates.MonthLocator()
	myFmt = mdates.DateFormatter('%b')
	X = plt.gca().xaxis
	X.set_major_locator(locator)
	X.set_major_formatter(myFmt)

	for tick in axes1.xaxis.get_major_ticks():
	      tick.label.set_fontsize(20) 
	for tick in axes1.yaxis.get_major_ticks():
	      tick.label.set_fontsize(20)

	plt.ylim(30,70)
	plt.text(0.44, 0.08, 'Lower RH Limit',verticalalignment='bottom', horizontalalignment='right',transform=axes1.transAxes, color='red', fontsize=25)
	plt.text(0.25, 0.78, 'Upper RH Limit',verticalalignment='bottom', horizontalalignment='right',transform=axes1.transAxes, color='red', fontsize=25)
	plt.text(0.38, 0.54, 'Working RH Limit',verticalalignment='bottom', horizontalalignment='right',transform=axes1.transAxes, color='green', fontsize=25)
	plt.axhline(y=35, color='r', linestyle='--')
	plt.axhline(y=60, color='r', linestyle='--')
	plt.axhline(y=50, color='green', linestyle='--')
	plt.savefig('RH.jpg', bbox_inches='tight', pad_inches=0.1)

	#plot through streamlit
	rhimg = Image.open("RH.jpg")
	st.image(rhimg, width=None)
