import streamlit as st
import os

st.set_page_config(page_title="Run Planet Profile")


if st.button("Run Planet Profile with my Choices", type = "primary"):
    st.write("Pushing your settings and choices to Planet Profile...")

    os.chdir('..')
    # Assuming user has cloned the PPApp into the same environment as PP
    current_directory = os.getcwd()
    st.write(f"Current working directory: {current_directory}")
    Planet = os.getenv("Planet")
    os.system('python PlanetProfileCLI.py Planet')

    #python PlanetProfileCLI.py Europa

else:
    st.write("Choices have not yet been pushed to Planet Profile")






