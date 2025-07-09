import streamlit as st
import os
import importlib
import sys

st.set_page_config(page_title="Bulk Planetary Settings")

st.title("Bulk Planetary Settings")
st.write("OPTIONAL -- Choose your Bulk Planetary Settings Below")

Planet = os.getenv("Planet")


# Get the path to the current script's directory
# For /PlanetProfile/PlanetProfileApp/your_script.py, this will be:
# /PlanetProfile/PlanetProfileApp
BulkPlanertarySettings_directory = os.path.dirname(os.path.abspath(__file__))
#st.write(BulkPlanertarySettings_directory)

# Get the parent directory (/PlanetProfile)
app_directory = os.path.dirname(BulkPlanertarySettings_directory)
#st.write(app_directory)
parent_directory  = os.path.dirname(app_directory)
st.write(parent_directory)
# Add the parent directory to Python's search path.
# Now Python can find any modules inside /PlanetProfile.
if parent_directory not in sys.path:
    sys.path.append(parent_directory)



os.chdir('..') #From the PlanetProfile/PlanetProfileApp, going to PlanetProfile
#st.write(parent_directory)
current_directory = os.getcwd()
st.write(current_directory)

#os.chdir(str(Planet)) #now in the individual folder of the planet
#st.write(os.getcwd())
#st.write(PP+str(Planet))

#PPPlanet = "PP"+str(Planet)


#from "PP"+str(Planet) import *

# Get the planet name from the environment variable
Planet = os.getenv("Planet") # e.g., "Venus"


# Construct the module name as a string
# e.g., if Planet is "Venus", this becomes "PPVenus"
module_to_import = f"PP{Planet}"


# Use importlib to import the module
st.write(sys.path)
planet_folder = sys.path.append(Planet)
st.write(planet_folder)

#planet_module = importlib.import_module(planet_folder.module_to_import)

#st.write(planet_module)

#os.environ["Planet.Bulk.R_m"] = str(st.number_input("Radius of the body (m)", value = planet_module.Planet.Bulk.R_m))
#to be passed to Planet.Bulk.R_m
os.environ["Planet.Bulk.M_kg"] = str(st.number_input("Mass of the body (kg)"))
# to be passed to Planet.Bulk.M_kg
os.environ["Planet.Bulk.Tsurf_K"] = str(st.number_input("Temperature at the surface ($^\circ K$)"))
#Planet.Bulk.Tsurf_K = 110
os.environ["Planet.Bulk.Psurf_MPa"] = str(st.number_input("Pressure at the surface (MPa)"))
#Planet.Bulk.Psurf_MPa = 0.0
os.environ["Planet.Bulk.Cmeasured"] = str(st.number_input("Normalized Axial Moment of Inertia $C$"))
#Planet.Bulk.Cmeasured = 0.346  # Value from Anderson et al. (1998): https://doi.org/10.1126/science.281.5385.2019
os.environ["Planet.Bulk.Cuncertainty "] = str(st.number_input("Uncertainty in $C$"))
#Planet.Bulk.Cuncertainty = 0.005
os.environ["Planet.Bulk.Tb_K"] = str(st.number_input("Temperature at the bottom ($^\circ K$)"))
#Planet.Bulk.Tb_K = 268.305  # 30 km ice with 1.0x Seawater