import streamlit as st
import pandas as pd
import numpy as np
import helpers as utils

def get_magnitud_category(magnitud):
    if magnitud <= 2:
        return "Micro"
    elif magnitud <= 3.9:
        return "Menor"
    elif magnitud <= 3:
        return "Micro"
    elif magnitud <= 4.9:
        return "Ligero"
    elif magnitud <= 5.9:
        return "Moderado"
    elif magnitud <= 6.9:
        return "Fuerte"
    elif magnitud <= 7.9:
        return "Mayor"
    elif magnitud <= 9.9:
        return "Épico o Catastrófico"
    return "Legendario o apocalíptico"

def get_profundidad_category(profundidad):
    if profundidad <= 70:
        return "Superficiales"
    elif profundidad <= 450:
        return "Intermedios"
    return "Profundos "

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
df["MAGNITUD_CLASS"] = df["MAGNITUD"].transform(get_magnitud_category)
df["PROFUNDIDAD_CLASS"] = df["PROFUNDIDAD"].transform(get_profundidad_category)
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
    "SIZE": None,
    "MAGNITUD_CLASS": None,
    "PROFUNDIDAD_CLASS": None
}
st.dataframe(df, hide_index=True, column_config=column_config)

years = df["YEAR"].unique()
magnitudes = df["MAGNITUD_CLASS"].unique()
profundidades = df["PROFUNDIDAD_CLASS"].unique()

start_year, end_year = years[0], years[years.size - 1]
st.markdown(str.format(f"### Mapa de Sismos ({start_year}-{end_year})"))
start_year, end_year = st.select_slider(
    "Seleccione un rango de fechas:",
    options=years,
    value=(years[0], years[years.size - 1]),
)

columns1 = st.columns([2,2])
magnitudes_selected = columns1[0].multiselect('Seleccionar por Magnitud:', magnitudes, magnitudes)
profundidades_selected = columns1[1].multiselect('Seleccionar por Profundidad:', profundidades, profundidades)

st.markdown('''
Seleccionaste las fechas entre {0} y {1}\n
Profundidad: {2}\n
Magnitud: {3}\n
'''.format(start_year, end_year, profundidades_selected, magnitudes_selected))

df1 = df[(df["YEAR"] >= start_year) & (df["YEAR"] <= end_year) & (df["MAGNITUD_CLASS"].isin(magnitudes_selected)) & (df["PROFUNDIDAD_CLASS"].isin(profundidades_selected))]
df2 = df1.groupby("YEAR").size().reset_index(name="COUNT")

on = st.toggle("Mostrar tabla de resultados")
if on:
    columns2 = st.columns([2,6])
    columns2[0].dataframe(df2, hide_index=True, column_config={"YEAR": "Año", "COUNT": "Cantidad"})
    columns2[1].map(df1, latitude="LATITUD", longitude="LONGITUD", size="SIZE")
else:
    st.map(df1, latitude="LATITUD", longitude="LONGITUD", size="SIZE")

