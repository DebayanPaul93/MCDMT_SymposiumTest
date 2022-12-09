#import packages
import streamlit as st, sys
import streamlit_ext as ste
import pandas as pd
import pytz
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
    col1, col2, col3, col4, col5 = st.columns(5)
    with col5:
        language = st.selectbox("Select Language/Selecteer de taal", ['English','Nederlands'])

    if(language == 'English'):
        st.header("Welcome to Metamorforze Research Project!!")
        st.markdown('<div style="text-align: justify;">The desire to design new sustainable archive buildings is shared by the Building Performance Group of Eindhoven University of Technology (TU/e) and the National Archives of the Netherlands (NA). It is being actively pursued in a design research project granted by Metamorfoze Onderzoek under the name “Klimaatmodel Archieven Fase 2”. In this project, researchers and design engineers from TU/e and conservators from NA work on the mutual aim to develop a user-friendly decision-support tool for stakeholders and policy enablers involved in the early design stages of archive buildings.</div>', unsafe_allow_html=True)
        st.text("")
        st.text("")
        st.markdown('<div style="text-align: justify;">The design project commenced in March 2021 and is aimed to be completed by March 2023. Currently, we are at the stage of finding the appropriate inputs and outputs of the tool through performing simulations with the help and advice of several domain experts in the field. We are open to and appreciate any ideas and suggestions for improving the tool to make it as useful and user-friendly as possible.</div>', unsafe_allow_html=True)
        st.text("")
        st.text("")
        dstimg = Image.open("DST.png")

    elif(language == 'Nederlands'):
        st.header("Welkom bij Metamorforze Onderzoek Project!!")
        st.markdown('<div style="text-align: justify;">De wens om nieuwe duurzame archiefgebouwen te ontwerpen wordt gedeeld door de Building Performance Group van de Technische Universiteit Eindhoven (TU/e) en het Nationaal Archief Nederland (NA). Dit wordt actief nagestreefd in een door Metamorfoze Onderzoek toegekend ontwerponderzoeksproject onder de naam "Klimaatmodel Archieven Fase 2". In dit project werken onderzoekers en ontwerpers van de TU/e en conservatoren van het NA aan het gezamenlijke doel om een gebruiksvriendelijke beslissingsondersteunende tool te ontwikkelen voor belanghebbenden en beleidsmakers die betrokken zijn bij de vroege ontwerpfasen van archiefgebouwen.</div>', unsafe_allow_html=True)
        st.text("")
        st.text("")
        st.markdown('<div style="text-align: justify;">Het ontwerpproject ging in maart 2021 van start en zou in maart 2023 voltooid moeten zijn. Momenteel zijn wij bezig met het vinden van de juiste inputs en outputs van het instrument door simulaties uit te voeren met de hulp en het advies van verscheidene domeinexperts op dit gebied. Wij staan open voor en waarderen alle ideeën en suggesties voor het verbeteren van het instrument om het zo nuttig en gebruiksvriendelijk mogelijk te maken.</div>', unsafe_allow_html=True)
        st.text("")
        st.text("")
        dstimg = Image.open("DST.png")


    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        if (language == 'English'):
            st.image(dstimg, caption='Infographics of the features of Decision Support Tool', width = None)            #Centering the image
        elif(language == 'Nederlands'):
            st.image(dstimg, caption='Infografieken van de kenmerken van het beslissingsondersteunend instrument', width = None)            #Centering the image
    with col3:
        st.write("")

    col4, col5, col6 = st.columns(3)
    with col4:
        if(language == 'English'):
            name = ste.text_input("Enter your Name")
        elif(language == 'Nederlands'):
            name = ste.text_input("Voer uw naam in")
    with col5:
        if(language == 'English'):
            date = ste.date_input("Enter Date",value=datetime.today())
        elif(language == 'Nederlands'):
            date = ste.date_input("Voer datum in",value=datetime.today())
        date_report = date.strftime('%d %B, %Y') 
    with col6:
        cet = pytz.timezone('Europe/Amsterdam')
        if (date_report == datetime.today().strftime('%d %B, %Y')): 
            if(language == 'English'):
                time = ste.time_input("Enter Time", value= datetime.now(tz=cet), disabled=True) 
            elif(language == 'Nederlands'):
                time = ste.time_input("Voer tijd in", value= datetime.now(tz=cet), disabled=True)     
            time_report = time.strftime("%I:%M %p")
        else:
            if(language == 'English'):
                time = ste.time_input("Enter Time", value= datetime.now(tz=cet), disabled=False) 
            elif(language == 'Nederlands'):
                time = ste.time_input("Voer tijd in", value= datetime.now(tz=cet), disabled=False)     
            time_report = time.strftime("%I:%M %p")

    if(language == 'English'):
        st.write("Report Date & Time: {} {} (Amsterdam Time)".format(date_report,time_report)+", created by "+name)
    elif(language == 'Nederlands'):
        st.write("Verslag Datum & Tijd: {} {} (Amsterdam Tijd)".format(date_report,time_report)+", gemaakt door "+name)  

    if 'reporttime' or 'reportdate' or 'name' not in st.session_state:
        st.session_state.reporttime = time_report
        st.session_state.reportdate = date_report
        st.session_state.name = name

                                            

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

