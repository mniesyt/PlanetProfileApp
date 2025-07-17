import streamlit as st

# Define the pages
main_settings = st.Page("pages/PlanetProfileMainPage.py", title="Planet Profile Main Settings", icon = "🌙" ) 
bulk_planetary_settings = st.Page("pages/BulkPlanetarySettings.py", title="Bulk Planetary Settings", icon="🪙")
layer_step_settings = st.Page("pages/LayerStepSettings.py", title="Layer Step Settings", icon="📶")
figure_settings = st.Page("pages/FigureSettings.py", title="Layer Step Settings", icon="📈")
run_PlanetProfile = st.Page("pages/RunPlanetProfile.py", title="Run Planet Profile", icon="🚀")
# Set up navigation
pg = st.navigation([main_settings, bulk_planetary_settings, layer_step_settings, figure_settings, run_PlanetProfile])

# Run the selected page
pg.run()