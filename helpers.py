import streamlit as st
import pandas as pd
import os

dirname = os.path.dirname(__file__)

@st.cache_data
def read_dataset(dataset_path, separator=","):
    filename = os.path.join(dirname, dataset_path)
    return pd.read_csv(filename, sep=separator)