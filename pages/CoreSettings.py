import streamlit as st
import os
import sys
import re
from Utilities.planet_sidebar import show_planet_status
show_planet_status()

st.set_page_config(page_title="Core and Silicate Settings")
st.title("Core and Silicate Settings")
st.set_page_config(page_icon="./PPlogo.ico")
st.write("Configure the makeup of your planet's core and mantle here")
st.markdown("---")

# Get the planet name from the session state
Planet = st.session_state.get("Planet", None)
if not Planet:
    st.error("Please Select a Planet on the Planet Profile Main Settings Page")
    st.stop()

#Initializing if the planet has an iron core into the session state
if "Do.Fe_CORE" not in st.session_state:
    st.session_state["Do.Fe_CORE"] = Planet.Do.Fe_CORE

if "changed_core_settings" not in st.session_state:
    st.session_state["changed_core_settings"] = {}

def track_core_change(key, new_value, default_value):
    if new_value != default_value:
        st.session_state["changed_core_settings"][key] = new_value


# ----- Do Fe_Core toggle -----
st.subheader("Include an Iron Core?")
st.write("If you choose not to include an iron core, your planet's core will be populated entirely by sa ilicate mantle instead.")
default_do_core_flag = Planet.Do.Fe_CORE
user_do_core_flag = st.toggle("Does your planet have a core?", value = default_do_core_flag)
track_core_change("Do.Fe_CORE", user_do_core_flag, default_do_core_flag)
st.markdown("---")

# ----- User selects core EOS or sets densities for the core and silicate materials -----
# Get absolute path to the EOS directory relative to this file
eos_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "PlanetProfile", "Thermodynamics", "EOStables", "Perple_X")
)

# Get list of mantle EOS files
eos_files = [f for f in os.listdir(eos_folder) if f.endswith(".tab")]

st.markdown("### Use Equations of State or Densities")
st.write("You can either specify the equation of state (EOS) for your core and silicates from a list of available core EOS's or input the densities of your core and silicate species.")
# Toggle between using EOS or manual densities
default_core_eos = Planet.Core.coreEOS or ""
use_eos = st.selectbox(
        "How do you want to define your core and silicate composition?",
        options=["Use Equation of State file", "Manually enter densities"],
        index=0 if Planet.Core.coreEOS else 1,
    )
st.markdown("---")


# ----- Core settings begin here -----

if user_do_core_flag:

    if use_eos == "Use Equation of State file":
        # Single core EOS
        core_eos_file = "Fe-S_3D_EOS.mat"
        core_eos_path = os.path.join(eos_folder, core_eos_file)
        st.info("Using Fe-S_3D_EOS.mat EOS for the core...")  #currently, we only have the one model for iron core stuff so it will efault to using this
        #track_core_change("Planet.Core.coreEOS", core_eos_file, default_core_eos)  if eventually we have mulitple core models this would keep track of user changes

    else:
        track_core_change("Planet.Core.coreEOS", "", default_core_eos)  # Clear EOS setting

        st.markdown("#### Manually Enter Core Densities")
        for var, label, default in [
            ("Planet.Core.rhoFe_kgm3", "Density of Iron (Fe), (kg/m³)", Planet.Core.rhoFe_kgm3),
            ("Planet.Core.rhoFeS_kgm3", "Density of Iron Sulfide (FeS), (kg/m³)", Planet.Core.rhoFeS_kgm3)
            #("Planet.Core.rhoPoFeFCC", "Density of PoFeFCC (kg/m³)", Planet.Core.rhoPoFeFCC)  --> Marshall started implementing this, but so far it is never actually used for anything
        ]:
            val = st.number_input(label, value=default)
            track_core_change(var, val, default)
            #Planet.Do.CONSTANT_INNER_DENSITY = True ---> this needs to be set to true if using densities

    st.markdown("---")
    st.markdown("### Other Core Settings")

    for var, label, default in [
        ("Planet.Core.QScore", "Quality Factor Qs; describes how efficiently the core absorbs or dissipates energy", Planet.Core.QScore),
        ("Planet.Core.wFe_ppt", "Mass fraction of Iron in the core (ppt)", Planet.Core.wFe_ppt),
    ]:
        val = st.number_input(label, value=default)
        track_core_change(var, val, default)
    st.markdown("---")



    st.markdown("### Core Molar Fractions")
    for var, label, default in [
        ("Planet.Core.xFeSmeteoritic", "Molar Fraction of Iron Sulfide (FeS), meteoritic", Planet.Core.xFeSmeteoritic),
        ("Planet.Core.xFeS", "Molar Fraction of Iron Sulfide (FeS) in the core", Planet.Core.xFeS),
        ("Planet.Core.xFeCore", "Molar Fraction of Iron (Fe)in the core", Planet.Core.xFeCore),
        ("Planet.Core.xH2O", "Molar Fraction of Water in the core", Planet.Core.xH2O),
    ]:
        val = st.number_input(label, value=default)
        track_core_change(var, val, default)
    st.markdown("---")


