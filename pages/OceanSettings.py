import streamlit as st
import os
import sys
import re
from Utilities.planet_sidebar import show_planet_status
show_planet_status()

st.set_page_config(page_title="Ocean Settings")
st.title("Ocean Settings")
st.set_page_config(page_icon="./PPlogo.ico")
st.write("Configure your ocean here. Use a pre-defined ocean or set your own salt species and concentrations. The default for each planet is a predefined ocean which will automatically populate below.")
st.markdown("---")

# Get the planet name from the session state
Planet = st.session_state.get("Planet", None)
if not Planet:
    st.error("Please Select a Planet on the Planet Profile Main Settings Page")
    st.stop()

# Check if the planet is set to have no ocean by default
planet_has_ocean = not getattr(Planet.Do, "NO_H2O", False) # Default to False if attribute doesn't exist

if "user_wants_ocean" not in st.session_state:
    st.session_state["user_wants_ocean"] = planet_has_ocean

# ----- Reset Button to return to Defaults -----
#initializing the reset_ocean_flag in the session state as False
if "reset_ocean_flag" not in st.session_state:
    st.session_state["reset_ocean_flag"] = False

# If reset has been triggered, reset all ocean-related session state
# This block is only executed when the user clicks the “Reset” button.
if st.session_state["reset_ocean_flag"]: #if flag is true (if user presses reset button)
    # Revert to default: no ocean or default ocean
    st.session_state["user_wants_ocean"] = planet_has_ocean
    st.session_state["custom_ocean_flag"] = False
    st.session_state["custom_ocean_comp"] = None
    st.session_state["reset_ocean_flag"] = False
    st.success("Ocean settings reset to planet defaults.")
    st.rerun()




# Step 2: User toggle for whether they want to generate an ocean
st.subheader("Include an Ocean for your Planet?")
st.write("Determine whether your planet has a liquid water ocean.")

# If the default No_H2O is true, then toggle defaults to False (unchecked)
# If the default is to have an ocean, then this is set to true and the rest of the ocean settings pop up
user_wants_ocean = st.toggle("Include an ocean?",  value = st.session_state["user_wants_ocean"])
st.session_state["user_wants_ocean"] = user_wants_ocean  # update session state with toggle value




# ----- If the User wants an ocean, they set all of the settings here -----
if user_wants_ocean:

    # Define or access the default ocean composition (set this wherever you define defaults)
    default_ocean = getattr(Planet.Ocean, "comp")

    # Initializing Ocean session state variables
    if "custom_ocean_flag" not in st.session_state: #custom ocean in this case is just to keep track if the user is using any ocean other than the default for their selected planet
        st.session_state["custom_ocean_flag"] = False
    if "custom_ocean_comp" not in st.session_state:
        st.session_state["custom_ocean_comp"] = None


    st.markdown("---")

    st.subheader("Ocean Composition")
    user_ocean_type = st.selectbox("Use Predefined Ocean or Define own Ocean Composition", ("Use pre-defined ocean composition","Define your own ocean composition"),index = 0, placeholder = "Select Ocean Type")
    #User selects which water they want to use, will have to call from prespecified options list

    # ----- Predefined ocean Options and Settings -----
    # Predefined options list
    predefined_ocean_options = ("Pure H2O", "Seawater", "MgSO4", "NaCl")

    if user_ocean_type == "Use pre-defined ocean composition":
        try:
            default_ocean_type_index = predefined_ocean_options.index(Planet.Ocean.comp) #selectbox needs an integer input for default values, so this searches the predefined ocean options and gets the index of the default ocean comp from PPPlanet.py
        except ValueError:
            default_ocean_type_index = 0  # Fallback to first option if not found

        selected_ocean = st.selectbox("Choose Predefined Ocean", predefined_ocean_options, index=default_ocean_type_index)
        #Planet.Ocean.comp = selected_ocean --> will do this on the run planet profile page

            # Set flag based on deviation from default
        if selected_ocean != default_ocean:
            st.session_state["custom_ocean_flag"] = True
            st.session_state["custom_ocean_comp"] = selected_ocean
        else:
            st.session_state["custom_ocean_flag"] = False


    # Maybe to add later- dynamic loading of reaktoro salt databases. For now, these are the main 3 we use
    reaktoro_supported_databases = ["frezchem", "frezchemNH3", "frezchemSiCH4"]

    # ----- Custom Ocean Options and Settings ----
    if user_ocean_type == "Define your own ocean composition":
        st.session_state["custom_ocean_flag"] = True  # User is customizing their own ocean
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

        st.markdown("### Salt Concentration Settings")
        species_concentration_unit = st.selectbox("Choose Salt Species Concentration Units", ("absolute mol/kg", "relative ratios"))


        num_salts = st.number_input("Input number of salt species", min_value = 1)
        if species_concentration_unit == "relative ratios":
            Planet.Ocean.wOcean_ppt = st.number_input("Please input your desired parts per thousand (ppt) for you salts")

        else:
            Planet.Ocean.wOcean_ppt = None


        num_salts_list = [int(digit) for digit in str(num_salts)]
        salt_species_list = [] #initializing blank lists to be populated by chosen salts and concentrations
        salt_conc_list = []
        st.markdown("---")

        #Depending on how many salt species the user wants, they get an option to set each sepcies and their concentrations
        for i in range(int(num_salts)):
            st.write(f"Salt Species {i + 1}")
            selected_species = st.selectbox(f"Select Salt Species {i + 1}", species, key=f"species_select_{i}")
            concentration = st.number_input(f"Input Concentration of Salt {i + 1}", key=f"conc_input_{i}")

            salt_species_list.append(selected_species)
            salt_conc_list.append(concentration)
            st.markdown("---")

        if salt_species_list and salt_conc_list:
            salt_string = ", ".join(f"{species}: {conc}" for species, conc in zip(salt_species_list, salt_conc_list)) # this is all to format the salts and concentrations properly for PP to use
            st.markdown("### Salt Configuration")
            st.write(f"Selected salt concentration unit: `{species_concentration_unit}`")
            solution_name = st.text_input("Please name you custom ocean solution here (ex. MgSO4)") #user gets to pick how they want to name their ocean composition - this will get passed

        st.session_state["custom_ocean_comp"] = "CustomSolution" + solution_name + " = " + salt_string
        #This needs to get passed to Planet.Ocean.comp
        st.write(st.session_state["custom_ocean_comp"])

        
st.markdown("---")
if st.button("🔄 Reset to default ocean (double click)"): #when user clicks reset button,
    st.session_state["reset_ocean_flag"] = True #"reset_ocean_flag" is set to true in the session_state,
    # which triggers the if st.session_state["reset_ocean_flag"] function above
