import streamlit as st
import os
import sys
from pdf2image import convert_from_path
from PIL import Image
import re
import tempfile
from Utilities.planet_sidebar import show_planet_status
show_planet_status()


# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/BulkPlanetarySettings.py
RunPlanetProfile_directory = os.path.dirname(os.path.abspath(__file__))
#st.write(BulkPlanertarySettings_directory)
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


# making sure the Planet folder is in the path so can find PPPlanet
#planet_run_folder_string = '/'+str(Planet)
#full_planet_run_folder_string = parent_directory + planet_run_folder_string
#planet_run_folder = sys.path.append(os.path.join(full_planet_run_folder_string))
#figures_folder_string = full_planet_run_folder_string+ "/figures"
#planet_run_figures_folder = sys.path.append(os.path.join(figures_folder_string))
# Build path: /PlanetProfile/{Planet}/figures
figures_folder = os.path.join(parent_directory, Planet, "figures") #this does all of the commented out part above but in one step

st.set_page_config(page_title="Run Planet Profile")


if st.button("Run Planet Profile with my Choices", type = "primary"):
    st.write("Pushing your settings and choices to Planet Profile...")

    os.chdir('..')
    # Assuming user has cloned the PPApp into the same environment as PlanetProfile
    # have to move up one step out of PPApp into PP to run PP
    current_directory = os.getcwd()
    st.write(f"Current working directory: {current_directory}")
    Planet = os.getenv("Planet")
    os.system('python PlanetProfileCLI.py ' + str(Planet))



else:
    st.write("Choices have not yet been pushed to Planet Profile")

st.markdown("---")

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




