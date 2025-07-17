import streamlit as st
import os
import sys
from pdf2image import convert_from_path
from PIL import Image
import re
import tempfile


# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/BulkPlanetarySettings.py
RunPlanetProfile_directory = os.path.dirname(os.path.abspath(__file__))
#st.write(BulkPlanertarySettings_directory)

# Get the app directory (/PlanetProfile/PlanetProfileAPP)
app_directory = os.path.dirname(RunPlanetProfile_directory)
# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)
# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)


#os.chdir('..') #From the PlanetProfile/PlanetProfileApp, going to PlanetProfile

# Get the planet name from the environment variable
Planet = os.getenv("Planet") # e.g., "Venus"

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
    match = re.search(r'Tb\d+\.\d+K(.+)\.pdf$', filename)
    if match:
        label = match.group(1)
    else:
        label = filename[:-4] if filename.endswith('.pdf') else filename
    figure_dict[label] = os.path.join(figures_folder, filename)

figure_labels = list(figure_dict.keys()) 
tabs = st.tabs(figure_labels)

for tab, label in zip(tabs, figure_labels):
    with tab:
        pdf_path = figure_dict[label]
        with st.spinner(f"Rendering figure: {label}..."):
            images = convert_from_path(pdf_path)
            st.image(images[0], use_container_width=True)
            st.caption(f"**{label}**")



