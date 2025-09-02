import streamlit as st
import os
import sys
from pdf2image import convert_from_path
from PIL import Image
import re
import subprocess
from copy import deepcopy
import pandas as pd
import re
from pathlib import Path
from dataclasses import asdict, is_dataclass
import pprint
import shutil

# ----- Page setup stuff -----
from Utilities.planet_sidebar import show_planet_status
show_planet_status()
st.set_page_config(page_icon="./PPlogo.ico")
st.set_page_config(page_title="Run PlanetProfile")
st.title("Run PlanetProfile")
st.subheader("Summary of Your Planet and Changes you have made from Defaults:")

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



# ----- Setting Up SemiCustomPlanet object and Module Saving  -----

# This initializes the changed settings dictionaries in the event that the user did not visit that particular page
for key in ["changed_bulk_settings_flags", "custom_ocean_flag", "changed_step_settings_flags", "changed_core_settings"]:
    if key not in st.session_state:
        # For the boolean custom_ocean_flag, initialize as False; for the others, use empty dict
        st.session_state[key] = False if key == "custom_ocean_flag" else {}

# Clean name and build module name if user is doing a SemiCustom run
def sanitize_filename(name):
    return re.sub(r"[^\w\-]", "_", name)



# If the user has changed any inputs, we will create a semi-custom Planet object here to push their changes to
# Check if any setting has been changed
any_changes_made = (
    st.session_state["custom_ocean_flag"]
    or any(st.session_state["changed_bulk_settings_flags"].values())
    or any(st.session_state["changed_step_settings_flags"].values())
    or any(st.session_state["changed_core_settings"].values())
)



def sanitize_filename(name):
    """Sanitize the filename by replacing invalid characters with underscores."""
    return re.sub(r'\W|^(?=\d)', '_', name)


# Conditionally create SemiCustomPlanet if any settings have been changed and PPSemiCustomPlanet.py file for running
if any_changes_made:
    SemiCustomPlanet = deepcopy(Planet)

    # Default name suggestion
    default_name = "SemiCustom" + chosen_planet

    # User names their semi custom planet here
    custom_planet_name = st.text_input("Enter a name for your modified planet (Hint: name it something that will help you identify what settings you have changed): ", value=default_name)


    # Full target directory: /PlanetProfile/<planet_name>
    planet_folder = os.path.join(parent_directory, chosen_planet)
    os.makedirs(planet_folder, exist_ok=True)

    # Create module name
    sanitized_name = sanitize_filename(custom_planet_name)
    module_filename = f"PP{sanitized_name}.py"

    # Full output path
    output_path = os.path.join(planet_folder, module_filename)

    st.info("Creating PP" + custom_planet_name + ".py based on user settings at " + str(planet_folder) + " ...")

    # Load original module file (e.g., PPEnceladus.py)
    original_path = os.path.join(planet_folder, f"PP{chosen_planet}.py")
    with open(original_path, "r") as f:
        original_lines = f.readlines()
    st.success(f"Semi-custom module saved as: {module_filename}")



    st.markdown("---")
else:
    SemiCustomPlanet = Planet  # No changes, use original Planet module
    st.info("No settings were modified. Running with default Planet.")
    st.markdown("---")





# This is used to set attributes to the planet object when the settings aren't all the same subtype (step settings has both Planet.Steps and Planet.Ocean, core settings has Planet.Core and Planet.Sil)
def set_nested_attr(obj, attr_path, value):
    """
    Recursively sets a nested attribute given a dotted path.
    E.g. set_nested_attr(obj, "Steps.nIceI", 5) sets obj.Steps.nIceI = 5
    """
    parts = attr_path.split(".")
    for part in parts[:-1]:
        obj = getattr(obj, part)
    setattr(obj, parts[-1], value)

    # Debug print - used to test and check that the SemiCustomPlanet object has been updated with the changed settings
    #full_path = ".".join(parts)
    #st.write(f"Updated `SemiCustomPlanet.{full_path}` to `{value}`")
    #print(f"Updated SemiCustomPlanet.{full_path} = {value}")

# ----- Changed Settings Summary and Updating of SemiCustomPlanet with new changes -----
changed_settings_for_SemiCustom = {}
default_values_for_comments = {}  # For optional inline comment

