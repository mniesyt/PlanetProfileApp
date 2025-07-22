import streamlit
def show_planet_status():
    planet = streamlit.session_state.get("Planet", None)
    if planet:
        streamlit.sidebar.markdown(f"**Current Planet:** {planet}")
    else:
        streamlit.sidebar.markdown("⚠️ **Current Planet:** ❌ Not Set")