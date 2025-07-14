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
Planet =PlanetStruct(Planet)




# Initializing the session state of all the variables
if "Planet.Bulk.R_m" not in st.session_state:
    st.session_state.Planet_Bulk_R_m = planet_module.Planet.Bulk.R_m  # Initialize the session state
if "Planet.Bulk.M_kg" not in st.session_state:
    st.session_state.Planet_Bulk_M_kg = planet_module.Bulk.M_kg
if "Planet.Bulk.Tsurf_K" not in st.session_state:
     st.session_state.Planet_Bulk_Tsurf_K = planet_module.Bulk.Tsurf_K
if "Planet.Bulk.Psurf_MPa" not in st.session_state:
    st.session_state.Planet_Bulk_Psurf_MPa = planet_module.Bulk.Psurf_MPa
if "Planet.Bulk.Cmeasured" not in st.session_state:
    st.session_state.Planet_Bulk_Cmeasured = Planet.Bulk.Cmeasured
if "Planet.Bulk.Cuncertainty" not in st.session_state:
    st.session_state.Planet_Bulk_Cuncertainty = Planet.Bulk.Cuncertainty
if "Planet.Bulk.Tb_K" not in st.session_state:
    st.session_state.Planet_Bulk_Tb_K = Planet.Bulk.Tb_K


def user_input_a_variable(bulk_setting):
    st.write("You are setting a custom value for this variable: " + bulk_setting)


Planet.Bulk.R_m = st.number_input("Radius of the body (m)", value = planet_module.Planet.Bulk.R_m, key = "Planet.Bulk.R_m", on_change = user_input_a_variable("Radius of the body (m)"))
Planet.Bulk.M_kg = st.number_input("Mass of the body (kg)", value = planet_module.Planet.Bulk.M_kg, key = "Planet.Bulk.M_kg", on_change = user_input_a_variable("Mass of the body (kg)"))
Planet.Bulk.Tsurf_K = st.number_input("Temperature at the surface ($^\circ K$)", value = planet_module.Planet.Bulk.Tsurf_K, key = "Planet.Bulk.M_kg",on_change = user_input_a_variable("Temperature at the surface ($^\circ K$)"))
Planet.Bulk.Psurf_MPa = st.number_input("Pressure at the surface (MPa)", value = planet_module.Planet.Bulk.Psurf_MPa, key = "Bulk.Psurf_MPa", on_change = user_input_a_variable("Pressure at the surface (MPa)"))
Planet.Bulk.Cmeasured = st.number_input("Normalized Axial Moment of Inertia $C$", value = planet_module.Planet.Bulk.Cmeasured, key = "Planet.Bulk.Cmeasured", on_change = user_input_a_variable("Normalized Axial Moment of Inertia $C$"))
Planet.Bulk.Cuncertainty = st.number_input("Uncertainty in $C$", value = planet_module.Planet.Bulk.Cuncertainty, key = "Planet.Bulk.Cuncertainty", on_change = user_input_a_variable("Uncertainty in $C$y"))
Planet.Bulk.Tb_K = st.number_input("Temperature at the bottom ($^\circ K$)", value = planet_module.Planet.Bulk.Tb_K, key = "Planet.Bulk.Tb_K", on_change = user_input_a_variable("Temperature at the bottom "))
#os.environ["Planet.Bulk.Tb_K"] = str(st.number_input("Temperature at the bottom ($^\circ K$)", value = planet_module.Planet.Bulk.Tb_K))

#need to make it so that custom runs save to /PlanetProfile/Planet, and that these runs will be available for the user to load their custom runs later

os.chdir('PlanetProfileApp') #changing back to app directory so people can navigate between other pages