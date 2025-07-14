import streamlit as st
import os
import importlib
import sys
import numpy as np

st.set_page_config(page_title="Layer Step Settings")

# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/BulkPlanetarySettings.py
BulkPlanertarySettings_directory = os.path.dirname(os.path.abspath(__file__))
#st.write(BulkPlanertarySettings_directory)

# Get the app directory (/PlanetProfile/PlanetProfileAPP)
app_directory = os.path.dirname(BulkPlanertarySettings_directory)
# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)
# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)


os.chdir('..') #From the PlanetProfile/PlanetProfileApp, going to PlanetProfile

# Get the planet name from the environment variable
Planet = os.getenv("Planet") # e.g., "Venus"
st.write(Planet)


# making sure the Planet folder is in the path so can find PPPlanet
planet_folder_string = '/PlanetProfile/Default/'+str(Planet)
full_planet_folder_string = parent_directory + planet_folder_string
default_folder = sys.path.append(os.path.join(full_planet_folder_string))
#st.write(sys.path)
#planet_folder = sys.path.append(Planet)


# Construct the module name as a string
# e.g., if Planet is "Europa", this becomes "PPEuropa"
module_to_import = f"PP{Planet}"

# Use importlib to import the module
planet_module = importlib.import_module(module_to_import)

from PlanetProfile.Utilities.defineStructs import PlanetStruct, Constants #grabbing what we need so user can change what variables they need to
Planet =PlanetStruct(Planet)



st.title("Layer Step Settings")
st.write("OPTIONAL -- Choose your Layer Step Settings Below")
st.subheader("Ice I Layer Steps")
Planet.Steps.nIceI = st.number_input("Desired number of Ice I Layer steps", value = planet_module.Planet.Steps.nIceI, step = 1)
st.write("Defines the number of steps for the Ice I layer. Number of steps for other layers will be calculated based on mass, radius, and moment of inertia inputs.")
st.markdown("---")

st.subheader("Ocean Pressure Step Size")
Planet.Ocean.deltaP = st.number_input("Step Size for Ocean Pressure $\Delta P$ (MPa)", value = planet_module.Planet.Ocean.deltaP)
st.write("Increment of pressure in MPa between each layer in lower hydrosphere/ocean (sets profile resolution)")
st.markdown("---")

st.subheader("Temperature Step Size")
Planet.Ocean.deltaT = st.number_input("Step size for Temperature $\Delta T$ ($^\circ K$)", value = planet_module.Planet.Ocean.deltaT)
st.write("Step size in $^\circ K$ for temperature values used in generating ocean EOS functions. If set, overrides calculations that otherwise use the specified precision in user-set temperature at the bottom $^\circ K$ to determine this.")
st.markdown("---")

st.subheader("Hydrosphere Maximum Pressure")
Planet.Ocean.PHydroMax_MPa = st.number_input("Maximum Pressure of the Hydrosphere (MPa)", value = planet_module.Planet.Ocean.PHydroMaz_MPa)
st.write("Guessed maximum pressure of the hydrosphere in MPa. Must be greater than the actual pressure, but ideally not by much.")
st.markdown("---")