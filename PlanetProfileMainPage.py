import streamlit as st

#from streamlit_option_menu import option_menu

# Main page content
st.markdown("# Planet Profile Main Settings")
st.sidebar.markdown("# Planet Profile Main Settings")


st.title("Planet Profile")
st.write("Let's Start by Setting Up Your Planet")

st.subheader("Use Predefined Body?")

st.selectbox("Choose your Planetary Body below",
             ("Europa", "Ganymede", "Titan"))
# will eventually have to have an actual call to the list of available moons from planet profile directly

st.markdown("---")
st.subheader("Temperature Setup")
st.number_input("Select Your Bottom Temperature (in  $^\circ K$)")
# User Passes in a Temperature of the bottom of the ocean
st.markdown("---")

st.subheader("Ocean Composition")
user_ocean_type = st.selectbox("Use Predefined Ocean or Define own Ocean Composition", ("Use pre-defined ocean composition","Define your own ocean composition"),index = None, placeholder = "Select Ocean Type")
#User selects which water they want to use, will have to call from prespecified options list
#print(user_ocean_type.index)

if user_ocean_type == "Use pre-defined ocean composition":
   st.selectbox("Choose Predefined Ocean", ("Pure H2O", "Seawater", "MgSO4", "NaCl"))



if user_ocean_type == "Define your own ocean composition":
    st.write("Define Your Ocean Below")
# will have to add an option to select concentration units  
    species_concentration_unit = st.selectbox("Choose Salt Species Concentration Units", ("absolute mol/kg", "relative ratios"))
    num_salts = st.number_input("Input number of salt species", min_value = 1)
    num_salts_list = [int(digit) for digit in str(num_salts)]
    #st.write(type(num_salts_list))
    #st.write(num_salts_list)
    salt_name_list = []
    salt_conc_list = []
    st.markdown("---")
    for num in range(num_salts_list[0]):
        st.write("Salt Species", str(num+1))
        salt_name_list.append(st.text_input("Input name of Salt " + str(num+1)))
        salt_conc_list.append(st.text_input("Input Concentration of Salt " + str(num+1)))
        st.markdown("---")
    st.write(salt_name_list)
    st.write(salt_conc_list)
    st.write(species_concentration_unit)
    #num_salts_list = list(len(str((num_salts))))
    #st.write(len(num_salts_list))
    
    #for num in num_salts_list:
        #st.write(num_salts_list)
        #salt_name_list.append(st.text_input("Salt Species"))
        #st.write(salt_name_list)
        #num += 1


    #salt_name_list.append(st.text_input("First Ocean Salt"))
    #st.number_input("First Salt Concentration")
    #st.write(salt_name_list)
    #if num_salts >= 2: 
        #st.text_input("Second Ocean Salt")
        #st.number_input("Second Salt Concentration (ppt)")

    #if num_salts >= 3: 
        #st.text_input("Third Ocean Salt")
        #st.number_input("Third Salt Concentration (ppt)")

#with st.popover("Open popover"):
   # st.markdown("Hello World 👋")
    #name = st.text_input("What's your name?")

