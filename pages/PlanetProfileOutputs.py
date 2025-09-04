import streamlit as st
from pdf2image import convert_from_path
import os
import sys
import pandas as pd
import re
from io import StringIO
import altair as alt
import time
from collections import defaultdict
from datetime import datetime



# ----- Page setup stuff -----
from Utilities.planet_sidebar import show_planet_status
show_planet_status()
st.set_page_config(page_icon = "./PPlogo.ico")
st.set_page_config(page_title = "PlanetProfile Outputs")
st.title("PlanetProfile Outputs")

st.subheader("Outputs Produced by PlanetProfile will Appear Below")
st.markdown("---")

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
st.write(f"# {chosen_planet} Figures")


# ----- Batching and timestamping figures  -----
BATCH_TIME_THRESHOLD_SECONDS = 60  # Groups files created within 60 seconds (can change this threshold as needed)

# Loads and timestamps all PDFs
pdf_file_paths = []
for filename in os.listdir(figures_folder):
    if filename.endswith(".pdf"):
        path = os.path.join(figures_folder, filename)
        mod_time = os.path.getmtime(path)
        pdf_file_paths.append((path, mod_time))

# Sorts PDF files by modification time
pdf_file_paths.sort(key=lambda x: x[1])

# Empty dictionaries to add batches to
batches = []
current_batch = []
prev_time = None
# Grouping the PDF files into batches
for path, mod_time in pdf_file_paths:
    if prev_time is None or (mod_time - prev_time) <= BATCH_TIME_THRESHOLD_SECONDS:
        current_batch.append((path, mod_time))
    else:
        batches.append(current_batch)
        current_batch = [(path, mod_time)]
    prev_time = mod_time
# adds files to batches
if current_batch:
    batches.append(current_batch)

# funtion to create tab titles for each batch based on timestamp - to eventually be Overwritten with something that is more descriptive/the dicitonary mapping Scott is
#going to work on that maps file names with the user-named module that created it
def format_batch_label(batch):
    if not batch:
        return "Unknown Batch"
    timestamp = datetime.fromtimestamp(batch[0][1])
    return timestamp.strftime("Batch %Y-%m-%d %H:%M:%S")

batch_labels = [format_batch_label(batch) for batch in batches]

# Outer tabs - grouped by time
outer_tabs = st.tabs(batch_labels)



# ----- Figure Printing and Setup of Captions and Figure Types -----
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


# This creates the inner tabs of the figures files based on the figure type
for tab, batch in zip(outer_tabs, batches):
    with tab:
        # --- Map figure types for this batch ---
        figure_dict = {}

        for filepath, _ in batch:
            filename = os.path.basename(filepath)
            name_only = filename[:-4]

            matched_keyword = None
            for keyword in figure_types:
                if keyword in name_only:
                    matched_keyword = keyword
                    break

            label = figure_types.get(matched_keyword, matched_keyword if matched_keyword else name_only)
            figure_dict[label] = filepath  # Use figure title as key

        # Sort figure labels alphabetically for consistent order
        figure_labels = sorted(figure_dict.keys())
        inner_tabs = st.tabs(figure_labels)

        # --- Display each figure in inner tab ---
        for fig_tab, label in zip(inner_tabs, figure_labels):
            with fig_tab:
                pdf_path = figure_dict[label]
                with st.spinner(f"Rendering: {label}..."):
                    images = convert_from_path(pdf_path)
                    st.image(images[0], use_container_width=True)
                st.caption(f"**{captions.get(label, label)}**")
st.markdown("---")




# ----- .txt. files loading for the GUI -----
st.write(f"# {chosen_planet} text files")
# Get list of .txt files and their modification times
# Step 1: Get list of .txt files and their modification times
txt_files = [
    (f, os.path.getmtime(os.path.join(planet_folder, f)))
    for f in os.listdir(planet_folder)
    if f.endswith(".txt")
]

# Sort by modification time
txt_files.sort(key=lambda x: x[1])

# Step 2: Group files into batches by timestamp (90 seconds apart)
threshold = 90  # seconds
batches = []
current_batch = []
last_ts = None

for file, ts in txt_files:
    if last_ts is None or (ts - last_ts) <= threshold:
        current_batch.append((file, ts))
    else:
        batches.append(current_batch)
        current_batch = [(file, ts)]
    last_ts = ts

if current_batch:
    batches.append(current_batch)

