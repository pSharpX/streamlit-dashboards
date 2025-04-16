import streamlit as st
import pandas as pd
import numpy as np
import helpers as utils

st.title("Catálogo Sísmico 1960 - 2023")
st.sidebar.markdown("# Page 4 🎉")
st.divider()

dataset_path = "./data/Catalogo1960_2023.csv"

df = utils.read_dataset(dataset_path)

df["YEAR"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.year
df["MONTH"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.month
df["YEAR_MONTH"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.strftime('%Y-%m')
df["MONTH_NAME"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.month_name()
df["SIZE"] = df["MAGNITUD"] * 100
#df["COLOR"] = df["MAGNITUD"] * 100

column_config = {
    "ID": None,
    "FECHA_UTC": None,
    "HORA_UTC": "Hora",
    "LATITUD": "Latitud",
    "LONGITUD": "Longitud",
    "PROFUNDIDAD": "Profundidad",
    "MAGNITUD": "Magnitud",
    "FECHA_CORTE": None,
    "YEAR": "Año",
    "MONTH": None,
    "YEAR_MONTH": "Fecha",
    "MONTH_NAME": "Mes",
    "SIZE": None
}
st.dataframe(df, hide_index=True, column_config=column_config)

years = df["YEAR"].unique()

start_year, end_year = years[0], years[years.size - 1]
st.markdown(str.format(f"### Mapa de Sismos ({start_year}-{end_year})"))
start_year, end_year = st.select_slider(
    "Seleccione un rango de fechas:",
    options=years,
    value=(years[0], years[years.size - 1]),
)

df1 = df[(df["YEAR"] >= start_year) & (df["YEAR"] <= end_year)]
df2 = df1.groupby("YEAR").size().reset_index(name="COUNT")
st.markdown(str.format(f"Seleccionaste las fechas entre {start_year} y {end_year}"))

on = st.toggle("Mostrar tabla de resultados")
if on:
    columns = st.columns([2,6])
    columns[0].dataframe(df2, hide_index=True, column_config={"YEAR": "Año", "COUNT": "Cantidad"})
    columns[1].map(df1, latitude="LATITUD", longitude="LONGITUD", size="SIZE")
else:
    st.map(df1, latitude="LATITUD", longitude="LONGITUD", size="SIZE")

