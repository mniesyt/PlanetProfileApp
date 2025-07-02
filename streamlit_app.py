import streamlit as st

#from streamlit_option_menu import option_menu

st.title("Planet Profile")
st.write("Let's Start by Setting Up Your Planet")

st.subheader("Use Predefined Body?")

st.selectbox("Choose your Planetary Body below",
             ("Europa", "Ganymede", "Titan"))

# will eventually have to have an actual call to the list of available moons from planet profile directly
st.subheader("Temperature Setup")
st.number_input("Select Your Bottom Temperature (in  $^\circ K$)")
# User Passes in a Temperature of the bottom of the ocean

st.subheader("Ocean Composition")
user_ocean_type = st.selectbox("Use Predefined Ocean or Define own Ocean Composition", ("Use pre-defined ocean composition","Define your own ocean composition"),index = None, placeholder = "Select Ocean Type")
#User selects which water they want to use, will have to call from prespecified options list
#print(user_ocean_type.index)

if user_ocean_type == "Use pre-defined ocean composition":
   st.write("Using Predefined Ocean")


if user_ocean_type == "Define your own ocean composition":
    st.write("Define Your Ocean Below")
# will have to add an option to select concentration units  
    num_salts = st.number_input("Input number of salt species", min_value = 1, max_value = 3)
    st.text_input("First Ocean Salt")
    st.number_input("First Salt Concentration")

    if num_salts >= 2: 
        st.text_input("Second Ocean Salt")
        st.number_input("Second Salt Concentration")

    if num_salts >= 3: 
        st.text_input("Third Ocean Salt")
        st.number_input("Third Salt Concentration")

#with st.popover("Open popover"):
   # st.markdown("Hello World 👋")
    #name = st.text_input("What's your name?")

