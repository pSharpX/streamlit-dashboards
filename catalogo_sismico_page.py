import streamlit as st
import pandas as pd
import numpy as np
import helpers as utils

st.title("Catalogo Sismico 1960 - 2023")
st.sidebar.markdown("# Page 4 🎉")
st.divider()

dataset_path = "./data/Catalogo1960_2023.csv"

df = utils.read_dataset(dataset_path)

df["YEAR"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.year
df["MONTH"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.month
df["YEAR_MONTH"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.strftime('%Y-%m')
df["MONTH_NAME"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.month_name()

st.write(df)
st.map(df, latitude="LATITUD", longitude="LONGITUD", size="MAGNITUD")

