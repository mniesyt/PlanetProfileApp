import streamlit as st
import os
import importlib
import sys
import numpy as np
from functools import partial
from Utilities.planet_sidebar import show_planet_status
show_planet_status()

st.set_page_config(page_title="Bulk Planetary Settings")

st.title("Bulk Planetary Settings")
st.set_page_config(page_icon="./PPlogo.ico")
st.write("Default values for your selected body are displayed below.")
st.write("You may also change the Bulk Planetary Settings to custom values")
st.write("Reset to defualt values with the button at the bottom of the page")
st.markdown("---")


# Get the planet object from the session state
Planet = st.session_state.get("Planet", None)

if Planet in (None, "-- Select a Planet --"):
    st.error("Please Select a Planet on the Planet Profile Main Settings Page")
    st.stop()





# Pulls default values into the app for each PPPlanet, if the user sets a new
# value then it is saved as a session state variable

# planet_defaults dictionary
#keeping track of defaults for the planet with this dicitonary {"key": value}
#to get to the values, call the key form the dicitonary (planet_defaults["Planet.Bulk.R_m"] returns the value of planet_module.Planet.Bulk.R_m
planet_bulk_defaults = {
    "Planet.Bulk.R_m": Planet.Bulk.R_m,
    "Planet.Bulk.M_kg": Planet.Bulk.M_kg,
    "Planet.Bulk.Tsurf_K": Planet.Bulk.Tsurf_K,
    "Planet.Bulk.Psurf_MPa": Planet.Bulk.Psurf_MPa,
    "Planet.Bulk.Cmeasured": Planet.Bulk.Cmeasured,
    "Planet.Bulk.Cuncertainty": Planet.Bulk.Cuncertainty,
    #"Planet.Bulk.Tb_K": planet_module.Planet.Bulk.Tb_K, THIS IS INSTEAD SET ON THE MAIN SETTINGS PAGE
}


# Bulk Settings dictionary
# e.g. "Planet.Bulk.R_m": ("Radius of the body (m)", 6.378e6),
# the keys are the same as in planet_bulk_defaults ("Planet.Bulk.R_m"), the 'value' is (label, value) with label
# being the string listed (e.g. "Radius of the body (m)") and value being the default value from planet_bulk_defaults (e.g. planet_module.Planet.Bulk.R_m)
bulk_settings = {
    key: (label, planet_bulk_defaults[key]) for key, label in {
        "Planet.Bulk.R_m": "Radius of the body (m)",
        "Planet.Bulk.M_kg": "Mass of the body (kg)",
        "Planet.Bulk.Tsurf_K": "Temperature at the surface ($^\circ K$)",
        "Planet.Bulk.Psurf_MPa": "Pressure at the surface (MPa)",
        "Planet.Bulk.Cmeasured": "Normalized Axial Moment of Inertia $C$",
        "Planet.Bulk.Cuncertainty": "Uncertainty in $C$",
        #"Planet.Bulk.Tb_K": "Temperature at the bottom ($^\circ K$) -
    }.items() #The .items() method is used on the dictionary, which returns an iterable of key-value pairs like: ("Planet.Bulk.R_m", "Radius of the body (m)"),
}

# Initialize session state for all bulk_settings -> the key is the first part in the dictionary, this initialization
# loop prevents having to initialize every variable individually as below

#Initializing the changed_inputs to keep track of what variables the user has changed
if "changed_bulk_settings_flags" not in st.session_state:
    st.session_state["changed_bulk_settings_flags"] = {}  #initializing blank list for changed inputs to go into later
if "changed_bulk_settings" not in st.session_state:
    st.session_state["changed_bulk_settings"] = {}  # key: value

#this block runs every time the page loads
for key, (_, default_val) in bulk_settings.items(): #initializes variables into session_state
    if key not in st.session_state: #this means only not already created keys will be added to session state
        st.session_state[key] = default_val #now, all bulk settings are in the session state


#initializing the reset_bulk_flag in the session state as False
if "reset_bulk_flag" not in st.session_state:
    st.session_state["reset_bulk_flag"] = False


# This block is only executed when the user clicks the “Reset” button.
if st.session_state["reset_bulk_flag"]: #if flag is true (if user presses reset button)
    for key, val in planet_bulk_defaults.items():
        st.session_state[key] = val  # reloads all of the planet_defaults into session_state
    st.session_state["changed_bulk_settings_flags"] = {} #clears the changed_bulk_settings_flags dictionary
    st.session_state["changed_bulk_settings"] = {} #clears the changed_bulk_settings dictionary
    st.session_state["reset_bulk_flag"] = False #reset_bulk_flag now is set to false
    st.rerun()  # ensures Streamlit restarts before widgets render





# This function is used to keep track of what settings the user has changed, so that the
# code can print out what settings have been changed
def on_change_bulk_setting(bulk_setting_key):
    st.session_state["changed_bulk_settings_flags"][bulk_setting_key] = True
    st.session_state["changed_bulk_settings"][bulk_setting_key] = st.session_state[bulk_setting_key]
    #if a user changes an input,
    # This looks up the "changed_bulk_settings" dictionary inside st.session_state and
    # adds a new entry to this dictionary with the key bulk_setting_key (the name of the setting that was changed),
    # and flags it as a setting that has been changed --> this flag will be used on the RunPlanetProfile page to actually update the values of the semi-custom planet
    # The second line then keeps track of the values that the user has selected for those settings



# Create number inputs dynamically
for key, (label, _) in bulk_settings.items():
    #iterating over all of the key, (label,_) pairs in bulk_settings.items()
    #we are only doing things with they key and label, so the actual value is ignored with _
    setting_name = key.split(".")[-1] # this grabs just the key i.e. just Tb_K from "Planet.Bulk.Tb_K"
    #(key.split(".") splits the key into ["Planet", "Bulk", "R_m"] amd [-1] grabs the last object "R_m" in the list )

    # Create input widgets
    st.number_input(
        label, #this prints the label for what the number_input widget shows
        key = key, #this loads the default value into the widget -> the key calls the default value from the session state
        on_change = partial(on_change_bulk_setting, key) #using partial funciton because you can only pass a callable here, not a function call
        #if the user changes the value, then on_change_bulk_setting is called
    )

    current_value = st.session_state[key] #pulls the current value of the setting from the session_state usings its key

    #the actual updating of the Planet object will only happen on the Run Planet Profile page
    #setattr(Planet.Bulk, setting_name, current_value) #setattr(object, attribute, value) -> sets Planet.Bulk.setting_name to current_value



if st.button("🔄 Reset to default bulk settings (double click)"): #when user clicks reset button,
    st.session_state["reset_bulk_flag"] = True #"reset_bulk_flag" is set to true in the session_state,
    # which triggers the if st.session_state["reset_bulk_flag"] function above
