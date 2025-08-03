import streamlit as st
import pandas as pd
from logic import compute_supply_gap, summarize_data

# Streamlit Page Config
st.set_page_config(page_title="Udant Supply Chain Utility", layout="centered")

st.title("📦 Udant Supply Chain Utility")
st.caption("Analyze and visualize yield mismatches in contract farming.")
st.markdown("This tool compares forecasted and actual crop yields to calculate drift, deviation, and supply status.")

# Input Section
st.subheader("📥 Enter Forecast and Actual Data")
crops = st.text_input("Crop Names (comma-separated)", "Tomato, Wheat, Rice")
forecast = st.text_input("Forecast Quantities (kg)", "100, 200, 150")
actual = st.text_input("Actual Harvest Quantities (kg)", "90, 180, 160")

if st.button("🔍 Analyze"):
    try:
        df = compute_supply_gap(crops, forecast, actual)
        summary = summarize_data(df)

        st.success("✅ Analysis Completed")

        # Data Table
        st.subheader("📊 Supply Gap Table")
        st.dataframe(df, use_container_width=True)

        # Forecast vs Actual - Bar Chart
        st.subheader("📉 Forecast vs Actual (Bar Chart)")
        st.bar_chart(data=df.set_index("Crop")[["Forecast (kg)", "Actual (kg)"]])

        # Gap % - Line Chart
        st.subheader("📈 Gap Percentage Trend")
        st.line_chart(data=df.set_index("Crop")["Gap (%)"])

        # Summary
        st.subheader("📋 Summary Metrics")
        st.markdown(f"- **Total Forecasted**: {summary['Total Forecast']} kg")
        st.markdown(f"- **Total Actual**: {summary['Total Actual']} kg")
        st.markdown(f"- **Net Gap**: {summary['Net Gap']} kg")
        st.markdown(f"- **Average Gap %**: {summary['Average Gap %']}%")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
