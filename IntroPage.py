import streamlit as st

# Define the pages
about = st.Page("pages/About.py", title = "Welcome to Planet Profile", icon = "🌍")
main_settings = st.Page("pages/PlanetProfileMainSettings.py", title = "Planet Profile Main Settings", icon = "🌙" )
bulk_planetary_settings = st.Page("pages/BulkPlanetarySettings.py", title = "Bulk Planetary Settings", icon = "🪙")
ocean_settings = st.Page("pages/OceanSettings.py", title = "Ocean Settings", icon = "🌊" )
layer_step_settings = st.Page("pages/LayerStepSettings.py", title = "Layer Step Settings", icon = "📶")
figure_settings = st.Page("pages/FigureSettings.py", title = "Figure Settings", icon = "📈")
run_PlanetProfile = st.Page("pages/RunPlanetProfile.py", title = "Run Planet Profile", icon = "🚀")
# Set up navigation
pg = st.navigation([about, main_settings, bulk_planetary_settings, ocean_settings, layer_step_settings, figure_settings, run_PlanetProfile])

# Run the selected page
pg.run()
