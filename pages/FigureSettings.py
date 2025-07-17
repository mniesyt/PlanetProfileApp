import streamlit as st
import os
import sys


st.set_page_config(page_title="Figure Settings")
st.title("Figure Settings")
st.write("Choose which figures you would like to produce below as well as settings for your chosen figures")

Planet = os.getenv("Planet") # e.g., "Europa"

# Get the path to the current script's directory
# /PlanetProfile/PlanetProfileApp/BulkPlanetarySettings.py
FigureSettings_directory = os.path.dirname(os.path.abspath(__file__))
#st.write(BulkPlanertarySettings_directory)

# Get the app directory (/PlanetProfile/PlanetProfileAPP)
app_directory = os.path.dirname(FigureSettings_directory)
# Get the parent directory (/PlanetProfile)
parent_directory  = os.path.dirname(app_directory)
# Add the parent directory to Python's search path.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)

# Import config
from configPP import Params  # This brings in the current config state


# Optionally: Skip all plots
Params.SKIP_PLOTS = st.checkbox("❌ Skip All Plots", value=getattr(Params, "SKIP_PLOTS", False))
st.markdown("---")

# Automatically find all Params attributes that start with "PLOT_"
plot_attributes = sorted([attr for attr in dir(Params)
                          if attr.startswith("PLOT_") and isinstance(getattr(Params, attr), bool)])

# Optional: You can provide nicer labels using a mapping or just auto-format them
for attr in plot_attributes:
    # Format label from the attribute name (e.g., PLOT_GRAVITY → Gravity)
    label = attr.replace("PLOT_", "").replace("_", " ").title()
    new_value = st.toggle(label, value=getattr(Params, attr))
    setattr(Params, attr, new_value)

# Save/update trigger
if st.button("✅ Save Settings"):
    st.success("Plot settings updated.")
    st.rerun()