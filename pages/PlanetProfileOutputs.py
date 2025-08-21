import streamlit as st
from pdf2image import convert_from_path
import os
import sys

# ----- Page setup stuff -----
from Utilities.planet_sidebar import show_planet_status
show_planet_status()
st.set_page_config(page_icon = "./PPlogo.ico")
st.set_page_config(page_title = "PlanetProfile Outputs")
st.title("PlanetProfile Outputs")



# ----- File Path management -----
# Get the planet name from the session state
Planet = st.session_state.get("Planet", None)
if not Planet:
    st.error("Please Select a Planet on the Planet Profile Main Settings Page")
    st.stop()

chosen_planet = st.session_state.get("ChosenPlanet", None)

# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/RunPlanetProfile.py
RunPlanetProfile_directory = os.path.dirname(os.path.abspath(__file__))

# Get the app directory (/PlanetProfile/PlanetProfileApp)
app_directory = os.path.dirname(RunPlanetProfile_directory)

# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)

# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)

figures_folder = os.path.join(parent_directory, chosen_planet, "figures")


# ----- Figure Printing in Streamlit -----
st.subheader("Figures Produced by PlanetProfile will Appear Below")

pdf_files = [f for f in os.listdir(figures_folder) if f.endswith(".pdf")]

if not pdf_files:
    st.warning(f"No figure PDFs found in: {figures_folder}")
    st.stop()

figure_dict = {} #empty so we can update it later

# This dictionary is used to parse the figure file names and link them to figure titles in the GUI
figure_types = {
    "Gravity" : "Gravity and Pressure",
    "Wedge" : "Interior Wedge Diagram",
    "Hydrosphere" : "Hydrosphere Properties",
    "CoreMantTrade" : "Silicate-Core Size Tradeoff",
    "MantleDens" : "Silicate Radius-Density Handoff",
    "Seismic" : "Seismic Properties",
    "Viscosity" : "Viscosity",
    "Porosity2axes": "Porosity with 2 axes",
    "Porosity" : "Porosity"}


# This does the actual parsing of the figure file names
for filename in pdf_files:
    if filename.endswith('.pdf'):
        name_only = filename[:-4]
        matched_keyword = None

        for keyword in figure_types:
            if keyword in name_only:
                matched_keyword = keyword
                break

        # Uses slightly more descriptive title from the figure_types dictionary above
        label = figure_types.get(matched_keyword, matched_keyword if matched_keyword else name_only)
        figure_dict[label] = os.path.join(figures_folder, filename)

figure_labels = list(figure_dict.keys())
tabs = st.tabs(figure_labels)

#Below are descriptive captions for the figures, linked via dictionary to the titles for those figures
captions = {
    "Interior Wedge Diagram": "Shows an interior wedge diagram showing the calculations of the radii of each planet layer",
     "Gravity and Pressure": "Gravitational acceleration (g) and Pressure profiles as a function of radius",
    "Hydrosphere Properties": (
        "Interior Properties- \n\n"
        "Left: Phase diagram as a funciton of pressure and density. \n\n"
        "Right(Top): Temperature profile across different depths.\n\n"
        "Right(center): Longitudinal (p-wave) sound velocity Vp for each layer in km/s and shear (s-wave) sound velocity Vs for each layer in km/s as a funciton of depth, \n\n"
        "Right(Bottom): Electrical conductivity as a funciton of depth"),

    "Silicate-Core Size Tradeoff" : "Silicate–core size tradeoff - Based on given Moment of Inertia, calculates all profiles of silicate and core size pairs that fit within that gien MOI. The one determined by Planet Profile to most closely match the given MOI is marked on the figure",
    "Silicate Radius-Density Handoff" : "Silicate radius-density tradeoff - Based on given Moment of Inertia, calculates all profiles of silicate radii and densities that fit within that gien MOI. The one determined by Planet Profile to most closely match the given MOI is marked on the figure",
    "Porosity" : "Left: Porosity as a funciton of depth. Right: Porosity as a funciton of pressure",
    "Porosity with 2 axes": "Displays Porosity both as a function of depth and as a funciton of pressure on one figure" ,
    "Viscosity" : "Viscosity of the planet layers as a funciton of radius",
    "Seismic Properties" : (
        "Seismic Properties. \n\n"
        "Top Left - Bulk & shear moduli Ks & Gs as a function of radius. \n\n"
        "Top Right - Temperature, Pressure, and density as a funciton of radius. \n\n"
        "Bottom Left - Sound speeds Vp and Vs as a function of radius. \n\n"
        "Bottom Right - Seismic quality factor Qs as a funciton of raidus")
}


# This actually prints the figures in the GUI with the titles, tabs, and captions
for tab, label in zip(tabs, figure_labels):
    with tab:
        pdf_path = figure_dict[label]
        with st.spinner(f"Rendering figure: {label}..."):
            images = convert_from_path(pdf_path)
            st.image(images[0], use_container_width=True)

            caption = captions.get(label, f"{label}")
            st.caption(f"**{caption}**")
