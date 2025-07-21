import streamlit as st
import os

# Main page content
st.set_page_config(page_title="Planet Profile Main", page_icon="🌙",)



st.title("Planet Profile")
st.write("Let's Start by Setting Up Your Planet")

st.subheader("Body Selection")

run_custom_body = st.checkbox("Create fully custom Planet?", value=False)

if run_custom_body:
    st.write("Create your fully custom planet. Set you bottom temperature and ocean compositions below, then set your Bulk Planetary Settings,Laer Step Settings, and Figure Settings on the other tabs")
    os.environ["Planet"] = "Custom"

if not run_custom_body:
    os.environ["Planet"] = st.selectbox("Choose your Planetary Body below", 
                                    ("Ariel", "Callisto", "Dione", "Enceladus", "Europa", "Ganymede", 
                                     "Iapetus", "Io", "Luna", "Mimas", "Miranda", "Oberon", "Pluto", 
                                     "Rhea", "Tethys", "Titan", "Titania", "Triton", "Umbriel"))
# will eventually have to have an actual call to the list of available moons from planet profile directly


#Planet = os.getenv("Planet") -> how to call the chosen planet in other parts of the code later

st.markdown("---")
st.subheader("Temperature Setup")
st.number_input("Select Your Bottom Temperature (in  $^\circ K$)")
# User Passes in a Temperature of the bottom of the ocean
st.write("The temperature you select at the bottom of the ocean layer for your planet is used by Planet Profile to ...")
st.markdown("---")

st.subheader("Ocean Composition")
user_ocean_type = st.selectbox("Use Predefined Ocean or Define own Ocean Composition", ("Use pre-defined ocean composition","Define your own ocean composition"),index = None, placeholder = "Select Ocean Type")
#User selects which water they want to use, will have to call from prespecified options list


if user_ocean_type == "Use pre-defined ocean composition":
   st.selectbox("Choose Predefined Ocean", ("Pure H2O", "Seawater", "MgSO4", "NaCl"))



if user_ocean_type == "Define your own ocean composition":
    st.write("Define Your Ocean Below")
# will have to add an option to select concentration units  
    species_concentration_unit = st.selectbox("Choose Salt Species Concentration Units", ("absolute mol/kg", "relative ratios"))
    num_salts = st.number_input("Input number of salt species", min_value = 1)
    num_salts_list = [int(digit) for digit in str(num_salts)]
    salt_name_list = []
    salt_conc_list = []
    st.markdown("---")
    for num in range(num_salts_list[0]):
        st.write("Salt Species", str(num+1))
        salt_name_list.append(st.text_input("Input name of Salt " + str(num+1)))
        salt_conc_list.append(st.text_input("Input Concentration of Salt " + str(num+1)))
        st.markdown("---")
    #st.write(salt_name_list)
    #st.write(salt_conc_list)
    #st.write(species_concentration_unit)
 

