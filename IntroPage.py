import streamlit as st

# Define the pages
main_settings = st.Page("pages/PlanetProfileMainPage.py", title="Planet Profile Main Settings", icon = "🌙" ) 
bulk_planetary_settings = st.Page("pages/BulkPlanetarySettings.py", title="Bulk Planetary Settings", icon="🪙")
layer_step_settings = st.Page("pages/LayerStepSettings.py", title="Layer Step Settings", icon="📶")

# Set up navigation
pg = st.navigation([main_settings, bulk_planetary_settings, layer_step_settings])

# Run the selected page
pg.run()