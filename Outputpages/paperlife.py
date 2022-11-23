import streamlit as st,sys, math
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

def paperlife_output():
    # original_title = '<p style="font-family:Sans serif; color:cyan; font-size: 30px;"><b>Relative Lifetime of Collection</b></p>'
    # st.markdown(original_title, unsafe_allow_html=True)
    expander = st.expander("Relative Lifetime of Collection", expanded=False)

    no_of_zones = 3           # find this from zone calcualtion
    ph_paper = 8.0
    DP_0, DP = 1200,200       # find this from paper chemical values

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
    list_t_avg,list_life_multiplier = [],[]

    if(no_of_zones == 1):
        df_transposed_zone1 = df_transposed[['Zone 1 T','Zone 1 RH']]
        
        df_transposed_zone1['Vw_Strlic'] = pow(np.log(1-df_transposed_zone1['Zone 1 RH']/100)/(1.67*(df_transposed_zone1['Zone 1 T'])-285.655),1/(2.491-0.012*(df_transposed_zone1['Zone 1 T'])))
        list_k_strlic1 = []
        for index,row in df_transposed_zone1.iterrows():
            Vw_Strlic = row['Vw_Strlic']
            air_temp = row['Zone 1 T']
            k_strlic = math.exp(36.981 + 36.72*Vw_Strlic+0.244*np.log(pow(10,-ph_paper))-14300/(air_temp+273.15))
            list_k_strlic.append(k_strlic)
        df_transposed_zone1['k_Strlic'] = list_k_strlic1
        df_transposed_zone1['t[year]'] = ((1/DP-1/DP_0)*(1/df_transposed_zone1['k_Strlic']))
        t_avg = round(df_transposed_zone1['t[year]'].mean())
        list_t_avg.append(t_avg)
        t_k = round(((1/DP-1/DP_0)*(1/df_transposed_zone1['k_Strlic'].mean())))
        life_multiplier = round(t_k/((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15))))),2)
        list_life_multiplier.append(life_multiplier)
        t_k20by50 = round((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15)))))
        df_transposed_zone1['relative_lifetime'] = df_transposed_zone1['t[year]']/t_k20by50 
    
    
    elif(no_of_zones == 2):
        df_transposed_zone1 = df_transposed[['Zone 1 T','Zone 1 RH']]
        df_transposed_zone2 = df_transposed[['Zone 2 T','Zone 2 RH']]
        
        df_transposed_zone1['Vw_Strlic'] = pow(np.log(1-df_transposed_zone1['Zone 1 RH']/100)/(1.67*(df_transposed_zone1['Zone 1 T'])-285.655),1/(2.491-0.012*(df_transposed_zone1['Zone 1 T'])))
        list_k_strlic1 = []
        for index,row in df_transposed_zone1.iterrows():
            Vw_Strlic = row['Vw_Strlic']
            air_temp = row['Zone 1 T']
            k_strlic = math.exp(36.981 + 36.72*Vw_Strlic+0.244*np.log(pow(10,-ph_paper))-14300/(air_temp+273.15))
            list_k_strlic1.append(k_strlic)
        df_transposed_zone1['k_Strlic'] = list_k_strlic1
        df_transposed_zone1['t[year]'] = ((1/DP-1/DP_0)*(1/df_transposed_zone1['k_Strlic']))
        t_avg = round(df_transposed_zone1['t[year]'].mean())
        list_t_avg.append(t_avg)
        t_k = round(((1/DP-1/DP_0)*(1/df_transposed_zone1['k_Strlic'].mean())))
        life_multiplier = round(t_k/((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15))))),2)
        list_life_multiplier.append(life_multiplier)
        t_k20by50 = round((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15)))))
        df_transposed_zone1['relative_lifetime'] = df_transposed_zone1['t[year]']/t_k20by50
        
        df_transposed_zone2['Vw_Strlic'] = pow(np.log(1-df_transposed_zone2['Zone 2 RH']/100)/(1.67*(df_transposed_zone2['Zone 2 T'])-285.655),1/(2.491-0.012*(df_transposed_zone2['Zone 2 T'])))
        list_k_strlic2 = []
        for index,row in df_transposed_zone2.iterrows():
            Vw_Strlic = row['Vw_Strlic']
            air_temp = row['Zone 2 T']
            k_strlic = math.exp(36.981 + 36.72*Vw_Strlic+0.244*np.log(pow(10,-ph_paper))-14300/(air_temp+273.15))
            list_k_strlic2.append(k_strlic)
        df_transposed_zone2['k_Strlic'] = list_k_strlic2
        df_transposed_zone2['t[year]'] = ((1/DP-1/DP_0)*(1/df_transposed_zone2['k_Strlic']))
        t_avg = round(df_transposed_zone2['t[year]'].mean())
        list_t_avg.append(t_avg)
        t_k = round(((1/DP-1/DP_0)*(1/df_transposed_zone2['k_Strlic'].mean())))
        life_multiplier = round(t_k/((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15))))),2)
        list_life_multiplier.append(life_multiplier)
        t_k20by50 = round((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15)))))
        df_transposed_zone1['relative_lifetime'] = df_transposed_zone2['t[year]']/t_k20by50
    
    else:
        df_transposed_zone1 = df_transposed[['Zone 1 T','Zone 1 RH']]
        df_transposed_zone2 = df_transposed[['Zone 2 T','Zone 2 RH']]
        df_transposed_zone3 = df_transposed[['Zone 3 T','Zone 3 RH']]
        
        df_transposed_zone1['Vw_Strlic'] = pow(np.log(1-df_transposed_zone1['Zone 1 RH']/100)/(1.67*(df_transposed_zone1['Zone 1 T'])-285.655),1/(2.491-0.012*(df_transposed_zone1['Zone 1 T'])))
        list_k_strlic1 = []
        for index,row in df_transposed_zone1.iterrows():
            Vw_Strlic = row['Vw_Strlic']
            air_temp = row['Zone 1 T']
            k_strlic = math.exp(36.981 + 36.72*Vw_Strlic+0.244*np.log(pow(10,-ph_paper))-14300/(air_temp+273.15))
            list_k_strlic1.append(k_strlic)
        df_transposed_zone1['k_Strlic'] = list_k_strlic1
        df_transposed_zone1['t[year]'] = ((1/DP-1/DP_0)*(1/df_transposed_zone1['k_Strlic']))
        t_avg = round(df_transposed_zone1['t[year]'].mean())
        list_t_avg.append(t_avg)
        t_k = round(((1/DP-1/DP_0)*(1/df_transposed_zone1['k_Strlic'].mean())))
        life_multiplier = round(t_k/((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15))))),2)
        list_life_multiplier.append(life_multiplier)
        t_k20by50 = round((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15)))))
        df_transposed_zone1['relative_lifetime'] = df_transposed_zone1['t[year]']/t_k20by50
        
        df_transposed_zone2['Vw_Strlic'] = pow(np.log(1-df_transposed_zone2['Zone 2 RH']/100)/(1.67*(df_transposed_zone2['Zone 2 T'])-285.655),1/(2.491-0.012*(df_transposed_zone2['Zone 2 T'])))
        list_k_strlic2 = []
        for index,row in df_transposed_zone2.iterrows():
            Vw_Strlic = row['Vw_Strlic']
            air_temp = row['Zone 2 T']
            k_strlic = math.exp(36.981 + 36.72*Vw_Strlic+0.244*np.log(pow(10,-ph_paper))-14300/(air_temp+273.15))
            list_k_strlic2.append(k_strlic)
        df_transposed_zone2['k_Strlic'] = list_k_strlic2
        df_transposed_zone2['t[year]'] = ((1/DP-1/DP_0)*(1/df_transposed_zone2['k_Strlic']))
        t_avg = round(df_transposed_zone2['t[year]'].mean())
        list_t_avg.append(t_avg)
        t_k = round(((1/DP-1/DP_0)*(1/df_transposed_zone2['k_Strlic'].mean())))
        life_multiplier = round(t_k/((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15))))),2)
        list_life_multiplier.append(life_multiplier)
        t_k20by50 = round((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15)))))
        df_transposed_zone2['relative_lifetime'] = df_transposed_zone2['t[year]']/t_k20by50
        
        df_transposed_zone3['Vw_Strlic'] = pow(np.log(1-df_transposed_zone3['Zone 3 RH']/100)/(1.67*(df_transposed_zone3['Zone 3 T'])-285.655),1/(2.491-0.012*(df_transposed_zone3['Zone 3 T'])))
        list_k_strlic3 = []
        for index,row in df_transposed_zone3.iterrows():
            Vw_Strlic = row['Vw_Strlic']
            air_temp = row['Zone 3 T']
            k_strlic = math.exp(36.981 + 36.72*Vw_Strlic+0.244*np.log(pow(10,-ph_paper))-14300/(air_temp+273.15))
            list_k_strlic3.append(k_strlic)
        df_transposed_zone3['k_Strlic'] = list_k_strlic3
        df_transposed_zone3['t[year]'] = ((1/DP-1/DP_0)*(1/df_transposed_zone3['k_Strlic']))
        t_avg = round(df_transposed_zone3['t[year]'].mean())
        list_t_avg.append(t_avg)
        t_k = round(((1/DP-1/DP_0)*(1/df_transposed_zone3['k_Strlic'].mean())))
        life_multiplier = round(t_k/((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15))))),2)
        list_life_multiplier.append(life_multiplier)
        t_k20by50 = round((1/DP-1/DP_0)*(1/(math.exp(36.981 + 36.72*(pow(np.log(1-50/100)/(1.67*(20)-285.655),1/(2.491-0.012*(20))))+0.244*np.log(pow(10,-ph_paper))-14300/(20+273.15)))))
        df_transposed_zone3['relative_lifetime'] = df_transposed_zone3['t[year]']/t_k20by50

        #check if already file exists (Simulation is done)
        if (Path('CollectionRelativeLifeTime.jpg').is_file() is False):
            #T Plot creater
            fig1 = plt.figure(figsize = (24,12))
            axes = fig1.add_subplot(111)
            if(no_of_zones == 1):
                axes.plot(df_transposed_zone1.index, df_transposed_zone1['relative_lifetime'], color="green", linestyle='solid', label='')
            elif(no_of_zones == 2):
                axes.plot(df_transposed_zone1.index, df_transposed_zone1['relative_lifetime'], color="green", linestyle='solid', label='')
                axes.plot(df_transposed_zone2.index, df_transposed_zone2['relative_lifetime'], color="orange", linestyle='dashed', label='')
                axes.legend(['Ground Floor', 'Middle Floor',], fontsize=24, frameon=False)
            else:
                axes.plot(df_transposed_zone1.index, df_transposed_zone1['relative_lifetime'], color="green", linestyle='solid', label='')
                axes.plot(df_transposed_zone2.index, df_transposed_zone2['relative_lifetime'], color="orange", linestyle='dashed', label='')
                axes.plot(df_transposed_zone3.index, df_transposed_zone3['relative_lifetime'], color="blue", linestyle='dotted', label='')
                axes.legend(['Ground Floor', 'Middle Floor', 'Top Floor'], fontsize=24, frameon=False)
            
            axes.grid(axis = 'y')
            axes.grid(axis = 'x')
            axes.set_ylabel('Relative Lifetime', fontsize = 30, labelpad=20)

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
            
            plt.ylim(0,5)
            plt.savefig('CollectionRelativeLifeTime.jpg', bbox_inches='tight', pad_inches=0.1)

        #plot through streamlit
        paperlifetimeimg = Image.open("CollectionRelativeLifeTime.jpg")
        #st.image(paperlifetimeimg, width=None)
        expander.image(paperlifetimeimg)

    expander = st.expander("Collection LifeSpan (in Years)", expanded=False)
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

        expander = st.expander("Yearly Number of Hours above Annual Average Relative Humidity Setpoint", expanded=False)
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
            deltaY1 = list_t_avg[1] - list_t_avg[0]
            deltaY1 = round(deltaY1/list_t_avg[0] * 100, 1)
            if(deltaY1<0):
                expander2.metric(label="", value=str(list_t_avg[1]), delta=str(deltaY1) +"%", delta_color="inverse")
            else:
                expander2.metric(label="", value=str(list_t_avg[1]), delta=str(deltaY1) +"%")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            expander1 = st.expander("Ground Floor", expanded=False)
            expander1.metric(label="", value=str(list_t_avg[0]), delta="-", delta_color="off")
        with col2:
            expander2 = st.expander("Middle Floor", expanded=False)
            deltaY1 = list_t_avg[1] - list_t_avg[0]
            deltaY1 = round(deltaY1/list_t_avg[0] * 100, 1)
            if(deltaY1<0):
                expander2.metric(label="", value=str(list_t_avg[1]), delta=str(deltaY1) +"%", delta_color="inverse")
            else:
                expander2.metric(label="", value=str(list_t_avg[1]), delta=str(deltaY1) +"%")
        with col3:
            expander3 = st.expander("Top Floor", expanded=False)
            deltaY2 = list_t_avg[2] - list_t_avg[1]
            deltaY2 = round(deltaY2/list_t_avg[1] * 100, 1)
            if(deltaY2<0):  
                expander3.metric(label="", value=str(list_t_avg[2]), delta=str(deltaY2) +"%", delta_color="inverse")
            else:
                expander3.metric(label="", value=str(list_t_avg[2]), delta=str(deltaY2) +"%")


       
