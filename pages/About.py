import streamlit as st

st.set_page_config(page_title="About")
st.set_page_config(page_icon="./PPlogo.ico")


st.title("About Planet Profile")
st.subheader("Key Funcitonality")
st.write("Radial models of planetary interiors are generated from bulk properties based on geophysical models, lab data, and minimal assumptions")

st.subheader("Abstract")
st.write("The open-source PlanetProfile framework was developed to investigate the interior structure of icy moons based on collectively matching their observed properties and comparative planetology. \
The software relates observed and measured properties, assumptions such as the type of materials present, and laboratory equation-of-state (EOS) data through geophysical and thermodynamic models \
to evaluate radial profiles of mechanical, thermodynamic, and electrical properties, as self-consistently as possible.")

st.subheader("Plain Language Summary")
st.write("The software package PlanetProfile was developed in order to connect measurable properties of planetary bodies to each other and determine how planetary interiors might be structured.")

st.write("$From: Styczinski, S. D. Vance, and M. Melwani Daswani (2023)$ \n\n"
         "PlanetProfile: Self-consistent interior structure modeling for ocean worlds and rocky dwarf planets in Python. \n"
        "Earth and Space Science, 10(8), 10.1029/2022ea002748")
