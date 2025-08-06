import streamlit as st
import os
import sys
from pdf2image import convert_from_path
from PIL import Image
import re
import tempfile
from Utilities.planet_sidebar import show_planet_status
show_planet_status()
from copy import deepcopy


# ----- Page setup stuff -----
st.set_page_config(page_icon="./PPlogo.ico")
st.set_page_config(page_title="Run Planet Profile")
st.title("Run Planet Profile")
st.subheader("Summary of Your Planet and Changes you have made from Defaults:")



# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/BulkPlanetarySettings.py
RunPlanetProfile_directory = os.path.dirname(os.path.abspath(__file__))
# Get the app directory (/PlanetProfile/PlanetProfileApp)
app_directory = os.path.dirname(RunPlanetProfile_directory)
# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)
# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)

# Get the planet name from the session state
Planet = st.session_state.get("Planet", None)
if not Planet:
    st.error("Please Select a Planet on the Planet Profile Main Settings Page")
    st.stop()

# This initializes the changed settings dictionaries in the event that the user did not visit that particular page
for key in ["changed_bulk_settings_flags", "custom_ocean_flag", "changed_step_settings_flags", "changed_core_settings"]:
    if key not in st.session_state:
        # For the boolean custom_ocean_flag, initialize as False; for the others, use empty dict
        st.session_state[key] = False if key == "custom_ocean_flag" else {}


chosen_planet = st.session_state.get("ChosenPlanet", None)

# If the user has changed any inputs, we will create a semi-custom Planet object here to push their changes to
# Check if *any* setting has been changed
any_changes_made = (
    st.session_state["custom_ocean_flag"]
    or any(st.session_state["changed_bulk_settings_flags"].values())
    or any(st.session_state["changed_step_settings"].values())
    or any(st.session_state["changed_core_settings"].values())
)

# Conditionally create SemiCustomPlanet
if any_changes_made:
    SemiCustomPlanet = deepcopy(Planet)
    st.markdown("### Creating modified Planet based on user settings...")
    st.markdown("---")
else:
    SemiCustomPlanet = Planet  # No changes, use original
    st.info("No settings were modified. Running with default Planet.")
    st.markdown("---")

figures_folder = os.path.join(parent_directory, chosen_planet, "figures")

if any_changes_made:

    st.markdown("## Custom Bulk Settings Applied")
    # If the user has changed any bulk planetary settings, they will be updated into the SemiCustomPlanet object here
    for key, changed in st.session_state["changed_bulk_settings_flags"].items():
        if changed:
            setting_name = key.split(".")[-1]
            value = st.session_state["changed_bulk_settings"][key]
            setattr(SemiCustomPlanet.Bulk, setting_name, value)


    # This prints out for the user any of the bulk planetary settings they have changed from the default here
    if any(st.session_state["changed_bulk_settings_flags"].values()):
        st.warning("You have changed the following settings from the defaults: ")
        for key, was_changed in st.session_state["changed_bulk_settings_flags"].items():
            if was_changed:
                bulk_setting_name = key.split(".")[-1]
                bulk_new_val = st.session_state["changed_bulk_settings"][key]
                bulk_default_val = getattr(Planet.Bulk, bulk_setting_name, "N/A")

                st.markdown(f"- **{bulk_setting_name}**: `{bulk_default_val}` → `{bulk_new_val}`")
    else:
        st.info("No bulk settings have been changed. Using default bulk planetary settings.")
    st.markdown("---")



    # If the user has changed any ocean settings, they will be updated into the SemiCustomPlanet object here and printed for the user
    st.markdown("## Custom Ocean Settings Applied")
    running_custom_ocean = st.session_state.get("custom_ocean_flag")
    if running_custom_ocean == True:
        st.warning("You are using an ocean different than the default ocean")
        custom_ocean_comp = st.session_state.get("custom_ocean_comp")
        st.write("Your current ocean configuration is: " + custom_ocean_comp)
        SemiCustomPlanet.Ocean.comp = custom_ocean_comp

    if running_custom_ocean == False:
        st.info("No ocean settings have been changed. Using default ocean.")


    st.markdown("---")


    st.markdown("## Custom Layer Step Settings Applied")
    # If the user has changed any layer step settings, they will be updated into the SemiCustomPlanet object here and printed for the user
    if any(st.session_state["changed_step_settings_flags"].values()):
        st.warning("You have changed the following settings from the defaults: ")
        for key, changed in st.session_state["changed_step_settings_flags"].items():
            if changed:
                label = step_settings[key]["label"]
                setting_name = key.split(".")[-1]
                default_val = step_settings[key]["default"]
                new_val = st.session_state["changed_step_settings"][key]
                st.markdown(f"- **{label}** (`{setting_name}`): `{default_val}` → `{new_val}`")
    else:
        st.info("No step settings have been changed. All values are defaults.")
    st.markdown("---")


    st.markdown("## Custom Core and Silicate Settings Applied")
    # If the user has changed any core and silicate settings, they will be updated into the SemiCustomPlanet object here and printed for the user
    if any(st.session_state["changed_core_settings"].values()):
        st.warning("You have changed the following settings from the defaults: ")
        for key, changed in st.session_state["changed_core_settings"].items():
            if changed:
                label = step_settings[key]["label"]
                setting_name = key.split(".")[-1]
                default_val = step_settings[key]["default"]
                new_val = st.session_state["changed_core_settings"][key]
                st.markdown(f"- **{label}** (`{setting_name}`): `{default_val}` → `{new_val}`")
    else:
        st.info("No step settings have been changed. All values are defaults.")
    st.markdown("---")


