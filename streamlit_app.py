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
            """)
    with tab2:
        st.header("Cohort Description")
    with tab3:
        st.header("Patient History")
        option = st.selectbox(
                "Select a patient ID:", 
                ("4", "36855", "8933",  "4084"))
        file = 'json/'+option+'.json'
        with open(file, "r") as f:
    	    data = f.read()
        timeline(data, height=800)

if __name__ == "__main__":
    run()
