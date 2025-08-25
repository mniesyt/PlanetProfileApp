import streamlit as st
from pdf2image import convert_from_path
import os
import sys
import pandas as pd
import re
from io import StringIO

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
planet_folder = os.path.join(parent_directory, chosen_planet)

# ----- Figure Printing in Streamlit -----
st.subheader("Outputs Produced by PlanetProfile will Appear Below")
st.markdown("---")

st.write(f"# {chosen_planet} Figures")
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
st.markdown("---")




# ----- .txt. files loading for the GUI -----
# Read all .txt files in the folder
txt_files = [f for f in os.listdir(planet_folder) if f.endswith(".txt")]

st.write(f"# {chosen_planet} text files")
tab1, tab2, tab3 = st.tabs(["Ocean text File", "Core text File", "Profile text File"])

for txt_file in txt_files:
    file_path = os.path.join(planet_folder, txt_file)

    if txt_file.endswith("Core.txt"):
        core_column_names = ["RsilTrade (m)", "RcoreTrade (m)", "rhoSilTrade (kg/m³)"]
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        data_only = "".join(lines[1:])
        df_core = pd.read_csv(StringIO(data_only), delim_whitespace=True, header=None)
        df_core.columns = core_column_names

        with tab2:
            st.subheader(f"Core Data Table: {txt_file}")
            st.dataframe(df_core, use_container_width=True)

            st.subheader("Scatter Plot")
            x_axis = st.selectbox("X-axis", df_core.columns, index=0, key=f"x_{txt_file}")
            y_axis = st.selectbox("Y-axis", df_core.columns, index=2, key=f"y_{txt_file}")
            st.scatter_chart(df_core[[x_axis, y_axis]])
            st.markdown("---")

    elif txt_file.endswith("liquidOceanProps.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        header_lines = "".join(lines[1:4]).strip()
        header_line = lines[4].strip()
        column_names = re.split(r'\s{2,}|\t+', header_line)
        data_lines = "".join(lines[5:])
        df_ocean = pd.read_csv(StringIO(data_lines), sep=r'\s+', header=None)

        with tab1:
            st.subheader(f"Ocean File Header Info: {txt_file}")
            with st.expander("Show Ocean Header (Lines 2–4)"):
                st.code(header_lines)

            if len(column_names) != df_ocean.shape[1]:
                st.warning(f"⚠️ Column count mismatch: Header has {len(column_names)} columns, data has {df_ocean.shape[1]}")
                df_ocean.columns = [f"Col_{i+1}" for i in range(df_ocean.shape[1])]
            else:
                df_ocean.columns = column_names

            st.dataframe(df_ocean, use_container_width=True)
            st.subheader("Scatter Plot")
            x_axis = st.selectbox("X-axis", df_ocean.columns, key=f"ocean_x_{txt_file}")
            y_axis = st.selectbox("Y-axis", df_ocean.columns, key=f"ocean_y_{txt_file}")
            st.scatter_chart(df_ocean[[x_axis, y_axis]])
            st.markdown("---")

    else:
        profile_column_names = [
            "P (MPa)", "T (K)", "r (m)", "phase ID", "rho (kg/m3)",
            "Cp (J/kg/K)", "alpha (1/K)", "g (m/s2)", "phi (void/solid frac)",
            "sigma (S/m)", "k (W/m/K)", "VP (km/s)", "VS (km/s)", "QS",
            "KS (GPa)", "GS (GPa)", "Ppore (MPa)", "rhoMatrix (kg/m3)",
            "rhoPore (kg/m3)", "MLayer (kg)", "VLayer (m3)", "Htidal (W/m3)", "eta (Pa s)"
        ]

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        header_info = "".join(lines[:81]).strip()
        data_str = "".join(lines[83:])
        df_profile = pd.read_csv(StringIO(data_str), sep=r'\s+', header=None, na_values=['nan'])

        with tab3:
            st.subheader(f"Profile File: {txt_file}")
            with st.expander("Show Extended Profile Header (Lines 1–81)"):
                st.code(header_info)

            if df_profile.shape[1] == len(profile_column_names):
                df_profile.columns = profile_column_names
            else:
                st.warning(f"⚠️ Column mismatch: Expected {len(profile_column_names)} headers vs {df_profile.shape[1]} data columns")
                df_profile.columns = [f"Col_{i+1}" for i in range(df_profile.shape[1])]

            st.dataframe(df_profile, use_container_width=True)
            st.subheader("Plot Profile Data")
            x_axis = st.selectbox("X-axis", df_profile.columns, key=f"profile_x_{txt_file}")
            y_axis = st.selectbox("Y-axis", df_profile.columns, key=f"profile_y_{txt_file}")
            st.scatter_chart(df_profile[[x_axis, y_axis]])
            st.markdown("---")
