import streamlit as st
import pandas as pd
import numpy as np
import helpers as utils

def get_magnitud_category(magnitud):
    if magnitud <= 2:
        return "Micro"
    elif magnitud <= 3.9:
        return "Menor"
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
    return "Profundos"

def get_size(magnitud_class):
    return {
        "Micro": 0.2*100*10,
        "Menor": 0.4*100*10,
        "Ligero": 0.8*100*10,
        "Moderado": 1*100*10,
        "Fuerte": 10*100*10,
        "Mayor": 15*100*10,
        "Épico o Catastrófico": 30*100*10,
        "Legendario o apocalíptico": 30*100*10
    }.get(magnitud_class)

def get_color(magnitud_class):
    match magnitud_class:
        case "Micro":
            color = "#008f3950"
        case "Menor":
            color = "#ffff0050"
        case "Ligero":
            color = "#ff660060"
        case "Moderado":
            color = "#ff450060"
        case "Fuerte":
            color = "#ff400080"
        case "Mayor":
            color = "#b83d1480"
        case "Épico o Catastrófico":
            color = "#572364"
        case _:
            color = "#0a0a0a"
    return color

def get_color_preview(color):
    return f'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><circle cx="40" cy="50" r="25" fill="%23{color[1:]}"/></svg>'


st.title("Catálogo Sísmico 1960 - 2023")
st.sidebar.markdown("# Page 4 🎉")
st.divider()

dataset_path = "./data/Catalogo1960_2023.csv"

df = utils.read_dataset(dataset_path)

df["YEAR"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.year
df["MONTH"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.month
df["YEAR_MONTH"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.strftime('%Y-%m')
df["MONTH_NAME"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.month_name()
df["MAGNITUD_CLASS"] = df["MAGNITUD"].transform(get_magnitud_category)
df["PROFUNDIDAD_CLASS"] = df["PROFUNDIDAD"].transform(get_profundidad_category)
df["SIZE"] = df["MAGNITUD_CLASS"].transform(get_size)
df["COLOR"] = df["MAGNITUD_CLASS"].transform(get_color)
df["COLOR_PREVIEW"] = df["COLOR"].transform(get_color_preview)

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
    "MONTH_NAME": None,
    "MAGNITUD_CLASS": "Clase",
    "PROFUNDIDAD_CLASS": None,
    "SIZE": None,
    "COLOR": None,
    "COLOR_PREVIEW": st.column_config.ImageColumn("Color")
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
    columns2[1].map(df1, latitude="LATITUD", longitude="LONGITUD", size="SIZE", color="COLOR")
else:
    st.map(df1, latitude="LATITUD", longitude="LONGITUD", size="SIZE", color="COLOR")

