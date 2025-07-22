import streamlit as st
import os
import importlib
import sys


# Main page content
st.set_page_config(page_title="Planet Profile Main")



st.title("Planet Profile")
st.write("Let's Start by Setting Up Your Planet")
st.markdown("---")


st.subheader("Run fully custom Planet?")
st.write("Planet Profile has many profiles of moons ready for you to use. If you want to play around and create your own moon, check the box below. If you want to use " \
    "pre-existing moons and their properties, skip the checkbox and proceed below to select your planetary body")
run_custom_body = st.checkbox("Create fully custom Planet?", value=False)


if run_custom_body:
    st.write("Let's create your fully custom planet. Set the main Planet Profile settings below, then set your Bulk Planetary Settings,Laer Step Settings, and Figure Settings on the other tabs")
    st.session_state["Planet"] = "Custom"
    
# will eventually have to have an actual call to the list of available moons from planet profile directly
planet_list = ["-- Select a Planet --", "Ariel", "Callisto", "Dione", "Enceladus", "Europa", "Ganymede", 
                                     "Iapetus", "Io", "Luna", "Mimas", "Miranda", "Oberon", "Pluto", 
                                     "Rhea", "Tethys", "Titan", "Titania", "Triton", "Umbriel"]



if not run_custom_body:
    st.markdown("---")
    st.subheader("Body Selection")
    st.write("Please select a planetary body from the list of profiles below")
    selected_planet = st.selectbox(
        "Choose your Planetary Body:", 
        planet_list,
        key="Planet" #this sets a key for the Planet that the user has selected- the session state will use this key to keep track of the planet taht has been picked
)
    #Safe read from session_state
    Planet = st.session_state.get("Planet", "-- Select a Planet --")

    if Planet == "-- Select a Planet --":
        st.warning("Please select a planetary body to continue.")
        st.stop()



#Setting up the fle path for all future pages here

# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/pages/PlanetProfileMainSettings.py
PlanetProfileMainSettings_directory = os.path.dirname(os.path.abspath(__file__))


# Get the app directory (/PlanetProfile/PlanetProfileApp)
app_directory = os.path.dirname(PlanetProfileMainSettings_directory)

if app_directory not in sys.path:
    sys.path.append(app_directory)

from Utilities.PlanetLoader import load_planet_module



# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)

# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)
#now, setting up session state to manage 




# Get the planet name from the session state
Planet = st.session_state["Planet"]
if not Planet:
    st.error("Please Select a Planet on the Planet Profile Main Settings Page")
    st.stop()

#loading Planet default data for user
if Planet and Planet != "Custom":
    try:
        planet_module = load_planet_module(parent_directory, Planet) #loading the data 
        st.success(f"{Planet} data loaded.")
    except Exception as e:
        st.error(f"Error loading planet module: {e}")



#Planet = os.getenv("Planet") -> how to call the chosen planet in other parts of the code later

st.markdown("---")
st.subheader("Ice Layer Thickness")

thickness_or_Tb = st.selectbox("Select how you would like Planet profile to set up your Ice Shell. Descriptions of each type display when selected for more information", ("Input Ice I Layer thickness ", "Input Bottom Temperature Tb_K"))

if thickness_or_Tb == "Input Ice Shell thickness":
    st.number_input("Select the thickness of your Ice I Shell (in  $m$) below")
    st.write("Planet Profile will use the inputted ice layer thickness to generate the ice shell for your planet. Based on the ice shell thickness, the temperature at the bottom of the Ice shell will be calculated")
    #Planet.Do.ICEIh_THICKNESS = True
    #Planet.Bulk.zb_approximate_km = 30 # The approximate ice shell thickness desired (edited) 



if thickness_or_Tb == "Input Bottom Temperature Tb_K":
    st.number_input("Select Your Bottom Temperature (in  $^\circ K$) - Primarily for PlanetProfile Developers")
    # User Passes in a Temperature of the bottom of the ocean
    st.write("The temperature you select at the bottom of the ocean layer for your planet is used by Planet Profile to determine the thickness of the Ice Shell thickness. Behind the scenes, this sets Planet.Bulk.Tb_K")
    #Planet.Bulk.Tb_K = 


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
 

