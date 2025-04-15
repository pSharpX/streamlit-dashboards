import streamlit as st
import pandas as pd
import numpy as np
import helpers as utils

st.title("Centros de Vacunacion")
st.sidebar.markdown("# Overview 🎉")
st.divider()

st.markdown(
    """
    Esta tabla contiene la lista de los centros de vacunación programadas según entidad y ubicación geográfica a nivel nacional del territorio peruano.
    ### Dato y Medio de Distribución
    - Centros de Vacunación COVID-19 [Ir al recurso](https://cloud.minsa.gob.pe/s/96XbzfYBCGcwtp7/download)
    - Diccionario de Datos - Centros de Vacunación COVID-19 [Descargar](https://www.datosabiertos.gob.pe/sites/default/files/DD_TB_CENTRO_VACUNACION.xlsx)
    
    ### Dataset Info
    These fields are compatible with DCAT, an RDF vocabulary designed to facilitate interoperability between data catalogs published on the Web.
    | Field | Value |
    | -------- | ------- |
    | Publisher | [Ministerio de Salud](https://www.datosabiertos.gob.pe/group/ministerio-de-salud) |
    | Fecha modificada | 2021-09-08 |
    | Fecha de lanzamiento | 2021-08-14 |
    | Frequency | Daily |
    | Identificador | bd7f1a52-b383-49c9-876f-d8746a0e8975 |
    | License | [Open Data Commons Attribution License](http://opendefinition.org/licenses/odc-by/) |
    | Author | Ministerio de Salud |
    | Contact Name | OGTI-MINSA |
    | Contact Email | [mesadeayuda@minsa.gob.pe](mesadeayuda@minsa.gob.pe) |
    | Public Access Level | Public |
"""
)

dataset_path = "./data/TB_CENTRO_VACUNACION.csv"

df = utils.read_dataset(dataset_path, ";")
df_entidades_admin = df['entidad_administra'].dropna().unique()

st.subheader("Dataset:")
option = st.selectbox('Seleccionar una entidad:', df_entidades_admin)
df_main = df[df['entidad_administra'] == option]
st.write(df_main)