import streamlit as st
import os
import importlib
import sys
import numpy as np
from functools import partial

st.set_page_config(page_title="Layer Step Settings")
st.title("Layer Step Settings")
st.write("OPTIONAL -- Choose your Layer Step Settings Below")

# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/BulkPlanetarySettings.py
LayerStepSettings_directory = os.path.dirname(os.path.abspath(__file__))
#st.write(BulkPlanertarySettings_directory)

# Get the app directory (/PlanetProfile/PlanetProfileAPP)
app_directory = os.path.dirname(LayerStepSettings_directory)
# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)
# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)


#os.chdir('..') #From the PlanetProfile/PlanetProfileApp, going to PlanetProfile

# Get the planet name from the environment variable
Planet = st.session_state["Planet"]
if not Planet:
    st.error("Please Select a Planet on the Planet Profile Main Settings Page")
    st.stop()

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


planet_step_defaults = {"Planet.Steps.nIceI": planet_module.Planet.Steps.nIceI,
                        "Planet.Ocean.deltaP": planet_module.Planet.Ocean.deltaP,
                        "Planet.Ocean.deltaT": planet_module.Planet.Ocean.deltaT,
                        "Planet.Ocean.PHydroMax_MPa": planet_module.Planet.Ocean.PHydroMax_MPa}


# dictionary of dictionaries that each hold the label, defaults, subheaders, and descriptions of the step settings
step_settings = {
    "Planet.Steps.nIceI": {
        "label": "Number of Ice I Layer steps",
        "default": planet_module.Planet.Steps.nIceI,
        "subheader": "Ice I Layer Steps",
        "description": "Defines the number of steps for the Ice I layer. Number of steps for other layers will be calculated based on mass, radius, and moment of inertia inputs."
    },
    "Planet.Ocean.deltaP": {
        "label": "Step Size for Ocean Pressure $\Delta P$ (MPa)",
        "default": planet_module.Planet.Ocean.deltaP,
        "subheader": "Ocean Pressure Step Size",
        "description": "Increment of pressure in MPa between each layer in lower hydrosphere/ocean (sets profile resolution)."
    },
    "Planet.Ocean.deltaT": {
        "label": "Step size for Temperature $\Delta T$ ($^\circ K$)",
        "default": planet_module.Planet.Ocean.deltaT,
        "subheader": "Temperature Step Size",
        "description": "Step size in $^\circ K$ for temperature values used in generating ocean EOS functions. If set, overrides calculations that otherwise use the specified precision in user-set temperature at the bottom $^\circ K$ to determine this."
    },
    "Planet.Ocean.PHydroMax_MPa": {
        "label": "Maximum Pressure of the Hydrosphere (MPa)",
        "default": planet_module.Planet.Ocean.PHydroMax_MPa,
        "subheader": "Hydrosphere Maximum Pressure",
        "description": "Guessed maximum pressure of the hydrosphere in MPa. Must be greater than the actual pressure, but ideally not by much."
    }
}
#initializing the reset_bulk_flag in the session state as False
if "reset_step_flag" not in st.session_state:
    st.session_state["reset_step_flag"] = False


# This block is only executed when the user clicks the “Reset” button.
if st.session_state["reset_step_flag"]: #if flag is true (if user presses reset button)
    for key, val in planet_step_defaults.items():
        st.session_state[key] = val  # reloads all of the planet_defaults into session_state
    st.session_state["changed_inputs"] = {} #clears blank dictionary for changed inputs to go into later
    st.session_state["reset_step_flag"] = False #reset_bulk_flag now is set to false
    st.rerun()  # 🔁 ensures Streamlit restarts before widgets render


for key, setting in step_settings.items():
    if key not in st.session_state:
        st.session_state[key] = setting["default"]


#Initializing the changed_inputs to keep track of what variables the user has changed
if "changed_inputs" not in st.session_state:
    st.session_state["changed_inputs"] = {}  #initializing blank list for changed inputs to go into later


def on_change_step_setting(step_setting_key):
    st.session_state["changed_inputs"][step_setting_key] = True

# Create number inputs dynamically
for key, setting in step_settings.items():
    setting_name = key.split(".")[-1]

    st.subheader(setting["subheader"]) # this makes a subheader for each setting

    st.number_input(
        label=setting["label"],
        key=key,
        on_change=partial(on_change_step_setting, key)
    )

    current_value = st.session_state[key]
    setattr(eval("Planet." + ".".join(key.split(".")[1:-1])), setting_name, current_value)

    st.write(setting["description"]) #this writes out the description below the number_input
    st.markdown("---")

    if st.session_state["changed_inputs"].get(key, False):
        st.success(f"You changed **{setting['label']}** to `{current_value}`")


if st.button("🔄 Reset to module defaults (double click)"): #when user clicks reset button, 
    st.session_state["reset_step_flag"] = True #"reset_step_flag" is set to true in the session_state,
    # which triggers the if st.session_state["reset_step_flag"] function above





#st.subheader("Ice I Layer Steps")
#Planet.Steps.nIceI = st.number_input("Number of Ice I Layer steps", value = planet_module.Planet.Steps.nIceI, step = 1)
#st.write("Defines the number of steps for the Ice I layer. Number of steps for other layers will be calculated based on mass, radius, and moment of inertia inputs.")
#st.markdown("---")

#st.subheader("Ocean Pressure Step Size")
#Planet.Ocean.deltaP = st.number_input("Step Size for Ocean Pressure $\Delta P$ (MPa)", value = planet_module.Planet.Ocean.deltaP)
#st.write("Increment of pressure in MPa between each layer in lower hydrosphere/ocean (sets profile resolution)")
#st.markdown("---")

#st.subheader("Temperature Step Size")
#Planet.Ocean.deltaT = st.number_input("Step size for Temperature $\Delta T$ ($^\circ K$)", value = planet_module.Planet.Ocean.deltaT)
#st.write("Step size in $^\circ K$ for temperature values used in generating ocean EOS functions. If set, overrides calculations that otherwise use the specified precision in user-set temperature at the bottom $^\circ K$ to determine this.")
#st.markdown("---")

#st.subheader("Hydrosphere Maximum Pressure")
#Planet.Ocean.PHydroMax_MPa = st.number_input("Maximum Pressure of the Hydrosphere (MPa)", value = planet_module.Planet.Ocean.PHydroMax_MPa)
#st.write("Guessed maximum pressure of the hydrosphere in MPa. Must be greater than the actual pressure, but ideally not by much.")
#st.markdown("---")

#os.chdir('PlanetProfileApp') #changing back to app directory so people can navigate between other pages