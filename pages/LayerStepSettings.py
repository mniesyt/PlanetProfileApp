import streamlit as st
st.set_page_config(page_title="Layer Step Settings")


st.title("Layer Step Settings")
st.write("OPTIONAL -- Choose your Layer Step Settings Below")

st.number_input("Desired number of Ice I Layer steps", step=1)
# to be passed to Planet.Steps.nIceI
st.write("Defines the number of steps for the Ice I layer. Number of steps for other layers will be calculated based on mass, radius, and moment of inertia inputs.")
st.markdown("---")

st.number_input("Step Size for Ocean Pressure $\Delta P$")
st.write("Increment of pressure in MPa between each layer in lower hydrosphere/ocean (sets profile resolution)")
#Planet.Ocean.deltaP = 1.0
st.markdown("---")

st.number_input("Step size for Temperature $\Delta T$ ($^\circ K$)")
st.write("Step size in $^\circ K$ for temperature values used in generating ocean EOS functions. If set, overrides calculations that otherwise use the specified precision in user-set temperature at the bottom $^\circ K$ to determine this.")
#Planet.Ocean.deltaT = 0.1
st.markdown("---")

st.number_input("Maximum Pressure of the Hydrosphere (MPa)")
st.write("Guessed maximum pressure of the hydrosphere in MPa. Must be greater than the actual pressure, but ideally not by much.")
#Planet.Ocean.PHydroMax_MPa = 350.0
st.markdown("---")