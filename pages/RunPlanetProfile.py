import streamlit as st
import os
import sys
from pdf2image import convert_from_path
from PIL import Image
import re
import subprocess
from Utilities.planet_sidebar import show_planet_status
show_planet_status()
from copy import deepcopy
import pandas as pd
import re



# ----- Page setup stuff -----
st.set_page_config(page_icon="./PPlogo.ico")
st.set_page_config(page_title="Run PlanetProfile")
st.title("Run PlanetProfile")
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


# ----- Changed Settings Summary -----

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
    or any(st.session_state["changed_step_settings_flags"].values())
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



# ----- Summary of Changes Made and Updating of SemiCustomPlanet with new changes -----
if any_changes_made:
    # ----- Changed Bulk Settings Summary -----
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


    # ----- Changed Ocean Settings Summary -----
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

    # ----- Changed Layer Step Settings Summary -----
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

    # ----- Changed Core and Silicates Settings Summary -----
    st.markdown("## Custom Core and Silicate Settings Applied")
    # If the user has changed any core and silicate settings, they will be updated into the SemiCustomPlanet object here and printed for the user
    changed_core_settings = st.session_state.get("changed_core_settings", {})
    #st.write(changed_core_settings)
    if changed_core_settings:
        st.warning("You have changed the following settings from the defaults:")
        for key, was_changed in st.session_state["changed_core_settings_flags"].items():
            if was_changed:
                core_setting_name = key.split(".")[-1]
                core_new_val = st.session_state["changed_core_settings"][key]

                # All of this extra stuff is because Planet.Core deoesn't encompass everything - there is Planet.Sil and Planet.Do in the core settings attributes
                # Extract object path from key
                parts = key.split(".")  # ["Planet", "Core", "wFe_ppt"]

                # Start from Planet
                obj = Planet
                try:
                    # Walk through the object path dynamically
                    for part in parts[1:-1]:  # skip "Planet", stop before last part (attribute name)
                        obj = getattr(obj, part)

                        # Get the attribute value (or use "N/A" if missing)
                    core_default_val = getattr(obj, core_setting_name, "N/A")
                except AttributeError:
                    core_default_val = "N/A"

                st.markdown(f"- **{core_setting_name}**: `{core_default_val}` → `{core_new_val}`")
    else:
        st.info("No core or silicate settings have been changed. All values are defaults.")
    st.markdown("---")


# ----- Printing All Figures -----
config_path = os.path.join(parent_directory, "configPP.py") #path to configPP.py
#st.write(config_path)

# Import config
from configPP import configAssign  # This brings in the current config state from the configPP.py file
# Call the function to get Params and ExploreParams
Params, ExploreParams = configAssign() #configAssign creates the ParamsStruct and ExploreParamsStruct

exclude_plot = "SKIP_PLOTS"
exclude_calcs = {"CALC_ASYM", "CALC_NEW_ASYM"}

# Automatically set all Params attributes with 'PLOT' or 'CALC' in the name to True **Except CALC_ASYM --> if CALC_ASYM is false, then PLOT_ASYM, PLOT_MAG_SPECTRUM and PLOT_MAG_SPECTRUM_COMBO won't print out
for attr in dir(Params):

    if "PLOT" in attr and not attr.startswith("__"):
        if attr == exclude_plot:
            setattr(Params, attr, False)
        else:
            setattr(Params, attr, True)

    if "CALC" in attr and not attr.startswith("__"):
        setattr(Params, attr, attr not in exclude_calcs) #sets

# Optional: Show updated Params values in Streamlit for confirmation
#plot_attrs = {attr: getattr(Params, attr) for attr in dir(Params) if "PLOT" in attr and not attr.startswith("__")}
#calc_attrs = {attr: getattr(Params, attr) for attr in dir(Params) if "CALC" in attr and not attr.startswith("__")}
#st.write("Updated PLOT parameters in Params:", plot_attrs)
#st.write("Updated CALC parameters in Params:", calc_attrs)


# ----- Functions for reading PP terminal output LaTeX tabulars and configuring them into tables int he GUI ----

def strip_ansi_codes(s):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
    return ansi_escape.sub('', s)

def extract_section_titles(latex_str):
    return re.findall(r'\\section\*{([^}]*)}', latex_str)

