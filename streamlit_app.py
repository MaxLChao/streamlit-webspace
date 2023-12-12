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
            
            Due to the immense size of the csv, and RAM limitations of the app + resources, we took only a subselection of the measurements by a patient to display. Here we took only 1 million measurements from the original csv, and then began data cleaning on this subselection. To host and visualize the data in the timeline format required, conversion of the data needed to be performed, subsetting each by the patient and converting into a [timeline json format](https://timeline.knightlab.com/docs/json-format.html). 

            In terms of additional cleaning done by the 1 Million measurments that were subselected, many of these actually were missing dates and had to be dropped. There were 4 different categories of measurments that were taken:
            
            | Concept ID | Counts | Counts with dates |
            |-----|---|---|
            |Clinical Observation|203852|203852|
            |Lab Test|600051|502838|
            |Observable Entity|195875|195875|
            |Procedure|222|181|
            |**Total**|**1000000**|**902756**|

            Each category was used as the title for each "event" in the timeline with the observable entry acting as the textual data. Once completed, data was pulled from the cleaned person.csv and general patient information was displayed on the summary page of the timeline as well as adding the death tag and death date if the patient had past. Data cleaning was performed in R and a small subselection of patients were converted into timeline json and displayed onto the timeline tab. R Scripting of the data clean up is available in the repo under [measurements_cleanup.R](https://github.com/MaxLChao/streamlit-webspace/blob/main/measurenments_cleanup.R)

            
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
