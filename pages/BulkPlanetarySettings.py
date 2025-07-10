import streamlit as st
import os
import importlib
import sys
import numpy as np



st.set_page_config(page_title="Bulk Planetary Settings")

st.title("Bulk Planetary Settings")
st.write("Choose your Bulk Planetary Settings Below.")

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
st.write("Default values for your selected body are displayed below. You can also change the Bulk Planetary Settings if you would like to.")


# Pulls default values into the app for each PPPlanet, if the user sets a new
# value then it is saved as an environment variable
from PlanetProfile.Utilities.defineStructs import PlanetStruct, Constants #grabbing what we need so user can change what variables they need to

def user_input_a_variable(bulk_setting):
    st.write("You are setting a custom value for this variable: " + bulk_setting)
    os_environ_key = str("Planet.Bulk."+bulk_setting)
    bulk_setting = float(bulk_setting)
    Planet.Bulk.bulk_setting = int(os.environ[os_environ_key])
    


os.environ["Planet.Bulk.R_m"] = str(st.number_input("Radius of the body (m)", value = planet_module.Planet.Bulk.R_m, on_change = user_input_a_variable("R_m")))
st.write(os.environ["Planet.Bulk.R_m"])
#Planet.Bulk.R_m = os.environ["Planet.Bulk.R_m"]
#st.write(Planet.Bulk.R_m)


#to be passed to Planet.Bulk.R_m
os.environ["Planet.Bulk.M_kg"] = str(st.number_input("Mass of the body (kg)", value = planet_module.Planet.Bulk.M_kg))
# to be passed to Planet.Bulk.M_kg
os.environ["Planet.Bulk.Tsurf_K"] = str(st.number_input("Temperature at the surface ($^\circ K$)", value = planet_module.Planet.Bulk.Tsurf_K))
#Planet.Bulk.Tsurf_K = 110
os.environ["Planet.Bulk.Psurf_MPa"] = str(st.number_input("Pressure at the surface (MPa)", value = planet_module.Planet.Bulk.Psurf_MPa))
#Planet.Bulk.Psurf_MPa = 0.0
os.environ["Planet.Bulk.Cmeasured"] = str(st.number_input("Normalized Axial Moment of Inertia $C$", value = planet_module.Planet.Bulk.Cmeasured))
#Planet.Bulk.Cmeasured = 0.346  # Value from Anderson et al. (1998): https://doi.org/10.1126/science.281.5385.2019
os.environ["Planet.Bulk.Cuncertainty "] = str(st.number_input("Uncertainty in $C$", value = planet_module.Planet.Bulk.Cuncertainty))
#Planet.Bulk.Cuncertainty = 0.005
os.environ["Planet.Bulk.Tb_K"] = str(st.number_input("Temperature at the bottom ($^\circ K$)", value = planet_module.Planet.Bulk.Tb_K))
#Planet.Bulk.Tb_K = 268.305  # 30 km ice with 1.0x Seawater


os.chdir('PlanetProfileApp') #changing back to app directory so people can navigate between other pages