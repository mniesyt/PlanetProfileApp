import streamlit as st
import os
import importlib
import sys
import numpy as np
from functools import partial



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



# List of bulk property keys and labels - this is a dictionary holding the values of each bulk_setting from the default PP.py 
bulk_fields = {
    "Planet.Bulk.R_m": ("Radius of the body (m)", planet_module.Planet.Bulk.R_m),
    "Planet.Bulk.M_kg": ("Mass of the body (kg)", planet_module.Planet.Bulk.M_kg),
    "Planet.Bulk.Tsurf_K": ("Temperature at the surface ($^\circ K$)", planet_module.Planet.Bulk.Tsurf_K),
    "Planet.Bulk.Psurf_MPa": ("Pressure at the surface (MPa)", planet_module.Planet.Bulk.Psurf_MPa),
    "Planet.Bulk.Cmeasured": ("Normalized Axial Moment of Inertia $C$", planet_module.Planet.Bulk.Cmeasured),
    "Planet.Bulk.Cuncertainty": ("Uncertainty in $C$", planet_module.Planet.Bulk.Cuncertainty),
    "Planet.Bulk.Tb_K": ("Temperature at the bottom ($^\circ K$)", planet_module.Planet.Bulk.Tb_K),
}

# Initialize session state for all fields -> the key is the first part in the dictionary, this initialization loop prevents having to initialize every 
# variable individually as below
for key, (_, default_val) in bulk_fields.items():
    if key not in st.session_state:
        st.session_state[key] = default_val


# Persistent change-tracking dictionary
if "changed_inputs" not in st.session_state:
    st.session_state["changed_inputs"] = {}

# Initializing the session state of all the variables
#if "Planet.Bulk.R_m" not in st.session_state:
    #st.session_state["Planet.Bulk.R_m"]= planet_module.Planet.Bulk.R_m  # Initialize the session state
#if "Planet.Bulk.M_kg" not in st.session_state:
    #st.session_state["Planet.Bulk.M_kg"] = planet_module.Planet.Bulk.M_kg
#if "Planet.Bulk.Tsurf_K" not in st.session_state:
    #st.session_state["Planet.Bulk.Tsurf_K"] = planet_module.Planet.Bulk.Tsurf_K
#if "Planet.Bulk.Psurf_MPa" not in st.session_state:
    #st.session_state["Planet.Bulk.Psurf_MPa"] = planet_module.Planet.Bulk.Psurf_MPa
#if "Planet.Bulk.Cmeasured" not in st.session_state:
    #st.session_state["Planet.Bulk.Cmeasured"] = planet_module.Planet.Bulk.Cmeasured
#if "Planet.Bulk.Cuncertainty" not in st.session_state:
    #st.session_state["Planet.Bulk.Cuncertainty"] = planet_module.Planet.Bulk.Cuncertainty
#if "Planet.Bulk.Tb_K" not in st.session_state:
    #st.session_state["Planet.Bulk.Tb_K"] = planet_module.Planet.Bulk.Tb_K

def on_change_bulk_setting(bulk_setting_key):
    st.session_state["changed_inputs"][bulk_setting_key] = True


    
# Create number inputs dynamically
for key, (label, _) in bulk_fields.items():
    # Set value in the actual Planet object if needed
    field_name = key.split(".")[-1] # this grabs just the key i.e. just Tb_K from "Planet.Bulk.Tb_K" (key.split(".") splits the key into ["Planet", "Bulk", "R_m"] amd [-1] grabs the last object in the list )

    # Create input
    st.number_input(
        label,
        value=st.session_state[key],
        key=key,
        on_change=partial(on_change_bulk_setting, key)
    )

    # Update Planet object
    current_value = st.session_state[key]
    setattr(Planet.Bulk, field_name, current_value)

    # Show success message if changed
    if st.session_state["changed_inputs"].get(key, False):
        st.success(f"You changed **{label}** to `{current_value}`")


if st.button("🔄 Reset all values to defaults"):
    for key, (_, default_val) in bulk_fields.items():
        st.session_state[key] = default_val
    st.session_state["changed_inputs"] = {}
    st.rerun()  # Force UI to update immediately

#Planet.Bulk.R_m = st.number_input("Radius of the body (m)", value =  st.session_state["Planet.Bulk.R_m"], key = "Planet.Bulk.R_m", on_change = user_input_a_variable)
#Planet.Bulk.M_kg = st.number_input("Mass of the body (kg)", value = planet_module.Planet.Bulk.M_kg, on_change = user_input_a_variable)
#Planet.Bulk.Tsurf_K = st.number_input("Temperature at the surface ($^\circ K$)", value = planet_module.Planet.Bulk.Tsurf_K,on_change = user_input_a_variable)
#Planet.Bulk.Psurf_MPa = st.number_input("Pressure at the surface (MPa)", value = planet_module.Planet.Bulk.Psurf_MPa, on_change = user_input_a_variable)
#Planet.Bulk.Cmeasured = st.number_input("Normalized Axial Moment of Inertia $C$", value = planet_module.Planet.Bulk.Cmeasured,  on_change = user_input_a_variable)
#Planet.Bulk.Cuncertainty = st.number_input("Uncertainty in $C$", value = planet_module.Planet.Bulk.Cuncertainty, on_change = user_input_a_variable)
#Planet.Bulk.Tb_K = st.number_input("Temperature at the bottom ($^\circ K$)", value = planet_module.Planet.Bulk.Tb_K, on_change = user_input_a_variable)
#os.environ["Planet.Bulk.Tb_K"] = str(st.number_input("Temperature at the bottom ($^\circ K$)", value = planet_module.Planet.Bulk.Tb_K))

#need to make it so that custom runs save to /PlanetProfile/Planet, and that these runs will be available for the user to load their custom runs later

os.chdir('PlanetProfileApp') #changing back to app directory so people can navigate between other pages