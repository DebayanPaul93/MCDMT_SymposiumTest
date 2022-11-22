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

def pv_output():
	original_title = '<p style="font-family:Sans serif; color:cyan; font-size: 30px;"><b>Rooftop Photovoltaic Power Generation</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)

	if (Path('PVMonthlyProduction.jpg').is_file() is False):

		#read hourly pvpower dataframe and create monthly
		pvpowerhourly = pd.read_csv('PV Generation.csv')
		timeindex = pd.date_range(start='01/01/2021/00:00:00', end='31/12/2021/23:00:00',freq='H',tz='CET')
		pvpowerhourly.index = timeindex
		pvpowermonthly = round(pvpowerhourly.resample('M').sum())

		#plot
		monthlypvpowerfig, axes = plt.subplots(figsize = (12,6))
		n = 12
		r = np.arange(n)
		width = 0.25
		plt.bar(r, pvpowermonthly['AC Power [KWh]'], color = 'green', width = width, edgecolor = 'white')

		plt.tick_params(
		    axis='x',          # changes apply to the x-axis
		    which='both',      # both major and minor ticks are affected
		    bottom=False,      # ticks along the bottom edge are off
		    top=False)         # ticks along the top edge are off
		    #labelbottom=False) # labels along the bottom edge are off
   
		axes.spines['top'].set_visible(False)
		axes.spines['right'].set_visible(False)

		for tick in axes.yaxis.get_major_ticks():
		      tick.label.set_fontsize(20)
		        
		for tick in axes.xaxis.get_major_ticks():
		      tick.label.set_fontsize(20)
		        
		        
		plt.xticks(r,['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
		plt.ylabel('Monthly Photovoltaic Power Output [kWh]', fontsize=15, labelpad=20)
		plt.savefig('PVMonthlyProduction.jpg')

	#plot through streamlit
	pvimg = Image.open("PVMonthlyProduction.jpg")
	st.image(pvimg, width=None)

	original_title = '<p style="font-family:Sans serif; color:cyan; font-size: 30px;"><b>On-site Generation vs. Utility Demand Comparison</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)

	if (Path('OEMOEF.jpg').is_file() is False):

		#read hourly pvpower and consumption dataframe and create monthly
		pvpowerhourly = pd.read_csv('PV Generation.csv')
		consumptionhourly = pd.read_csv('total elec energy.csv')
		timeindex = pd.date_range(start='01/01/2021/00:00:00', end='31/12/2021/23:00:00',freq='H',tz='CET')
		pvpowerhourly.index = timeindex
		consumptionhourly.index = timeindex
		pvpowerdaily= round(pvpowerhourly.resample('D').sum())
		consumptiondaily= round(consumptionhourly.resample('D').sum())

		#combine two dataframes
		combineddf = pd.concat([pvpowerdaily, consumptiondaily], axis = 1)

		#OEM calculation function
		dailyoemlist, dailyoeflist = [],[]
		for index, row in combineddf.iterrows():
			gen = row['AC Power [KWh]']
			demand = row['Total Demand [kWh]']
			if(gen>demand):
				oem = 100 - (((gen - demand)/gen) * 100)
				dailyoemlist.append(oem)
			else:
				dailyoemlist.append(100)

			oef = gen/demand * 100
			dailyoeflist.append(oef)

		combineddf['Daily OEM'] = np.array(dailyoemlist)
		combineddf['Daily OEF'] = np.array(dailyoeflist)
		annual_oef = round(combineddf['AC Power [KWh]'].sum()/combineddf['Total Demand [kWh]'].sum() * 100)
		combineddf['Annual OEF'] = annual_oef

		#plot
		params = {'legend.fontsize': 12, 'xtick.labelsize': 15, 'ytick.labelsize': 15, 'axes.labelsize': 16,'axes.labelpad':15} 
		plt.rcParams.update(params)            #Updating parameters
		fig, host = plt.subplots(figsize=(18,6))
		fig.subplots_adjust(right=0.75)

		par1 = host.twinx()                                  #Twins of host axis to plot multiple yaxes in same plot

		p11, = host.plot(combineddf.index, combineddf['Daily OEM'], color='orange', linestyle='dashed', label='OEM')
		p21, = par1.plot(combineddf.index, combineddf['Daily OEF'], color='green', label='OEF', linewidth=2)


		locator = mdates.MonthLocator()
		myFmt = mdates.DateFormatter('%b')
		X = plt.gca().xaxis
		X.set_major_locator(locator)
		X.set_major_formatter(myFmt)
		host.set_ylim(0, (round(combineddf['Daily OEF'].max(),-1)))
		par1.set_ylim(0, (round(combineddf['Daily OEF'].max(),-1)))

		host.set_ylabel("Daily On-site Energy Matching (%)")
		par1.set_ylabel("Daily On-site Energy Fraction (%)")                          #Setting ylabels

		lines = [p11, p21]
		host.legend(lines, [l.get_label() for l in lines], loc='upper right', ncol=4, frameon=False)

		for ax in [par1]:
			ax.set_frame_on(True)
			ax.patch.set_visible(False)
			plt.setp(ax.spines.values(), visible=False)
			ax.spines["right"].set_visible(True)

		plt.text(0.16, 0.24, 'Annual OEF (%)',verticalalignment='bottom', horizontalalignment='right',transform=host.transAxes,color='red', fontsize=14)
		plt.axhline(y=annual_oef, color='r')
		plt.savefig('OEMOEF.jpg')

	#plot through streamlit
	oemoefimg = Image.open("OEMOEF.jpg")
	st.image(oemoefimg, width=None)
