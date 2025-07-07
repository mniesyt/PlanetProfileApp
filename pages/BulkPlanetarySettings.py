import streamlit as st
st.set_page_config(page_title="Bulk Planetary Settings")

st.title("Bulk Planetary Settings")
st.write("OPTIONAL -- Choose your Bulk Planetary Settings Below")

st.number_input("Radius of the body (m)")
#to be passed to Planet.Bulk.R_m
st.number_input("Mass of the body (kg)")
# to be passed to Planet.Bulk.M_kg
st.number_input("Temperature at the surface ($^\circ K$)")
#Planet.Bulk.Tsurf_K = 110
st.number_input("Pressure at the surface (MPa)")
#Planet.Bulk.Psurf_MPa = 0.0
st.number_input("Normalized Axial Moment of Inertia $C$")
#Planet.Bulk.Cmeasured = 0.346  # Value from Anderson et al. (1998): https://doi.org/10.1126/science.281.5385.2019
st.number_input("Uncertainty in $C$")
#Planet.Bulk.Cuncertainty = 0.005
st.number_input("Temperature at the bottom ($^\circ K$)")
#Planet.Bulk.Tb_K = 268.305  # 30 km ice with 1.0x Seawater