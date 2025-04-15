import streamlit as st
import pandas as pd
import numpy as np

# Define the pages
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
main_page2 = st.Page("main_page2.py", title="Main Page 2", icon="🎈")
page_2 = st.Page("ubigeo_page.py", title="Page 2", icon="🎈")
page_3 = st.Page("centro_vacunas_page.py", title="Page 3", icon="❄️")
page_4 = st.Page("catalogo_sismico_page.py", title="Page 4", icon="🎉")

# Set up navigation
pg = st.navigation([main_page, main_page2, page_2, page_3, page_4])

# Run the selected page
pg.run()