if any_changes_made:

    # ----- Changed Bulk Settings Summary -----
    st.markdown("## Custom Bulk Settings Applied")
    # If the user has changed any bulk planetary settings, they will be updated into the SemiCustomPlanet object here
    for key, changed in st.session_state["changed_bulk_settings_flags"].items():
        if changed:
            attr = key.split(".")[-1]
            val = st.session_state["changed_bulk_settings"][key]
            setattr(SemiCustomPlanet.Bulk, attr, val)

            full_key = f"Planet.Bulk.{attr}"
            changed_settings_for_SemiCustom[full_key] = val
            default_values_for_comments[full_key] = getattr(Planet.Bulk, attr, "N/A")

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
    custom_ocean_type = st.session_state.get("custom_ocean_comp", None)
    custom_ocean_ppt = st.session_state.get("custom_ocean_concentration", None)

    default_ocean_type = getattr(Planet.Ocean, "comp", "N/A")
    default_ocean_ppt = getattr(Planet.Ocean, "wOcean_ppt", "N/A")

    if running_custom_ocean == True:
        st.warning("You are using an ocean different than the default ocean")

        if custom_ocean_type:
            st.markdown(f"- **Ocean Composition**: `{default_ocean_type}` → `{custom_ocean_type}`")
            SemiCustomPlanet.Ocean.comp = custom_ocean_type
            changed_settings_for_SemiCustom["Planet.Ocean.comp"] = custom_ocean_type
            default_values_for_comments["Planet.Ocean.comp"] = default_ocean_type
        else:
            SemiCustomPlanet.Ocean.comp = default_ocean_type  # reset

        if custom_ocean_ppt is not None:
            st.markdown(f"- **Ocean Salinity (ppt)**: `{default_ocean_ppt}` → `{custom_ocean_ppt}`")
            SemiCustomPlanet.Ocean.wOcean_ppt = custom_ocean_ppt
            changed_settings_for_SemiCustom["Planet.Ocean.wOcean_ppt"] = custom_ocean_ppt
            default_values_for_comments["Planet.Ocean.wOcean_ppt"] = default_ocean_ppt
        else:
            SemiCustomPlanet.Ocean.wOcean_ppt = default_ocean_ppt  # reset




    if running_custom_ocean == False:
        st.info("No ocean settings have been changed. Using default ocean.")
    st.markdown("---")

    # ----- Changed Layer Step Settings Summary -----
    st.markdown("## Custom Layer Step Settings Applied")
    # If the user has changed any layer step settings, they will be updated into the SemiCustomPlanet object here and printed for the user
    for key, new_val in st.session_state.get("changed_step_settings", {}).items():
        # Remove the "Planet." prefix to get the attribute path
        attr_path = key.replace("Planet.", "", 1)
        # Set the value in SemiCustomPlanet
        set_nested_attr(SemiCustomPlanet, attr_path, new_val)
        full_key = key  # e.g., Planet.Steps.nIceI
        changed_settings_for_SemiCustom[full_key] = new_val

        parts = attr_path.split(".")
        default_obj = Planet
        try:
            for part in parts[:-1]:
                default_obj = getattr(default_obj, part)
            default_values_for_comments[full_key] = getattr(default_obj, parts[-1], "N/A")
        except Exception:
            default_values_for_comments[full_key] = "N/A"

    changed_flags = st.session_state.get("changed_step_settings_flags", {})
    changed_settings = st.session_state.get("changed_step_settings", {})

    if any(changed_flags.values()):
        st.warning("You have changed the following settings from the defaults:")

        for key, changed in changed_flags.items():
            if changed:
                new_val = changed_settings.get(key, "N/A")
                default_val = st.session_state.get(key, "N/A")  # Default was stored here at init

                # Strip just the final part of the setting name
                setting_name = key.split(".")[-1]

                st.markdown(f"- `{setting_name}`: `{default_val}` → `{new_val}`")
    else:
        st.info("No step settings have been changed. All values are defaults.")


    st.markdown("---")

    # ----- Changed Core and Silicate Settings Summary -----
    st.markdown("## Custom Core and Silicate Settings Applied")

    changed_core_settings = st.session_state.get("changed_core_settings", {})

    if changed_core_settings:
        st.warning("You have changed the following settings from the defaults:")

        for key, was_changed in st.session_state["changed_core_settings_flags"].items():
            if was_changed:
                new_val = st.session_state["changed_core_settings"][key]
                full_key = key  # e.g., Planet.Core.wFe_ppt

                # Apply to runtime object
                attr_path = key.replace("Planet.", "", 1)
                set_nested_attr(SemiCustomPlanet, attr_path, new_val)

                # Store in changed settings
                changed_settings_for_SemiCustom[full_key] = new_val

                # Get default value for inline comment
                parts = attr_path.split(".")
                default_obj = Planet
                try:
                    for part in parts[:-1]:
                        default_obj = getattr(default_obj, part)
                    default_val = getattr(default_obj, parts[-1], "N/A")
                except Exception:
                    default_val = "N/A"

                default_values_for_comments[full_key] = default_val

                # For display
                setting_name = parts[-1]
                st.markdown(f"- **{setting_name}**: `{default_val}` → `{new_val}`")

    else:
        st.info("No core or silicate settings have been changed. All values are defaults.")
    st.markdown("---")

    #- ----- Actually updates and writes the PPSemiCustomPlanet.py file -----
    # --- Load and Modify Lines from Original File ---
    with open(original_path, "r") as f:
        original_lines = f.readlines()

    updated_lines = []
    for line in original_lines:
        updated = False
        for full_key, new_val in changed_settings_for_SemiCustom.items():
            pattern = rf"^\s*{re.escape(full_key)}\s*="

            if re.match(pattern, line):
                # Format new value
                if isinstance(new_val, str):
                    new_val_str = f'"{new_val}"'
                elif isinstance(new_val, bool):
                    new_val_str = str(new_val)
                else:
                    new_val_str = repr(new_val)

                default_val = default_values_for_comments.get(full_key, "N/A")
                line = f"{full_key} = {new_val_str}  # changed from default: {default_val}\n"
                updated = True
                break  # Move to next line
        updated_lines.append(line)

    # --- Write Updated File ---
    with open(output_path, "w") as f:
        f.writelines(updated_lines)

    st.success(f"Custom planet module updated with your custom settings: `{module_filename}`")
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


# ----- Functions for reading PP terminal output LaTeX tabulars and configuring them into tables in the GUI ----

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

# Determine which module to run
if any_changes_made:
    module_to_run = f"{sanitize_filename(custom_planet_name)}"
else:
    module_to_run = chosen_planet  # e.g., PPEuropa


if st.button("Run PlanetProfile with my Choices", type = "primary"):
    with st.spinner("Pushing your settings to PlanetProfile..."):

        parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
        # Assuming user has cloned the PPApp into the same environment as PlanetProfile
        # have to move up one step out of PPApp into PP to run PP
        st.success(f"Running PlanetProfileCLI.py from: {parent_dir}")

        # Command to actually run PlanetProfile
        if not any_changes_made:
            command = ["python", "PlanetProfileCLI.py", str(module_to_run)]
        else:
            full_path = f"{chosen_planet}/{module_filename}"
            command = ["python", "PlanetProfileCLI.py", full_path]

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
