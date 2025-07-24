import streamlit as st
import os
import importlib
import sys


# --- Setting up Main Page ---
st.set_page_config(page_title="Planet Profile Main")
st.title("Planet Profile")
st.write("Let's Start by Setting Up Your Planet")
st.markdown("---")


#--- Planet Selection - Custom or from dropdown ---
planet_list = ["-- Select a Planet --", "Ariel", "Callisto", "Dione", "Enceladus", "Europa", "Ganymede",
               "Iapetus", "Io", "Luna", "Mimas", "Miranda", "Oberon", "Pluto",
               "Rhea", "Tethys", "Titan", "Titania", "Triton", "Umbriel"]

# Initialzing all of the things to session state
if "planet_selectbox" not in st.session_state:
    st.session_state["ChosenPlanet"] = "-- Select a Planet --"

if "Planet" not in st.session_state:
    st.session_state["Planet"] = None

if "run_custom_body" not in st.session_state:
    st.session_state["run_custom_body"] = False

# Option for user to select fully custom planet
st.subheader("Run fully custom Planet?")
st.write(
    "Planet Profile has profiles of many moons ready for you to use. "
    "If you want to create your own moon, check the box below. "
    "Otherwise, choose from existing planetary bodies."
)

# Checkbox manages if the user wants to run a custom planet or not
run_custom_body = st.checkbox("Create fully custom Planet?", value=st.session_state["run_custom_body"], key="run_custom_body")

# Custom Planet path
if run_custom_body:
    st.session_state["ChosenPlanet"] = "Custom"
    st.session_state["Planet"] = None  # Custom settings handled elsewhere
    st.success("Using Custom Planet. Configure settings in other tabs.")

else:
    st.markdown("---")
    st.subheader("Body Selection")
    st.write("Please select a planetary body from the list of profiles below")

    selected_planet = st.selectbox(
        "Choose your Planetary Body:",
        planet_list,
        #index=planet_list.index(st.session_state["planet_selectbox"]),
        key="planet_selectbox"
    )
    if selected_planet != "-- Select a Planet --":
        st.session_state["ChosenPlanet"] = selected_planet

chosen_planet = st.session_state.get("ChosenPlanet", None)

# --- Checks and load planet ---
if chosen_planet == "-- Select a Planet --":
    st.warning("Please select a planetary body to continue.")
    st.stop()
else:
    # Updates the session state to the chosen planet
    st.sidebar.markdown(f"**Current Planet:**  {chosen_planet}")
    st.success(f"Using Planet: {chosen_planet}")


# --- File Path Management as well as loading of planet default data ---

# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/pages/PlanetProfileMainSettings.py
PlanetProfileMainSettings_directory = os.path.dirname(os.path.abspath(__file__))

# Get the app directory (/PlanetProfile/PlanetProfileApp)
app_directory = os.path.dirname(PlanetProfileMainSettings_directory)
if app_directory not in sys.path:
    sys.path.append(app_directory)


# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)

# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)

# --- Load planet module ---
if chosen_planet != "Custom":
    from Utilities.PlanetLoader import load_planet_module

    try:
        planet_module = load_planet_module(parent_directory, chosen_planet)
        st.success(f"{chosen_planet} data loaded.")
    except Exception as e:
        st.error(f"Error loading planet module: {e}")
        st.stop()


    # Construct the Planet object
    #from PlanetProfile.Utilities.defineStructs import PlanetStruct, Constants
    # Store the planet object in session state
    st.session_state["Planet"] = planet_module.Planet
    #st.write(st.session_state["Planet"])

Planet = st.session_state.get("Planet", None)

# need to add what happens if the user selects custom here


# --- Main Settings Options Begin here- Tb_K and  Ocean Compositions ---

st.markdown("---")
st.subheader("Ice Layer Thickness")

thickness_or_Tb = st.selectbox("Select how you would like Planet profile to set up your Ice Shell. Descriptions of each type display when selected for more information", ("Input Ice Shell thickness", "Input Bottom Temperature Tb_K"))



#Planet is currently just a string. In other pages we turn it into an object with attributes but we have not done that here
if thickness_or_Tb == "Input Ice Shell thickness":
    Planet.Bulk.zb_approximate_km = st.number_input("Select the thickness of your Ice I Shell (in  $km$) below")
    st.write("Planet Profile will use the inputted ice layer thickness to generate the ice shell for your planet. Based on the ice shell thickness, the temperature at the bottom of the Ice shell will be calculated")


    # Ensure Planet.Do exists and is a dictionary
    if not hasattr(Planet.Do, "ICEIh_THICKNESS"):
        Planet.Do.ICEIh_THICKNESS = True #if the attribute doesn't exist, this is making it and setting it to true
    else:
        Planet.Do.ICEIh_THICKNESS = True  #  #user is inputting the thickness instead of Tb_K so the thickness flag is set to true




if thickness_or_Tb == "Input Bottom Temperature Tb_K":
    Planet.Bulk.Tb_K =st.number_input("Select Your Bottom Temperature (in  $^\circ K$) - Primarily for PlanetProfile Developers")
    # User Passes in a Temperature of the bottom of the ocean
    st.write("The temperature you select at the bottom of the ocean layer for your planet is used by Planet Profile to determine the thickness of the Ice Shell thickness. Behind the scenes, this sets Planet.Bulk.Tb_K")




st.markdown("---")

st.subheader("Ocean Composition")
user_ocean_type = st.selectbox("Use Predefined Ocean or Define own Ocean Composition", ("Use pre-defined ocean composition","Define your own ocean composition"),index = None, placeholder = "Select Ocean Type")
#User selects which water they want to use, will have to call from prespecified options list


if user_ocean_type == "Use pre-defined ocean composition":
   st.selectbox("Choose Predefined Ocean", ("Pure H2O", "Seawater", "MgSO4", "NaCl"))



if user_ocean_type == "Define your own ocean composition":
    st.write("Define Your Ocean Below")
# will have to add an option to select concentration units
    species_concentration_unit = st.selectbox("Choose Salt Species Concentration Units", ("absolute mol/kg", "relative ratios"))
    num_salts = st.number_input("Input number of salt species", min_value = 1)
    num_salts_list = [int(digit) for digit in str(num_salts)]
    salt_name_list = []
    salt_conc_list = []
    st.markdown("---")
    for num in range(num_salts_list[0]):
        st.write("Salt Species", str(num+1))
        salt_name_list.append(st.text_input("Input name of Salt " + str(num+1)))
        salt_conc_list.append(st.text_input("Input Concentration of Salt " + str(num+1)))
        st.markdown("---")
    #st.write(salt_name_list)
    #st.write(salt_conc_list)
    #st.write(species_concentration_unit)
