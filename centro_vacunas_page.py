import streamlit as st
import pandas as pd
import numpy as np
import helpers as utils

def merge_centro_vacunas_and_ubigeos(df_centros, df_ubigeos):
    return pd.merge(df_centros, df_ubigeos, left_on="id_ubigeo", right_on="id_ubigeo", how="left", suffixes=("_ds1", "_ds2"))

def clean_data_ubigeos(df_ubigeos):
    df_ubigeos.drop(['ubigeo_reniec','ubigeo_inei', 'departamento_inei', 'provincia_inei', 'macroregion_inei', 'macroregion_minsa', 'iso_3166_2', 'fips'], axis=1, inplace=True)

def clean_data_centros(df_centros):
    df_centros['entidad_administra'].fillna("Sin Entidad", inplace=True)
    df_centros.drop("id_eess", axis=1, inplace=True)

def group_centros_by_entidades(df):
    return df.groupby("entidad_administra", sort="count").size().reset_index(name="count")

def group_centros_by_departamento(df):
    return df.groupby("departamento", sort="count").size().reset_index(name="count")

def group_centros_by_provincia(df):
    return df.groupby(["departamento", "provincia"], sort="count").size().reset_index(name="count")

def group_centros_by_distrito(df):
    return df.groupby("distrito", sort="count").size().reset_index(name="count")

def filter_centros_by_departamento(df, departamento="LIMA"):
    return df[df["departamento"] == departamento]

def filter_centros_by_provincia(df, provincia="LIMA"):
    return df[df["provincia"] == provincia]

def filter_centros_without_entidades(df):
    return df[df["entidad_administra"] != "Sin Entidad"]

st.title("DataSet - Centros de Vacunacion")
st.sidebar.markdown("# Page 3 🎉")
st.divider()

centros_dataset_url = "./data/TB_CENTRO_VACUNACION.csv"
ubigeo_dataset_url = "./data/TB_UBIGEOS.csv"

df_centros = utils.read_dataset(centros_dataset_url, ";")
df_ubigeos = utils.read_dataset(ubigeo_dataset_url, ";")

clean_data_centros(df_centros)
clean_data_ubigeos(df_ubigeos)

df_main = merge_centro_vacunas_and_ubigeos(df_centros, df_ubigeos)

list_entidades_admin = df_centros['entidad_administra'].dropna().unique()
list_departamentos = df_ubigeos['departamento'].dropna().unique()

option_entidad = st.selectbox('Seleccionar una entidad:', list_entidades_admin)
df_centros_table = df_main[df_main['entidad_administra'] == option_entidad]

df_gb_entidades = filter_centros_without_entidades(df_centros)
df_gb_entidades = group_centros_by_entidades(df_gb_entidades)
df_gb_entidades = df_gb_entidades[df_gb_entidades["count"] > 50]


st.write(df_centros_table)

st.markdown("### Centros de vacunacion por Entidades (> 50 centros)")
st.bar_chart(df_gb_entidades, x="entidad_administra", y="count", x_label="Entidades", y_label="Cantidad")

st.markdown("### Centros de vacunacion por Departamento:")
option_departamento = st.selectbox('Seleccionar un departamento:', list_departamentos)
df_plot_2 = filter_centros_by_departamento(df_main, option_departamento)
st.write(group_centros_by_provincia(df_plot_2))
st.map(df_plot_2, latitude="latitud_ds2", longitude="longitud_ds2")