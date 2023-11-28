import streamlit as st
from streamlit.logger import get_logger
import numpy as np
import pandas as pd
import time
#import plotly.express as px
# streamlit timeline

LOGGER = get_logger(__name__)


def run():
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

if __name__ == "__main__":
    run()
