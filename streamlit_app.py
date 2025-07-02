import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Settings'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected

st.title("Planet Profile")
st.write("Let's Start by Setting Up Your Planet")
st.selectbox("Choose your Planetary Body below",
             ("Europa", "Ganymede", "Titan"))

# will eventually have to have an actual call to the list of available moons from planet profile directly

st.number_input("Select Your Bottom Temperature (in  $^\circ K$)")
# User Passes in a Temperature of the bottom of the ocean


st.selectbox("Choose your ocean composition",
             ("Gibbs SeaWater", "NiSO4"))
#User selects which water they want to use, will have to call from prespecified options list