#----- Silicate Settings begin here -----

st.markdown("### Silicate EOS and Densities")
st.write("This manages the equation of state for the planet mantle")
# Defaults from Planet object
default_silicate_eos = Planet.Sil.mantleEOS # Current silicate EOS default from Planet
default_silicate_density = Planet.Sil.rhoSilWithCore_kgm3

if use_eos == "Use Equation of State file":
    st.info("You selected to use equations of state. Choose your silicate EOS below.")

    current_eos = Planet.Sil.mantleEOS
    selected_silicate_eos = st.selectbox(
        "Select Silicate Mantle EOS File",
        eos_files,
        index = eos_files.index(default_silicate_eos)
        if default_silicate_eos in eos_files else 0
        )

    track_core_change("Planet.Sil.mantleEOS", selected_silicate_eos, default_silicate_eos)

else:
    st.info("You selected to manually enter densities. Enter your silicate density below.")

    silicate_density = st.number_input(
            "Silicate Density with Core (kg/m³)",
            value=default_silicate_density
        )

    track_core_change("Planet.Sil.rhoSilWithCore_kgm3", silicate_density, default_silicate_density)
    # Clear EOS if switching to manual density
    track_core_change("Planet.Sil.mantleEOS", "", default_silicate_eos)
st.markdown("---")


st.markdown("### Other Silicate Settings")

# Radiogenic heating
default_Qrad = Planet.Sil.Qrad_Wkg
Qrad = st.number_input("Average radiogenic heating rate for silicates in W/kg.", value=default_Qrad, format="%.2e")
track_core_change("Planet.Sil.Qrad_Wkg", Qrad, default_Qrad)

# Tidal heating  ---> Scott says this isn't actually being used yet, so we will ignore it for now
#default_Htidal = Planet.Sil.Htidal_Wm3
#Htidal = st.number_input("Tidal Heating (W/m³)", value=default_Htidal, format="%.1e")
#track_core_change("Planet.Sil.Htidal_Wm3", Htidal, default_Htidal)

# Rock porosity toggle
default_porous = Planet.Do.POROUS_ROCK
porous_flag = st.toggle("Enable Porous Rock - If the rock is porous and you have an ocean, water from the ocean will be able to flow into the porous areas", value=default_porous)
track_core_change("Planet.Do.POROUS_ROCK", porous_flag, default_porous)

if porous_flag:
    default_phiRockMax_frac = Planet.Sil.phiRockMax_frac
    default_Pclosure_MPa = Planet.Sil.Pclosure_MPa
    default_porosType = Planet.Sil.porosType
    poros_options = ['Han2014', 'Vitovtova2014', 'Chen2020'] #these are the current porosity models we have available. If we expect to have many more, we can add dynamic loading here.


    phiRockMax_frac = st.number_input("Porosity (void fraction) of the rocks in vacuum.", value = default_phiRockMax_frac)
    track_core_change("Planet.Sil.phiRockMax_frac", phiRockMax_frac, default_phiRockMax_frac)

    Pclosure_MPa = st.number_input("Pressure threshold in MPa beyond which pores in silicates shut completely and porosity drops to zero, for use in Han et al. (2014) model.")
    track_core_change("Planet.Sil.Pclosure_MPa", Pclosure_MPa, default_Pclosure_MPa)
    #st.selectbox requires using indexing for the default value that shows up in the selectbox, so this loop looks for the index of the default porosity model from the list and passes it to the selectbox
    try:
        default_index = poros_options.index(default_porosType)
    except ValueError:
        default_index = 0  # fallback to first option if not found

    porosType = st.selectbox(
    "Porosity model to apply for silicates.",
    options=poros_options,
    index=default_index)
    track_core_change("Planet.Sil.porosType", porosType, default_porosType)

#self.phiRockMax_frac = None # Porosity (void fraction) of the rocks in vacuum. This is the expected value for core-less bodies, and porosity is modeled for a range around here to find a matching MoI. For bodies with a core, this is a fixed value for rock porosity at P=0.
#self.Pclosure_MPa = 350 # Pressure threshold in MPa beyond which pores in silicates shut completely and porosity drops to zero, for use in Han et al. (2014) model. See Saito et al. (2016) for evidence of values up to ~750 MPa: https://doi.org/10.1016/j.tecto.2016.03.044
#self.porosType = 'Han2014'  # Porosity model to apply for silicates. Options are 'Han2014', 'Vitovtova2014', 'Chen2020'.
