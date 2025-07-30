import streamlit as st
from logic import calculate_supply_gap

st.set_page_config(page_title="Udant Supply Chain Utility", layout="centered")
st.title("Udant Supply Chain Utility")
st.markdown("Analyze supply-demand gaps for contract farming.")

# Inputs
st.subheader("Enter Crop Forecast and Actual Supply")
crops = st.text_input("Enter crops (comma-separated)", "Tomato, Wheat, Rice")
forecast = st.text_input("Forecast (in kg)", "100, 200, 150")
actual = st.text_input("Actual (in kg)", "90, 180, 160")

if st.button("Analyze Supply Gap"):
    try:
        df = calculate_supply_gap(crops, forecast, actual)
        st.success("Analysis Complete.")
        st.dataframe(df)

        st.bar_chart(df.set_index("Crop")[["Forecast (kg)", "Actual (kg)"]])
        st.line_chart(df.set_index("Crop")["Gap (kg)"])

    except Exception as e:
        st.error(f"Error: {e}")
