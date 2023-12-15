import streamlit as st
from streamlit.logger import get_logger
import numpy as np
import pandas as pd
import time
import plotly.figure_factory as ff
import plotly.express as px

# streamlit timeline
import streamlit as st
from streamlit_timeline import timeline
import json

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(layout="wide")
    tab1, tab2, tab3, tab4 = st.tabs(["Background", "Cohort Description", "Patient History", "Clinical Relationships"])
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
            
            From Ariadna: "Dropped concept ids for race, ethnicity and gender. Also dropped person source values as each person had a unique source value and I haven’t seen it in other files (unlike person id which is in measurements I believe). Ethnicity only gives two values. Dropped the month and year of birth and modified the datetime column to remove the time of birth (didn’t have time of birth just had a bunch of zeros)."

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
            
            Worked with a subset of the data, dealing only with data with non NaNs that have expired. Leaves us with 730 patients who have expired of the 3166 with data entries about conditions they had. 

            From Eliezer:"
            Of the cases, I had to eliminate many patients for having so many NaNs in fields even after reductions of categories. But there is about 1000 patients that died that we could study further, how old they were when they died, gender, race, condition, confirmed diagnosis occurrence, observation, and visit id aligned with anything else you wish to pull from these. Many had comorbidities listed when they "expired". This could be interesting along with any other data we have been looking at."

            """)
    with tab2:
        st.header("Cohort Description")
        file = "tables/personDF.csv"
        p_df = pd.read_csv(file)
        option_graphs = st.selectbox(
                "Select an overview: ",
                ("overview", "age", "sex", "race", "occurence types"))
        
        if option_graphs == "overview":
            st.markdown("""
            ### Patient Cohort description
            
            50740 unique patients, data taken from a cleaned person.csv found in the repo: [person.csv](https://github.com/MaxLChao/streamlit-webspace/blob/main/tables/personDF.csv). 

            Here we include basic graphics on a few cohort descriptors including: age, sex, race and occurence types.   

            ### PersonDF.csv 
            """)
            lines = st.slider("Select number of lines to visualize:", min_value=10, max_value=1000, value=10,
                              step = 10)
            st.table(p_df[["person_id", "gender_source_value", "race_source_value","death","age"]].head(n=lines))
        elif option_graphs == "age":
            fig = ff.create_distplot([p_df["age"]], ["Age (in Years)"])
            st.plotly_chart(fig, use_container_width = True)
            st.markdown("""
                Summary:

                Mean Age: 65.44
                
                Median Age: 66.00
                
                        """)
        elif option_graphs == "sex":
            sdf = p_df["gender_source_value"].value_counts().rename_axis('Sex').reset_index(name='Count') 
            fig = px.pie(sdf, values ='Count', names='Sex')
            fig.layout.height=500
            fig.layout.width=500
            st.plotly_chart(fig, use_container_width = True)
            st.dataframe(sdf, width=400, height=100)
        elif option_graphs == "race":
            st.markdown("""
            ### Split by Race:
            """)
            race = p_df["race_source_value"].value_counts().rename_axis('race').reset_index(name='counts')
            fig = px.pie(race, values ='counts', names='race')
            fig.layout.height = 700
            fig.layout.width = 700
            st.plotly_chart(fig, use_container_width = True)
            st.dataframe(race, width=400, height=350)
        elif option_graphs == "occurence types":
            st.markdown("""
                ### Occurences Mapped by Deaths

                Data cleaned for occurences by patients that have passed. There are multiple mappings to single patients.
                Only 730 of the 3166 recorded patients that had expired had mappings to occurences.

                The full listing of the occurences with the patient ids are available via: [EAfromAKSmergedDeath.csv](https://github.com/MaxLChao/streamlit-webspace/blob/main/tables/EAfromAKSmergedDeath.csv)
                        """)
            occ_opts = st.selectbox("Occurence Reviews: ",
                         ("Occurence Overview","Top Conditions", "Condition Multimapping"))
            if occ_opts == "Occurence Overview":
                occ_df = pd.read_csv("tables/EAfromAKSmergedDeath.csv")
                lines = st.slider("Select number of lines to visualize:", min_value =10, max_value = 1000, value = 10,
                                  step = 10)
                st.table(occ_df.head(n=lines))
            elif occ_opts == "Top Conditions":
                top_cons = pd.read_csv("tables/topconds.csv")
                lines = st.slider("Select number of lines to visualize:", min_value =10, 
                                  max_value = len(top_cons.index), value = 10,
                                  step = 10)
                st.table(top_cons.head(n=lines))
            elif occ_opts == "Condition Multimapping":
                idmat = pd.read_csv("tables/idmatrix_occ.csv", index_col=0)
                rcs = st.slider("Select number of top occurences:", min_value =10, 
                                max_value = len(idmat.index), value = 10,
                                step = 10)
                rcs = rcs - 1
                plotmat = idmat.iloc[0:rcs,0:rcs]
                #st.table(plotmat)
                fig = px.imshow(plotmat)
                fig.layout.width = 1000
                fig.layout.height = 1000
                st.plotly_chart(fig, use_container_width = True)
    with tab3:
        st.header("Patient History")
        option = st.selectbox(
                "Select a patient ID:", 
                ("4", "36855", "8933",  "4084", "25990", "23594"))
        file = 'json/'+option+'.json'
        with open(file, "r") as f:
    	    data = f.read()
        timeline(data, height=800)

    with tab4:
        st.header("Clinical Relationships with Death")
        cl_opts = st.selectbox("Select a Clinical Feature:",
                               ("Overview","Sex", "Age", "Race"))
        if cl_opts == "Overview":
            st.markdown("""
                ### Overview

                Looking into the correlation of simple clinical features with respect to death. Included are for race, sex, and age against death.

            """)
            corrmat = pd.read_csv("tables/corrmat_death.csv")
            st.dataframe(corrmat, width=600, height=520)
        elif cl_opts == "Sex":
            sdf = pd.read_csv("tables/sex_barplot.csv")
            meth = st.selectbox("Display Method:", 
                         ("Flat", "Percentage"))
            if meth == "Flat":
                fig = px.bar(sdf, x="sex", y='count', color='death',title="Death by Sex")
                st.plotly_chart(fig, use_container_width = True)
            elif meth == "Percentage":
                sdf['percentage'] = sdf['count']/sdf.groupby('sex')['count'].transform('sum')
                fig = px.bar(sdf, x='sex', y='percentage', color='death', title='Death by Sex')
                st.plotly_chart(fig, use_container_width = True)
        elif cl_opts == "Age":
            pdf = pd.read_csv("tables/personDF.csv")
            fig =px.box(pdf, x='death', y='age')
            st.plotly_chart(fig, use_container_width = True)
            st.markdown("""
                Median age of Alive: 65
                
                Median age of Expired: 80
            """)
        elif cl_opts == "Race":
            rdf = pd.read_csv("tables/race_barplot.csv")
            meth = st.selectbox("Display Method:",
                                ("Flat", "Percentage"))
            if meth == "Flat":
                fig = px.bar(rdf, x="race", y='count', color='death',title="Death by race")
                st.plotly_chart(fig, use_container_width = True)
            elif meth == "Percentage":
                rdf['percentage'] = rdf['count']/rdf.groupby('race')['count'].transform('sum')
                fig = px.bar(rdf, x='race', y='percentage', color='death', title='Death by race')
                st.plotly_chart(fig, use_container_width = True)
        

if __name__ == "__main__":
    run()