if st.button("Run Planet Profile with my Choices", type = "primary"):
    st.write("Pushing your settings and choices to Planet Profile...")

    os.chdir('..')
    # Assuming user has cloned the PPApp into the same environment as PlanetProfile
    # have to move up one step out of PPApp into PP to run PP
    current_directory = os.getcwd()
    st.write(f"Current working directory: {current_directory}")
    #Planet = os.getenv("Planet")
    os.system('python PlanetProfileCLI.py ' + str(chosen_planet))



else:
    st.write("Choices have not yet been pushed to Planet Profile")

st.markdown("---")

# ----- Figure Printing in Streamlit -----

st.subheader("Figures Produced by Planet Profile will Appear Below")

pdf_files = [f for f in os.listdir(figures_folder) if f.endswith(".pdf")]

if not pdf_files:
    st.warning(f"No figure PDFs found in: {figures_folder}")
    st.stop()

figure_dict = {}
for filename in pdf_files:
    match = re.search(r'([A-Z][a-zA-Z0-9_]*)\.pdf$', filename)
    if match:
        label = match.group(1)
    else:
        label = filename[:-4] if filename.endswith('.pdf') else filename
    figure_dict[label] = os.path.join(figures_folder, filename)

figure_labels = list(figure_dict.keys())
tabs = st.tabs(figure_labels)

#Below are descriptive captions for the figures
captions = {
    "Wedge": "Shows an interior wedge diagram showing the calculations of the radii of each planet layer",
    "Gravity": "Gravitational acceleration (g) and Pressure profiles as a function of radius",
    "Hydrosphere": (
        "Interior Properties- \n\n"
        "Left: Phase diagram as a funciton of pressure and density. \n\n"
        "Right(Top): Temperature profile across different depths.\n\n"
        "Right(center): Longitudinal (p-wave) sound velocity Vp for each layer in km/s and shear (s-wave) sound velocity Vs for each layer in km/s as a funciton of depth, \n\n"
        "Right(Bottom): Electrical conductivity as a funciton of depth"),

    "CoreMantTrade": "Silicate–core size tradeoﬀ - Based on given Moment of Inertia, calculates all profiles of silicate and core size pairs that fit within that gien MOI. The one determined by Planet Profile to most closely match the given MOI is marked on the figure",
    "MantleDens": "Silicate radius-density tradeoff - Based on given Moment of Inertia, calculates all profiles of silicate radii and densities that fit within that gien MOI. The one determined by Planet Profile to most closely match the given MOI is marked on the figure",
    "Porosity" : "Left: Porosity as a funciton of depth. Right: Porosity as a funciton of pressure",
    "Porosity2axes": "Displays Porosity both as a function of depth and as a funciton of pressure on one figure" ,
    "Viscosity" : "Viscosity of the planet layers as a funciton of radius",
    "Seismic" : (
        "Seismic Properties. \n\n"
        "Top Left - Bulk & shear moduli Ks & Gs as a function of radius. \n\n"
        "Top Right - Temperature, Pressure, and density as a funciton of radius. \n\n"
        "Bottom Left - Sound speeds Vp and Vs as a function of radius. \n\n"
        "Bottom Right - Seismic quality factor Qs as a funciton of raidus")


}



for tab, label in zip(tabs, figure_labels):
    with tab:
        pdf_path = figure_dict[label]
        with st.spinner(f"Rendering figure: {label}..."):
            images = convert_from_path(pdf_path)
            st.image(images[0], use_container_width=True)

            caption = captions.get(label, f"{label}")
            st.caption(f"**{caption}**")