# Format batch labels
formatted_batches = []
for i, batch in enumerate(batches):
    timestamp = datetime.fromtimestamp(batch[0][1]).strftime('%Y-%m-%d %H:%M:%S')
    label = f"Batch {i + 1} ({timestamp})"
    file_list = [f for f, _ in batch]
    formatted_batches.append((label, file_list))

st.write(f"# {chosen_planet} text files grouped by batch and file type")

# Step 3: Outer tabs for batches
batch_labels = [label for label, files in formatted_batches]
batch_tabs = st.tabs(batch_labels)

for batch_idx, (batch_label, files) in enumerate(formatted_batches):
    with batch_tabs[batch_idx]:
        # Step 4: Inner tabs for file types
        inner_tabs = st.tabs(["Ocean text File", "Core text File", "Profile text File"])

        # Prepare dict to hold files by type
        files_by_type = {
            "Ocean": [f for f in files if f.endswith("liquidOceanProps.txt")],
            "Core": [f for f in files if f.endswith("Core.txt")],
            "Profile": [f for f in files if not (f.endswith("Core.txt") or f.endswith("liquidOceanProps.txt"))]
        }



# Read all .txt files in the folder
#txt_files = [f for f in os.listdir(planet_folder) if f.endswith(".txt")]



# ----- Printing of the liquidOceanProps.txt file table and scatter plot -----
     # ----- Ocean files -----
        with inner_tabs[0]:
            for ocean_file in files_by_type["Ocean"]:
                file_path = os.path.join(planet_folder, ocean_file)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                header_lines = "".join(lines[1:4]).strip()
                header_line = lines[4].strip()
                column_names = re.split(r'\s{2,}|\t+', header_line)
                data_lines = "".join(lines[5:])
                df_ocean = pd.read_csv(StringIO(data_lines), sep=r'\s+', header=None)

                st.subheader(f"Ocean File Header Info: {ocean_file}")
                with st.expander("Show Ocean Header (Lines 2–4)"):
                    st.code(header_lines)

                if len(column_names) != df_ocean.shape[1]:
                    st.warning(f"⚠️ Column count mismatch: Header has {len(column_names)} columns, data has {df_ocean.shape[1]}")
                    df_ocean.columns = [f"Col_{i+1}" for i in range(df_ocean.shape[1])]
                else:
                    df_ocean.columns = column_names

                st.dataframe(df_ocean, use_container_width=True)
                st.subheader("Scatter Plot")

                persist_plot = st.checkbox("Plot multiple Y-axes against same X-axis", key=f"persist_{ocean_file}")
                x_axis = st.selectbox("X-axis", df_ocean.columns, key=f"x_{ocean_file}")

                if persist_plot:
                    y_axes = st.multiselect(
                        "Y-axis (select one or more)",
                        df_ocean.columns.drop(x_axis),
                        default=[df_ocean.columns[1]] if x_axis != df_ocean.columns[1] else df_ocean.columns[2:3],
                        key=f"multi_y_{ocean_file}"
                    )
                else:
                    y_axes = [st.selectbox("Y-axis", df_ocean.columns.drop(x_axis), key=f"single_y_{ocean_file}")]

                valid_y_axes = [y for y in y_axes if y != x_axis]

                if valid_y_axes:
                    # Convert columns to numeric (coerce errors to NaN)
                    df_ocean[x_axis] = pd.to_numeric(df_ocean[x_axis], errors='coerce')
                    for col in valid_y_axes:
                        df_ocean[col] = pd.to_numeric(df_ocean[col], errors='coerce')

                    df_plot = df_ocean[[x_axis] + valid_y_axes].dropna()
                    df_plot = df_plot.set_index(x_axis)[valid_y_axes]

                    if not df_plot.empty:
                        st.scatter_chart(df_plot)
                    else:
                        st.info("No valid data to plot after cleaning.")
                else:
                    st.info("Please select a Y-axis different from the X-axis to plot.")

        # ----- Core files -----
        with inner_tabs[1]:
            core_column_names = ["RsilTrade (m)", "RcoreTrade (m)", "rhoSilTrade (kg/m³)"]
            for core_file in files_by_type["Core"]:
                file_path = os.path.join(planet_folder, core_file)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                data_only = "".join(lines[1:])
                df_core = pd.read_csv(StringIO(data_only), sep='\s+', header=None)
                df_core.columns = core_column_names

                st.subheader(f"Core Data Table: {core_file}")
                st.dataframe(df_core, use_container_width=True)

                st.subheader("Scatter Plot")

                persist_plot = st.checkbox("Plot multiple Y-axes against same X-axis", key=f"persist_core_{core_file}")
                x_axis = st.selectbox("X-axis", df_core.columns, key=f"x_core_{core_file}")

                if persist_plot:
                    y_axes = st.multiselect(
                        "Y-axis (select one or more)",
                        df_core.columns.drop(x_axis),
                        default=[df_core.columns[1]] if x_axis != df_core.columns[1] else df_core.columns[2:3],
                        key=f"multi_y_core_{core_file}"
                    )
                else:
                    y_axes = [st.selectbox("Y-axis", df_core.columns.drop(x_axis), key=f"single_y_core_{core_file}")]

                valid_y_axes = [y for y in y_axes if y != x_axis]

                if valid_y_axes:
                    df_plot = df_core.set_index(x_axis)[valid_y_axes]
                    st.scatter_chart(df_plot)
                else:
                    st.info("Please select a Y-axis different from the X-axis to plot.")

        # ----- Profile files -----
        with inner_tabs[2]:
            profile_column_names = [
                "P (MPa)", "T (K)", "r (m)", "phase ID", "rho (kg/m3)",
                "Cp (J/kg/K)", "alpha (1/K)", "g (m/s2)", "phi (void/solid frac)",
                "sigma (S/m)", "k (W/m/K)", "VP (km/s)", "VS (km/s)", "QS",
                "KS (GPa)", "GS (GPa)", "Ppore (MPa)", "rhoMatrix (kg/m3)",
                "rhoPore (kg/m3)", "MLayer (kg)", "VLayer (m3)", "Htidal (W/m3)", "eta (Pa s)"
            ]

            for profile_file in files_by_type["Profile"]:
                file_path = os.path.join(planet_folder, profile_file)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                header_info = "".join(lines[:81]).strip()
                data_str = "".join(lines[83:])
                df_profile = pd.read_csv(StringIO(data_str), sep=r'\s+', header=None, na_values=['nan'])

                st.subheader(f"Profile File: {profile_file}")
                with st.expander("Show Extended Profile Header (Lines 1–81)"):
                    st.code(header_info)

                if df_profile.shape[1] == len(profile_column_names):
                    df_profile.columns = profile_column_names
                else:
                    st.warning(
                        f"⚠️ Column mismatch: Expected {len(profile_column_names)} headers vs {df_profile.shape[1]} data columns"
                    )
                    df_profile.columns = [f"Col_{i+1}" for i in range(df_profile.shape[1])]

                st.dataframe(df_profile, use_container_width=True)
                st.subheader("Plot Profile Data")

                chart_placeholder = st.empty()

                persist_plot = st.checkbox(
                    "Plot multiple Y‑axes against same X‑axis", key=f"persist_profile_{profile_file}"
                )

                x_axis = st.selectbox("X-axis", df_profile.columns, key=f"x_profile_{profile_file}")

                available_y_columns = [col for col in df_profile.columns if col != x_axis]

                if persist_plot:
                    y_axes = st.multiselect(
                        "Y-axis (select one or more)",
                        options=available_y_columns,
                        default=available_y_columns[:1],
                        key=f"multi_y_profile_{profile_file}"
                    )
                else:
                    y_axes = [st.selectbox(
                        "Y-axis",
                        options=available_y_columns,
                        key=f"single_y_profile_{profile_file}"
                    )]

                if y_axes:
                    try:
                        df_profile[x_axis] = pd.to_numeric(df_profile[x_axis], errors='coerce')
                        for col in y_axes:
                            df_profile[col] = pd.to_numeric(df_profile[col], errors='coerce')

                        chart_data = df_profile[[x_axis] + y_axes].dropna()
                        chart_data = chart_data.set_index(x_axis)[y_axes]

                        if not chart_data.empty:
                            chart_placeholder.scatter_chart(chart_data)
                        else:
                            chart_placeholder.empty()
                            st.info("No valid data to plot after cleaning.")
                    except Exception as e:
                        chart_placeholder.empty()
                        st.warning(f"⚠️ Unable to plot: {e}")
                else:
                    chart_placeholder.empty()
                    st.info("Please select a Y-axis different from the X-axis to plot.")
