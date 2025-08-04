import os
import importlib.util
import streamlit as st


def load_planet_module(parent_dir, planet_name):
    """
    Dynamically loads a module (e.g. PPEuropa.py) from PlanetProfile/PlanetProfile/Default/Planet based on planet_name.
    Stores the result in session_state so it only loads once per session.
    """
    #This checks if a planet has actualle been selected, and if not, it stops the code
    # Get the planet from session_state
    if planet_name in (None, "-- Select a Planet --"):
        st.warning("No planet selected.")
        st.stop()

# This checks if the planet info has already been loaded/stored in the session state and will not reload if they have already been loaded
    # Avoid reloading if the same planet is already loaded
    if (
        "planet_data" in st.session_state
        and st.session_state.get("planet_loaded") == planet_name
    ):
        return st.session_state["planet_data"]


    # Path to the module file
    planet_default_module_path = os.path.join(parent_dir, "PlanetProfile", "Default", planet_name, f"PP{planet_name}.py")


    if not os.path.exists(planet_default_module_path):
        st.error(f"Could not find file at: {module_path}")
        st.stop()

    # Use importlib to load the module from file- spec and exec_module are commands in the importlib library
    module_name = f"PP{planet_name}" #e.g. PPEuropa.py
    spec = importlib.util.spec_from_file_location(module_name, planet_default_module_path) #based on the module and module path (e.g. PPEuropa.py in PlanetProfile/PlanetProfile/Defaults/Europa, returns a ModuleSpec object that tells Python how ot load the module)
    planet_module = importlib.util.module_from_spec(spec) #this creates a module object from spec
    spec.loader.exec_module(planet_module) #Execute the module's code inside the module object

    # Store in session_state so other pages can use it
    #st.session_state["Planet"] = Planet
    st.session_state["planet_data"] = planet_module
    st.session_state["planet_loaded"] = module_name

    return planet_module
