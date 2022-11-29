import streamlit as st,sys
from pathlib import Path
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

def trh_output():
	# st.expander('Mean Air Temperature in Conditioned Zones', expanded=False)
	# original_title = '<p style="font-family:Sans serif; color:cyan; font-size: 30px;"><b>Mean Air Temperature in Conditioned Zones</b></p>'
	# st.markdown(original_title, unsafe_allow_html=True)
	expander = st.expander("Mean Air Temperature & Relative Humidity in Conditioned Zones", expanded=False)
	expander.write("")

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
	dd, data = esr.read('3_zonesnew.eso')
	for var in list_variables:
	    for i in range(3):
	        frequency, key, variable = dd.find_variable(var)[i] 
	        idx = dd.index[frequency, key, variable]
	        hourly_temptime_series = data[idx]
	        list_hourlyoutput.append(hourly_temptime_series)
    
	df = pd.DataFrame(list_hourlyoutput)
	df_transposed = df.transpose()
	df_transposed.columns = list_columnnames
	timeindex = pd.date_range(start='01/01/2021/00:00:00', end='31/12/2021/23:00:00',freq='H')
	df_transposed.index = timeindex
	list_highTavg, list_highRHavg = [],[]

	if(no_of_zones == 1):
		df_transposed_zone1 = df_transposed[['Zone 1 T','Zone 1 RH']]
		highTavg1=round((len(df_transposed_zone1[df_transposed_zone1['Zone 1 T'] > 18.1])/8760 * 100),1)               #0.1 more than annual avergae T setpoint, need to read
		list_highTavg1.append(highTavg)
		highRHavg1=round((len(df_transposed_zone1[df_transposed_zone1['Zone 1 RH'] > 50.1])/8760 * 100),1)              #0.1 more than annual avergae RH setpoint, need to read
		list_highRHavg.append(highRHavg1)


	elif(no_of_zones == 2):
		df_transposed_zone1 = df_transposed[['Zone 1 T','Zone 1 RH']]
		df_transposed_zone2 = df_transposed[['Zone 2 T','Zone 2 RH']]
		highTavg1=round((len(df_transposed_zone1[df_transposed_zone1['Zone 1 T'] > 18.1])/8760 * 100),1)
		highTavg2=round((len(df_transposed_zone1[df_transposed_zone2['Zone 2 T'] > 18.1])/8760 * 100),1)
		list_highTavg.append(highTavg1)
		list_highTavg.append(highTavg2)
		highRHavg1=round((len(df_transposed_zone1[df_transposed_zone1['Zone 1 RH'] > 50.1])/8760 * 100),1) 
		highRHavg2=round((len(df_transposed_zone1[df_transposed_zone2['Zone 2 RH'] > 50.1])/8760 * 100),1) 
		list_highRHavg.append(highRHavg1)
		list_highRHavg.append(highRHavg2)

	else:
		df_transposed_zone1 = df_transposed[['Zone 1 T','Zone 1 RH']]
		df_transposed_zone2 = df_transposed[['Zone 2 T','Zone 2 RH']]
		df_transposed_zone3 = df_transposed[['Zone 3 T','Zone 3 RH']]
		highTavg1=round((len(df_transposed_zone1[df_transposed_zone1['Zone 1 T'] > 18.1])/8760 * 100),1) 
		highTavg2=round((len(df_transposed_zone1[df_transposed_zone2['Zone 2 T'] > 18.1])/8760 * 100),1) 
		highTavg3=round((len(df_transposed_zone1[df_transposed_zone3['Zone 3 T'] > 18.1])/8760 * 100),1) 
		list_highTavg.append(highTavg1)
		list_highTavg.append(highTavg2)
		list_highTavg.append(highTavg3)
		highRHavg1=round((len(df_transposed_zone1[df_transposed_zone1['Zone 1 RH'] > 50.1])/8760 * 100),1) 
		highRHavg2=round((len(df_transposed_zone1[df_transposed_zone2['Zone 2 RH'] > 50.1])/8760 * 100),1) 
		highRHavg3=round((len(df_transposed_zone1[df_transposed_zone3['Zone 3 RH'] > 50.1])/8760 * 100),1) 
		list_highRHavg.append(highRHavg1)
		list_highRHavg.append(highRHavg2)
		list_highRHavg.append(highRHavg3)


	#check if already file exists (Simulation is done)
	if (Path('Temperature.jpg').is_file() is False):        
		#T Plot creater
		fig1 = plt.figure(figsize = (24,12))
		axes = fig1.add_subplot(111)
		if(no_of_zones == 1):
			axes.plot(df_transposed_zone1.index, df_transposed_zone1['Zone 1 T'], color="green", linestyle='solid', label='')
		elif(no_of_zones == 2):
			axes.plot(df_transposed_zone1.index, df_transposed_zone1['Zone 1 T'], color="green", linestyle='solid', label='')
			axes.plot(df_transposed_zone2.index, df_transposed_zone2['Zone 2 T'], color="orange", linestyle='dashed', label='')
			axes.legend(['Ground Floor', 'Middle Floor'], fontsize=24, frameon=False)
		else:
			axes.plot(df_transposed_zone1.index, df_transposed_zone1['Zone 1 T'], color="green", linestyle='solid', label='')
			axes.plot(df_transposed_zone2.index, df_transposed_zone2['Zone 2 T'], color="orange", linestyle='dashed', label='')
			axes.plot(df_transposed_zone3.index, df_transposed_zone3['Zone 3 T'], color="blue", linestyle='dotted', label='')
			axes.legend(['Ground Floor', 'Middle Floor', 'Top Floor'], fontsize=24, frameon=False)

		axes.grid(axis = 'y')
		axes.grid(axis = 'x')
		axes.set_ylabel('Temperature [°C]', fontsize = 30, labelpad=20)

		fig1.tight_layout()
		axes.autoscale(enable=True)
		axes.set_xticks(df_transposed_zone1.index, minor = True)

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
		plt.text(0.25, 0.50, 'Annual Average Temperature Setpoint',verticalalignment='bottom', horizontalalignment='right',transform=axes.transAxes, color='green', fontsize=25)
		plt.axhline(y=13, color='r', linestyle='--')
		plt.axhline(y=22, color='r', linestyle='--')
		plt.axhline(y=18, color='green', linestyle='--')
		plt.savefig('Temperature.jpg', bbox_inches='tight', pad_inches=0.1)

	#plot through streamlit
	timg = Image.open("Temperature.jpg")
	#expander.image(timg)
	#st.image(timg, width=None)
		


	# for i in range(3):
	# 	st.write("")

	# original_title = '<p style="font-family:Sans serif; color:cyan; font-size: 30px;"><b>Mean Air Relative Humidity in Conditioned Zones</b></p>'
	# st.markdown(original_title, unsafe_allow_html=True)

	#check if already file exists (Simulation is done)
	if (Path('RH.jpg').is_file() is False):                
		#RH Plot creater
		fig2 = plt.figure(figsize = (24,12))
		axes1 = fig2.add_subplot(111)
		if(no_of_zones == 1):
			axes1.plot(df_transposed_zone1.index, df_transposed_zone1['Zone 1 RH'], color="green", linestyle='solid', label='')
		elif(no_of_zones == 2):
			axes1.plot(df_transposed_zone1.index, df_transposed_zone1['Zone 1 RH'], color="green", linestyle='solid', label='')
			axes1.plot(df_transposed_zone2.index, df_transposed_zone2['Zone 2 RH'], color="orange", linestyle='dashed', label='')
			axes1.legend(['Ground Floor', '$2^{nd}$ Floor'], fontsize=24, frameon=False)
		else:
			axes1.plot(df_transposed_zone1.index, df_transposed_zone1['Zone 1 RH'], color="green", linestyle='solid', label='')
			axes1.plot(df_transposed_zone2.index, df_transposed_zone2['Zone 2 RH'], color="orange", linestyle='dashed', label='')
			axes1.plot(df_transposed_zone3.index, df_transposed_zone3['Zone 3 RH'], color="blue", linestyle='dotted', label='')
			axes1.legend(['Ground Floor', 'Middle Floor', 'Top Floor'], fontsize=24, frameon=False)
		
		axes1.grid(axis = 'y')
		axes1.grid(axis = 'x')
		axes1.set_ylabel('Relative Humidity [%]', fontsize = 30, labelpad=20)

		fig2.tight_layout()
		axes1.autoscale(enable=True)
		axes1.set_xticks(df_transposed_zone1.index, minor = True)

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
		plt.text(0.44, 0.08, 'Lower Relative Humidity Limit',verticalalignment='bottom', horizontalalignment='right',transform=axes1.transAxes, color='red', fontsize=25)
		plt.text(0.25, 0.78, 'Upper Relative Humidity Limit',verticalalignment='bottom', horizontalalignment='right',transform=axes1.transAxes, color='red', fontsize=25)
		plt.text(0.65, 0.54, 'Annual Average Relative Humidity Setpoint',verticalalignment='bottom', horizontalalignment='right',transform=axes1.transAxes, color='green', fontsize=25)
		plt.axhline(y=35, color='r', linestyle='--')
		plt.axhline(y=60, color='r', linestyle='--')
		plt.axhline(y=50, color='green', linestyle='--')
		plt.savefig('RH.jpg', bbox_inches='tight', pad_inches=0.1)

	#plot through streamlit
	rhimg = Image.open("RH.jpg")
	#st.image(rhimg, width=None)

	col_T, col_RH = st.columns(2)
	
	with col_T:
		expander1 = st.expander("Temperature", expanded=False)
		expander1.image(timg)
	with col_RH:
		expander2 = st.expander("Relative Humidity", expanded=False)
		expander2.image(rhimg)

	expander = st.expander("Yearly Percentage of Hours above Annual Average Temperature Setpoint", expanded=False)
	expander.write("")

	if(no_of_zones == 1):
		col1, col2, col3 = st.columns(3)
		with col1:
			st.write("")
		with col2:
			expander2 = st.expander("Ground Floor", expanded=False)
			expander2.metric(label="", value=str(list_highTavg[0])+ "%")
		with col3:
			st.write("")

		expander = st.expander("Yearly Percentage of Hours above Annual Average Relative Humidity Setpoint", expanded=False)
		expander.write("")

		col1, col2, col3 = st.columns(3)
		with col1:
			st.write("")
		with col2:
			expander2 = st.expander("Ground Floor", expanded=False)
			expander2.metric(label="", value=str(list_highRHavg[0])+ "%")
		with col3:
			st.write("")

	elif(no_of_zones == 2):
		col1, col2 = st.columns(2)
		with col1:
			expander1 = st.expander("Ground Floor", expanded=False)
			expander1.metric(label="", value=str(list_highTavg[0])+ "%")
		with col2:
			expander2 = st.expander("Middle Floor", expanded=False)
			deltaT1 = list_highTavg[1] - list_highTavg[0]
			deltaT1 = round(deltaT1,1)
			if(deltaT1<0):
				expander2.metric(label="", value=str(list_highTavg[1])+ "%", delta=deltaT1, delta_color="inverse")
			else:
				expander2.metric(label="", value=str(list_highTavg[1])+ "%", delta=deltaT1)

		expander = st.expander("Yearly Number of Hours above Annual Average Relative Humidity Setpoint", expanded=False)
		expander.write("")

		col1, col2 = st.columns(2)
		with col1:
			expander1 = st.expander("Ground Floor", expanded=False)
			expander1.metric(label="", value=str(list_highRHavg[0])+ "%")
		with col2:
			expander2 = st.expander("Middle Floor", expanded=False)
			deltaRH1 = list_highRHavg[1] - list_highRHavg[0]
			deltaRH1 = round(deltaRH1,1)
			if(deltaRH1<0):
				expander2.metric(label="", value=str(list_highRHavg[1])+ "%", delta=deltaRH1, delta_color="inverse")
			else:
				expander2.metric(label="", value=str(list_highRHavg[1])+ "%", delta=deltaRH1)

	else:
		col1, col2, col3 = st.columns(3)
		with col1:
			expander1 = st.expander("Ground Floor", expanded=False)
			expander1.metric(label="", value=str(list_highTavg[0])+ "%", delta="-", delta_color="off")
		with col2:
			expander2 = st.expander("Middle Floor", expanded=False)
			deltaT1 = list_highTavg[1] - list_highTavg[0]
			deltaT1 = round(deltaT1,1)
			if(deltaT1<0):
				expander2.metric(label="", value=str(list_highTavg[1])+ "%", delta=deltaT1, delta_color="inverse")
			else:
				expander2.metric(label="", value=str(list_highTavg[1])+ "%", delta=deltaT1)
		with col3:
			expander3 = st.expander("Top Floor", expanded=False)
			deltaT2 = list_highTavg[2] - list_highTavg[1]
			deltaT2 = round(deltaT2,1)
			if(deltaT2<0):	
				expander3.metric(label="", value=str(list_highTavg[2])+ "%", delta=deltaT2, delta_color="inverse")
			else:
				expander3.metric(label="", value=str(list_highTavg[2])+ "%", delta=deltaT2)

		expander = st.expander("Yearly Number of Hours above Annual Average Relative Humidity Setpoint", expanded=False)
		expander.write("")

		col1, col2, col3 = st.columns(3)
		with col1:
			expander1 = st.expander("Ground Floor", expanded=False)
			expander1.metric(label="", value=str(list_highRHavg[0])+ "%", delta="-", delta_color="off")
		with col2:
			expander2 = st.expander("Middle Floor", expanded=False)
			deltaRH1 = list_highRHavg[1] - list_highRHavg[0]
			deltaRH1 = round(deltaRH1,1)
			if(deltaRH1<0):
				expander2.metric(label="", value=str(list_highRHavg[1])+ "%", delta=deltaRH1, delta_color="inverse")
			else:
				expander2.metric(label="", value=str(list_highRHavg[1])+ "%", delta=deltaRH1)
		with col3:
			expander3 = st.expander("Top Floor", expanded=False)
			deltaRH2 = list_highRHavg[2] - list_highRHavg[1]
			deltaRH2 = round(deltaRH2,1)
			if(deltaRH2<0):	
				expander3.metric(label="", value=str(list_highRHavg[2])+ "%", delta=deltaRH2, delta_color="inverse")
			else:
				expander3.metric(label="", value=str(list_highRHavg[2])+ "%", delta=deltaRH2)










	
