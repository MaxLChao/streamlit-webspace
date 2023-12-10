import streamlit as st
from streamlit.logger import get_logger
import numpy as np
import pandas as pd
import time
#import plotly.express as px

# streamlit timeline
import streamlit as st
from streamlit_timeline import timeline
import json

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(layout="wide")
    tab1, tab2, tab3 = st.tabs(["Background", "Cohort Description", "Patient History"])
    with tab1:
        st.header("Background")
        st.markdown("""
            ### For BMI530

            Data collected via Janos Hajagos, and given to us as is from Professor Tengfei Ma. Data was originally used to model for length of stay. All data has been clearly deidentified and personal information including addresses and exact birthdates have been removed. 

            Modeling of age and other data has instead been estimated via the birthyear and occurence date. Due to large file sizes, this app has taken a subselection of data and is only displaying small portions of the data instead of the totality. Files and app are available via this [Link](https://github.com/MaxLChao/streamlit-webspace). 

            
            For the purpose of our project we did an analysis of what were the driving causes of death in this cohort of patients. Here we used a few csv's that were provided:
            1. Person.csv: a deidentified csv that provided information about the patient including birthdate, sex, and race.
            2. Measurments.csv: Grabbed a subselection of 1 million rows of measurements that were taken for the patients in the person.csv that included information on measurements taken during occurences or visits.
            3. Condition Occurrence csv: a csv that describes conditions of all the patients based on occurences. Can have multiple maps of occurences to a single patient across single and many visitations.

            Our goal is to visualize basic information of the cohort and identify any features that were common across the deaths.


            ## Cleaning up person.csv

            ## Cleaning up measurements.csv

            ## Cleaning up condition_occurence.csv


            """)
    with tab2:
        st.header("Cohort Description")
    with tab3:
        st.header("Patient History")
        option = st.selectbox(
                "Select a patient ID:", 
                ("4", "36855", "8933",  "4084", "25990", "23594"))
        file = 'json/'+option+'.json'
        with open(file, "r") as f:
    	    data = f.read()
        timeline(data, height=800)

if __name__ == "__main__":
    run()
