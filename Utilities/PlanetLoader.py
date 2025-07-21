import os
import importlib.util
import streamlit as st

def load_planet_module(parent_dir, Planet):
    """
    Dynamically loads a module (e.g. PPEuropa.py) from PlanetProfile/PlanetProfile/Default/Planet based on planet_name.
    Stores the result in session_state so it only loads once per session.
    """
# This checks if the planet info has already been loaded/stored in the session state and will not reload if they have already been loaded
    if "planet_data" in st.session_state and st.session_state.get("planet_loaded") == Planet:
        return st.session_state.planet_data
    

    # Path to the module file -> this does what te commented out lines do below but in one step 
    planet_default_module_path = os.path.join(parent_dir, "PlanetProfile", "Default", Planet, f"PP{Planet}.py")   
    st.write(planet_default_module_path)
# making sure the Planet folder is in the path so can find PPPlanet
#planet_folder_string = '/PlanetProfile/Default/'+str(Planet) #string to /PlanetProfile/Default/Planet
#full_planet_folder_string = parent_directory + planet_folder_string
#default_folder = sys.path.append(os.path.join(full_planet_folder_string)) # this gets to the folder where the defaults for the planet is


    if not os.path.exists(planet_default_module_path):
        raise FileNotFoundError(f"Could not find module file at: {planet_default_module_path}")

    # Use importlib to load the module from file- spec and exec_module are commands in the importlib library
    module_name = f"PP{Planet}" #e.g. PPEuropa.py
    spec = importlib.util.spec_from_file_location(module_name, planet_default_module_path) #based on the module and module path (e.g. PPEuropa.py in PlanetProfile/PlanetProfile/Defaults/Europa, returns a ModuleSpec object that tells Python how ot load the module)
    planet_module = importlib.util.module_from_spec(spec) #this creates a module object from spec
    spec.loader.exec_module(planet_module) #Execute the module's code inside the module object

    # Store in session_state so other pages can use it
    st.session_state["Planet"] = Planet
    st.session_state["planet_data"] = planet_module
    st.session_state["planet_loaded"] = module_name

    return planet_module