import streamlit as st

# Define the pages
main_page = st.Page("PlanetProfileMainPage.py", title="Main Page", icon=":crescent_moon:")
#page_2 = st.Page("BulkPlanetarySettings.py", title="Bulk Planetary Settings", icon="🪙")
#page_3 = st.Page("LayerStepSettings.py", title="Layer Step Settings", icon="📶")

# Set up navigation
pg = st.navigation([main_page])#, page_2, page_3])

# Run the selected page
pg.run()