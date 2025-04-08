import streamlit as st
import pandas as pd
import numpy as np
import helpers as utils

st.title("Ubigeos")
st.sidebar.markdown("# Page 2 🎉")
st.divider()

st.markdown(
    """
    Contiene las equivalencias de los códigos de UBIGEO del Perú, codificados por RENIEC y el INEI. Tiene un campo id_ubigeo que enlaza a una unidad geográfica equivalente. Contiene la descripción a nivel de departamento, región, provincia y distrito. Además contiene datos de superficie en km2, altitud, latitud y longitud del distrito.
    ### Dato y Medio de Distribución
    - Códigos de Ubigeo del Perú [Ir al recurso](https://cloud.minsa.gob.pe/s/GkfcJD8xKHJeCqn/download)
    - Ubigeo [Descargar](https://www.datosabiertos.gob.pe/sites/default/files/DD_TB_UBIGEOS.xlsx)

    ### Dataset Info
    These fields are compatible with DCAT, an RDF vocabulary designed to facilitate interoperability between data catalogs published on the Web.
    | Field | Value |
    | -------- | ------- |
    | Publisher | [Ministerio de Salud](https://www.datosabiertos.gob.pe/group/ministerio-de-salud) |
    | Fecha modificada | 2021-09-08 |
    | Fecha de lanzamiento | 2021-08-13 |
    | Frequency | Daily |
    | Homepage URL | https://github.com/jmcastagnetto/ubigeo-peru-aumentado |
    | Identificador | db44dd1c-d6ca-4b0c-aede-6532b0b3c177 |
    | License | [Open Data Commons Attribution License](http://opendefinition.org/licenses/odc-by/) |
    | Author | Ministerio de Salud |
    | Contact Name | OGTI-MINSA |
    | Contact Email | [mesadeayuda@minsa.gob.pe](mesadeayuda@minsa.gob.pe) |
    | Public Access Level | Public |
"""
)

dataset_path = "./data/TB_UBIGEOS.csv"

df = utils.read_dataset(dataset_path, ";")
#df_entidades_admin = df['entidad_administra'].dropna().unique()

st.subheader("Dataset:")
#option = st.selectbox('Seleccionar una entidad:', df_entidades_admin)
#df_main = df[df['entidad_administra'] == option]
st.write(df)