def clean_latex_cell(cell):
    cell = cell.strip()

    # Keep math content (e.g. $C/MR^2$) by removing only the $ signs
    cell = re.sub(r'\$', '', cell)

    # Handle common LaTeX commands
    cell = re.sub(r'\\textbf{([^}]*)}', r'\1', cell)
    cell = re.sub(r'\\ce{([^}]*)}', r'\1', cell)
    cell = re.sub(r'\\num{([^}]*)}', r'\1', cell)
    cell = re.sub(r'\\si{([^}]*)}', r'(\1)', cell)

    # Handle substack as ±
    cell = re.sub(r'\\substack\{([^}]*)\}', lambda m: ' ± '.join(line.strip() for line in m.group(1).split(r'\\')), cell)

    # Replace \pm with ±
    cell = cell.replace(r'\pm', '±')

    # Remove ~ (non-breaking space in LaTeX)
    cell = cell.replace('~', ' ')

    # Clean out \mathrm and other formatting
    cell = re.sub(r'\\mathrm{([^}]*)}', r'\1', cell)
    cell = re.sub(r'\\overline{([^}]*)}', r'\1', cell)

    # Remove any remaining LaTeX commands
    cell = re.sub(r'\\[a-zA-Z]+', '', cell)
    cell = re.sub(r'[{}]', '', cell)

    return cell.strip()

def parse_all_latex_tables(latex_str):
    tables_raw = re.findall(r'\\begin{tabular}.*?\\hline(.*?)\\end{tabular}', latex_str, re.DOTALL)
    #st.write("Raw tabular blocks found:", tables_raw)  #for testing to see how the tables are getting parsed

    tables = []

    for block in tables_raw:
        block = block.replace('\n', ' ')
        rows = [line.strip() for line in block.strip().split('\\\\') if line.strip()]

        parsed_rows = []

        for row in rows:
            cells = [clean_latex_cell(cell) for cell in row.split('&')]
            parsed_rows.append(cells)

        # Remove short rows or empty ones
        valid_rows = [r for r in parsed_rows if len(r) == 2]

        if len(valid_rows) >= 2 and len(valid_rows) / len(parsed_rows) >= 0.8:
            df = pd.DataFrame(valid_rows, columns=["Property", "Value"])
            tables.append(df)
        elif len(parsed_rows) >= 2 and len(parsed_rows[0]) > 2:
            headers = parsed_rows[0]
            data_rows = parsed_rows[1:]
            try:
                df = pd.DataFrame(data_rows, columns=headers)
                tables.append(df)
            except Exception as e:
                st.warning(f"Failed to parse structured table: {e}")
        else:
            st.warning("Skipping unrecognized table format.")

    return tables

def remove_latex_tables(raw_text):
    # Remove everything between \begin{tabular} and \end{tabular}, including those lines
    return re.sub(r'\\begin{tabular}.*?\\end{tabular}', '', raw_text, flags=re.DOTALL).strip()

# ----- Run Planet Profile Button and Outputs -----

if st.button("Run PlanetProfile with my Choices", type = "primary"):
    with st.spinner("Pushing your settings to PlanetProfile..."):

        parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
        # Assuming user has cloned the PPApp into the same environment as PlanetProfile
        # have to move up one step out of PPApp into PP to run PP
        st.success(f"Running PlanetProfileCLI.py from: {parent_dir}")

        # Command to actually run PlanetProfile
        command = ["python", "PlanetProfileCLI.py", str(chosen_planet)]

        result = subprocess.run(command, cwd=parent_dir, capture_output=True, text=True)
        output_str = result.stdout + "\n" + result.stderr


        if result.returncode == 0:
            st.success("PlanetProfile ran successfully.")
            st.markdown("---")
        else:
            st.error("There was an error running PlanetProfile.")
            st.markdown("---")

     # Optionally strip ANSI
        output_str = strip_ansi_codes(output_str)

        # --- Parse LaTeX tables from output ---
        tables = parse_all_latex_tables(output_str)
        titles = extract_section_titles(output_str)
        if tables:
            st.markdown("### PlanetProfile Table Outputs")
            for i, df in enumerate(tables):
                title = titles[i] if i < len(titles) else f"Table {i+1}"
                st.subheader(title)
                st.dataframe(df)

    # Remove LaTeX tables from the terminal output box, they just show up as tables above the box
    clean_output = remove_latex_tables(output_str)

    # Escape HTML characters for safe rendering
    escaped_output = clean_output.replace('<', '&lt;').replace('>', '&gt;')

    # Display styled terminal output
    st.markdown("---")
    st.markdown("### Raw Terminal Output")
    st.markdown(
        f"""
        <div style="height: 400px; overflow-y: scroll; background-color: #111; color: #eee; padding: 10px; font-family: monospace; white-space: pre-wrap; border: 1px solid #666;">
            {escaped_output}
        </div>
        """,
        unsafe_allow_html=True,
    )





else:
    st.warning("Choices have not yet been pushed to PlanetProfile")

st.markdown("---")



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
