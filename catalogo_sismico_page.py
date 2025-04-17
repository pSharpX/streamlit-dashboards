import streamlit as st
import pandas as pd
import numpy as np
import helpers as utils

def get_magnitud_category(magnitud):
    if magnitud < 2:
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
    return f'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><circle cx="40" cy="50" r="25" fill="%23{color[1:-2]}"/></svg>'


st.title("Catálogo Sísmico 1960 - 2023")
st.sidebar.markdown("# Page 4 🌎")
st.divider()

dataset_path = "./data/Catalogo1960_2023.csv"

df = utils.read_dataset(dataset_path, dtype={"ID": "int64","FECHA_UTC": str,"HORA_UTC": str,"LATITUD": "float64","LONGITUD": "float64","PROFUNDIDAD": "int64","MAGNITUD": "float64","FECHA_CORTE": str})

df["FECHA"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.strftime('%Y-%m-%d')
df["YEAR"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.year
df["MONTH"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.month
df["YEAR_MONTH"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.strftime('%Y-%m')
df["MONTH_NAME"] = pd.to_datetime(df["FECHA_UTC"], format='%Y%m%d').dt.month_name()
df["HORA"] = pd.to_datetime(df["HORA_UTC"], format='%H%M%S').dt.time
df["MAGNITUD_CLASS"] = df["MAGNITUD"].transform(get_magnitud_category)
df["PROFUNDIDAD_CLASS"] = df["PROFUNDIDAD"].transform(get_profundidad_category)
df["SIZE"] = df["MAGNITUD_CLASS"].transform(get_size)
df["COLOR"] = df["MAGNITUD_CLASS"].transform(get_color)
df["COLOR_PREVIEW"] = df["COLOR"].transform(get_color_preview)

column_config = {
    "ID": None,
    "FECHA_UTC": None,
    "FECHA": st.column_config.TextColumn(
        "Fecha",
        help="Hora universal coordinado (UTC), Es la fecha con cinco horas adelantadas con respecto a la hora local debido a que Peru se encuentra en una zona horaria UTC -5"),
    "HORA_UTC": None,
    "HORA": "Hora",
    "YEAR": None,
    "MONTH": None,
    "YEAR_MONTH": None,
    "MONTH_NAME": None,
    "FECHA_CORTE": None,
    "LATITUD": "Latitud",
    "LONGITUD": "Longitud",
    "PROFUNDIDAD": st.column_config.NumberColumn(
        "Profundidad",
        help="Profundidad del foco sísmico por debajo de la superficie",
        format="%d Km"),
    "MAGNITUD": st.column_config.TextColumn(
        "Magnitud",
        help="Corresponde a la cantidad de energía liberada por el sismo y esta expresada en la escala de magnitud momento Mw."),
    "MAGNITUD_CLASS": "Clase",
    "PROFUNDIDAD_CLASS": "Clase",
    "SIZE": None,
    "COLOR": None,
    "COLOR_PREVIEW": st.column_config.ImageColumn("Color")
}
column_order=("FECHA", "HORA", "LATITUD", "LONGITUD", "MAGNITUD", "MAGNITUD_CLASS", "PROFUNDIDAD", "PROFUNDIDAD_CLASS", "COLOR_PREVIEW")
st.dataframe(df, hide_index=True, column_config=column_config, column_order=column_order)

years = df["YEAR"].unique()
magnitudes = df["MAGNITUD_CLASS"].unique()
profundidades = df["PROFUNDIDAD_CLASS"].unique()

magnitudes_help = '''
1. Micro(< de 2,0)
2. Menor(2,0-2,9 y 3,0-3,9)
3. Ligero(4,0-4,9)
4. Moderado(5,0-5,9)
5. Fuerte(6,0-6,9)
6. Mayor(7,0-7,9)
7. Épico o Catastrófico(8,0-8,9 y 9,0-9,9)
8. Legendario o apocalíptico(10,0+)
'''
profundidades_help = '''
1. Superficial (0–70 km)
2. Intermedia (70–450 km)
3. Profunda (+450 km)
'''

start_year, end_year = years[0], years[years.size - 1]
st.markdown(str.format(f"### Mapa de Sismos ({start_year}-{end_year})"))
start_year, end_year = st.select_slider(
    "Filtrar por Rango de Fechas:",
    options=years,
    value=(years[0], years[years.size - 1]),
)

columns1 = st.columns([2,2])
magnitudes_selected = columns1[0].multiselect('Filtrar por Magnitud del Sismo:', help=magnitudes_help, options=magnitudes, default=magnitudes)
profundidades_selected = columns1[1].multiselect('Filtrar por Profundidad del Epicentro:', help=profundidades_help, options=profundidades, default=profundidades)

st.markdown('''
**Filtros aplicados**\n
`Fechas: {0} a {1}`\n
`Magnitud: {2}`\n
`Profundidad: {3}`\n
'''.format(start_year, end_year, magnitudes_selected, profundidades_selected))

df1 = df[(df["YEAR"] >= start_year) & (df["YEAR"] <= end_year) & (df["MAGNITUD_CLASS"].isin(magnitudes_selected)) & (df["PROFUNDIDAD_CLASS"].isin(profundidades_selected))]
df2 = df1.groupby("YEAR").size().reset_index(name="COUNT")

#on = st.toggle("Mostrar tabla de resultados")

tab1, tab2 = st.tabs(["Mapa", "Resultados"])
with tab1:
    st.map(df1, latitude="LATITUD", longitude="LONGITUD", size="SIZE", color="COLOR")
with tab2:
    st.dataframe(df2, hide_index=True, column_config={"YEAR": "Año", "COUNT": "Cantidad"})