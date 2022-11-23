#import packages
import streamlit as st, sys
import pandas as pd
from datetime import datetime
from PIL import Image
#import tkinter as tk
#from tkinter import filedialog


#Remove Watermark & Styling
st.set_page_config(page_title='Multi-criteria Decision Support Tool')
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            .sidebar-text {font-size:12px;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)
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


#import files
import Inputpages.weather
import Inputpages.paper
import Inputpages.repository
import Inputpages.construction
import Inputpages.setpoint
import Inputpages.hvac
import Inputpages.pv
import Inputpages.result

###Adding multiple input pages

def input_home_page():
    st.header("Welcome to Metamorforze Project!!")
    st.markdown('<div style="text-align: justify;">The desire to design new sustainable archive buildings is shared by the Building Performance Group of Eindhoven University of Technology (TU/e) and the National Archives of the Netherlands (NA). It is being actively pursued in a design research project granted by Metamorfoze Onderzoek under the name “Klimaatmodel Archieven Fase 2”. In this project, researchers and design engineers from TU/e and conservators from NA work on the mutual aim to develop a user-friendly decision-support tool for stakeholders and policy enablers involved in the early design stages of archive buildings.</div>', unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.markdown('<div style="text-align: justify;">The design project commenced in March 2021 and is aimed to be completed by March 2023. Currently, we are at the stage of finding the appropriate inputs and outputs of the tool through performing simulations with the help and advice of several domain experts in the field. We are open to and appreciate any ideas and suggestions for improving the tool to make it as useful and user-friendly as possible. </div>', unsafe_allow_html=True)
    st.text("")
    st.text("")
    dstimg = Image.open("DST.png")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        st.image(dstimg, caption='Infographics of the features of Decision Support Tool', width = None)            #Centering the image
    with col3:
        st.write("")

    col4, col5, col6, col7 = st.columns(4)
    with col4:
        name = st.text_input("Enter your Name")
    with col5:
        date = st.date_input("Enter Date",value=datetime.today()) 
        date_report = date.strftime('%d %B, %Y') 
    with col6:
        if (date_report == datetime.today().strftime('%d %B, %Y')): 
            time = st.time_input("Enter Time", value= datetime.now(), disabled=True)      
            time_report = time.strftime("%H:%M %p %Z")
        else:
            time = st.time_input("Enter Time", value= datetime.now(), disabled=False)      
            time_report = time.strftime("%H:%M %p %Z")
    with col7:
        email = st.text_input("Enter your e-mail id")

    st.write("Report Date & Time: {} {}".format(date_report,time_report))
#     st.markdown('#### Please select the Folder of Simulation Files in your System')
#     # Directory picker
#     root = tk.Tk()
#     root.withdraw()

#     # Make folder picker dialog appear on top of other windows
#     root.wm_attributes('-topmost', 1)

#     # Folder picker button
#     source_folderlocation_string, modified_folderlocation_string = "",""

#     clicked = st.button('Select Folder')
#     if clicked:
#         source_folderlocation_string = filedialog.askdirectory(master=root)                               #for reading folder from user system
#         if(source_folderlocation_string != ""):
#             st.text_input('You Selected Folder:', source_folderlocation_string)
#             modified_folderlocation_string = source_folderlocation_string.replace("/", "\\") 
#         else:
#             st.error("Please Select the Folder") 

                                            

def weather_page():
    Inputpages.weather.weather_input()

def paper_page():
    Inputpages.paper.paper_input()

def reposize_page():
    Inputpages.repository.size_input()

def construction_page():
    Inputpages.construction.construction_input()

def setpoint_page():
    Inputpages.setpoint.setpoint_input()

def hvac_page():
    Inputpages.hvac.hvac_input()

def pv_page():
    Inputpages.pv.pv_input()

buttonclickcheck = Inputpages.pv.buttonclickconfirm
if(buttonclickcheck):
    def result_page():
        Inputpages.result.resultmenu()

    inputpage_names_to_funcs = {
        "🏠   Home": input_home_page,
        "🌦   Weather Info": weather_page,
        "📜   Collection Chemical Properties": paper_page,
        "📏   Repository Sizing": reposize_page,
        "🧱   Building Construction Properties": construction_page,
        "🌡️    Annual Setpoints Limit": setpoint_page,
        "🔥❄️ HVAC Systems": hvac_page,
        "☀️🔋 Rooftop PV Info": pv_page,
        "🔚   Result": result_page,
    }


else:
    inputpage_names_to_funcs = {
        "🏠   Home": input_home_page,
        "🌦   Weather Info": weather_page,
        "📜   Collection Chemical Properties": paper_page,
        "📏   Repository Sizing": reposize_page,
        "🧱   Building Construction Properties": construction_page,
        "🌡️    Annual Setpoints Limit": setpoint_page,
        "🔥❄️ HVAC Systems": hvac_page,
        "☀️🔋 Rooftop PV Info": pv_page,
    }

selected_page = st.sidebar.selectbox("", inputpage_names_to_funcs.keys(),key='Page')
inputpage_names_to_funcs[selected_page]()

