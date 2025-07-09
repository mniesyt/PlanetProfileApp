import streamlit as st
import os
st.set_page_config(page_title="Bulk Planetary Settings")

st.title("Bulk Planetary Settings")
st.write("OPTIONAL -- Choose your Bulk Planetary Settings Below")

Planet = os.getenv("Planet")

os.chdir('..') #going to PlanetProfile
os.chdir("/"+ str(Planet)) #pulling 

#st.write(PP+str(Planet))

PPPlanet = "PP"+str(Planet)

from PPPlanet import *


os.environ["Planet.Bulk.R_m"] = str(st.number_input("Radius of the body (m)", value = Planet.Bulk.R_m))
#to be passed to Planet.Bulk.R_m
os.environ["Planet.Bulk.M_kg"] = str(st.number_input("Mass of the body (kg)"))
# to be passed to Planet.Bulk.M_kg
os.environ["Planet.Bulk.Tsurf_K"] = str(st.number_input("Temperature at the surface ($^\circ K$)"))
#Planet.Bulk.Tsurf_K = 110
os.environ["Planet.Bulk.Psurf_MPa"] = str(st.number_input("Pressure at the surface (MPa)"))
#Planet.Bulk.Psurf_MPa = 0.0
os.environ["Planet.Bulk.Cmeasured"] = str(st.number_input("Normalized Axial Moment of Inertia $C$"))
#Planet.Bulk.Cmeasured = 0.346  # Value from Anderson et al. (1998): https://doi.org/10.1126/science.281.5385.2019
os.environ["Planet.Bulk.Cuncertainty "] = str(st.number_input("Uncertainty in $C$"))
#Planet.Bulk.Cuncertainty = 0.005
os.environ["Planet.Bulk.Tb_K"] = str(st.number_input("Temperature at the bottom ($^\circ K$)"))
#Planet.Bulk.Tb_K = 268.305  # 30 km ice with 1.0x Seawater