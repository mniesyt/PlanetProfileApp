import streamlit as st
import os
import sys
import re

st.set_page_config(page_title="Figure Settings")
st.title("Figure Settings")
st.write("Choose which figures you would like to produce below as well as settings for your chosen figures")

Planet = os.getenv("Planet") # e.g., "Europa"

# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/FigureSettings.py
FigureSettings_directory = os.path.dirname(os.path.abspath(__file__))
# Get the app directory (/PlanetProfile/PlanetProfileAPP)
app_directory = os.path.dirname(FigureSettings_directory)
# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)
# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)

config_path = os.path.join(parent_directory, "configPP.py") #path to configPP.py


# Import config
from configPP import configAssign  # This brings in the current config state from the configPP.py file
# Call the function to get Params and ExploreParams
Params, ExploreParams = configAssign() #configAssign creates the ParamsStruct and ExploreParamsStruct


st.subheader("General Figure Settings")
# Optional: Skip all plots
Params.SKIP_PLOTS = st.checkbox("Skip All Plots", value=getattr(Params, "SKIP_PLOTS", False)) #the getattr loads the checkbox to default to whatever is in the config file originally
#if the user cheks that they want to skip plots, then params.SKIP_PLOTS is set to true
Params.LEGEND = st.checkbox("Include Legends on Plots", value=getattr(Params, "LEGEND", True))
Params.TITLES = st.checkbox("Include Titles on Plots", value=getattr(Params, "TITLES", False))
st.markdown("---") 


st.subheader("Figure Selection")

# Automatically find all Params attributes that start with "PLOT_"
plot_attributes = [attr for attr in dir(Params)
                          if attr.startswith("PLOT_") and isinstance(getattr(Params, attr), bool)] #this grabs all Params.PLOT options that start with PLOT and are booleans so that we can make toggles with them


# Dictionary to store updated values
updated_params = {} #if users update a params object, it will get stored here to later be passed back into configPP

toggle_descriptions = {} #this grabs the comments from the configPP file for what each plot is
with open(config_path, "r") as f:
    lines = f.readlines()


with open(config_path, "r") as file:
    for line in file:
        match = re.match(r"\s*Params\.(PLOT_[A-Z_]+)\s*=\s*(True|False)\s*#\s*(.+)", line)
        if match:
            param_name = match.group(1)  # e.g., PLOT_GRAVITY
            comment = match.group(3).strip()  # e.g., Whether to plot Gravity...
            toggle_descriptions[param_name] = comment

            if comment.lower().startswith("whether to "):
                comment = comment[11:]  # Remove "Whether to " from the descriptions in configPP
            comment = comment.replace("plot", "Plot", 1)  # Capitalize the first "plot" only in the description
    


# Optional: You can provide nicer labels using a mapping or just auto-format them
for attr in plot_attributes:
    # Format label from the attribute name (e.g., PLOT_GRAVITY → Gravity)
    label = toggle_descriptions.get(attr, attr.replace("PLOT_", "").title())
    current_val = getattr(Params, attr) #loads in the current value form the configPP file
    new_val = st.toggle(label, value=current_val) #saves whatever the user sets as 
    updated_params[attr] = new_val


# Save back to configPP.py
if st.button("Save Plot Settings"): #if user clicks the button
    configPP_file_path = os.path.join(os.path.dirname(__file__), "../configPP.py") #this loads the path that configPP.py is in
    with open(configPP_file_path, "r") as f: #opens configPP
        lines = f.readlines() #reads in configPP

    # Replace values in file lines
    for i, line in enumerate(lines): #this loops through every line in the configPP file. i is the line index, line is the string of what is written on that line
        for key, val in updated_params.items(): #this loops through the updated_params dictionary and pulls out the key-value pairs that the user has updated
            if line.strip().startswith(f"Params.{key}"): #this checks if the line is one of the params.PLOT
                lines[i] = f"    Params.{key} = {val}\n" #if the line is one of the params.PLOT, the current_val gets overwritten with the new_val for that line

    # Write back to file
    with open(file_path, "w") as f: 
        f.writelines(lines) #whichever lines have been changed are written back to configPP

    st.success("Settings saved") #displays if configPP has successfully been updated