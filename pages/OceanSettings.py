import streamlit as st
import os
import sys
import re
from Utilities.planet_sidebar import show_planet_status
show_planet_status()

st.set_page_config(page_title="Ocean Settings")
st.title("Ocean Settings")
st.set_page_config(page_icon="./PPlogo.ico")
st.write("Configure your ocean here. Use a pre-defined ocean or set your own salt species and concentrations.")

# Get the planet name from the session state
Planet = st.session_state.get("Planet", None)
if not Planet:
    st.error("Please Select a Planet on the Planet Profile Main Settings Page")
    st.stop()

st.markdown("---")

st.subheader("Ocean Composition")
user_ocean_type = st.selectbox("Use Predefined Ocean or Define own Ocean Composition", ("Use pre-defined ocean composition","Define your own ocean composition"),index = None, placeholder = "Select Ocean Type")
#User selects which water they want to use, will have to call from prespecified options list

if user_ocean_type == "Use pre-defined ocean composition":
   Planet.Ocean.comp = st.selectbox("Choose Predefined Ocean", ("Pure H2O", "Seawater", "MgSO4", "NaCl"))


# Maybe to add later- dynamic loading of reaktoro salt databases
reaktoro_supported_databases = ["frezchem", "frezchemNH3", "frezchemSiCH4"]


if user_ocean_type == "Define your own ocean composition":
    #st.write("Define Your Ocean Below")

    st.write("Planet Profile uses reaktoro databases to define aqueous salt species. Please select a reaktoro database to pull salts from. Frezchem is the default. frezchemNH3 supports ammonia species. frezchemSiCH4 supports methane species")


    from Utilities.SaltLoader import read_salt_db
    # Lets user pick whcih reaktoro database they want to run salts from
    selected_salt = st.selectbox("Choose a salt database:", reaktoro_supported_databases, index =0) #defaults to frezchem database

    # When selected, load the database
    if selected_salt:
        st.write(f"Loading species from `{selected_salt}.dat`...")
        try:
            species = read_salt_db(selected_salt + ".dat")
            st.success(f"Loaded {len(species)} aqueous species.")
        except Exception as e:
            st.error(f"Failed to load database: {e}")
        st.markdown("---")


# to add - the concentration units actually get passed to the planet object
    st.markdown("### Salt Concentration Settings")
    species_concentration_unit = st.selectbox("Choose Salt Species Concentration Units", ("absolute mol/kg", "relative ratios"))


    num_salts = st.number_input("Input number of salt species", min_value = 1)
    if species_concentration_unit == "relative ratios":
        Planet.Ocean.wOcean_ppt = st.number_input("Please input your desired parts per thousand (ppt) for you salts")

    else:
        Planet.Ocean.wOcean_ppt = None





    num_salts_list = [int(digit) for digit in str(num_salts)]
    salt_species_list = []
    salt_conc_list = []
    st.markdown("---")
    for i in range(int(num_salts)):
        st.write(f"Salt Species {i + 1}")
        selected_species = st.selectbox(f"Select Salt Species {i + 1}", species, key=f"species_select_{i}")
        concentration = st.number_input(f"Input Concentration of Salt {i + 1}", key=f"conc_input_{i}")

        salt_species_list.append(selected_species)
        salt_conc_list.append(concentration)
        st.markdown("---")

# Step 8: Create and display the summary string
    if salt_species_list and salt_conc_list:
        salt_string = ", ".join(
            f"{species}: {conc}" for species, conc in zip(salt_species_list, salt_conc_list)
    )
        st.markdown("### Salt Configuration")
        st.write(f"Selected salt concentration unit: `{species_concentration_unit}`")
    #st.write(salt_string)

        solution_name = st.text_input("Please name you custom ocean solution here (ex. MgSO4)")

    #st.write(solution_name)

    Planet.Ocean.comp = "CustomSolution" + solution_name + " = " + salt_string
    st.write(Planet.Ocean.comp)
