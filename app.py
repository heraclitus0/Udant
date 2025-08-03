import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from logic import compute_supply_gap, summarize_data

st.set_page_config(page_title="Udant Supply Chain Utility", layout="wide")
st.title("📈 Udant Supply Chain Utility")
st.caption("Analyze and visualize yield mismatches in contract farming.")
st.markdown("This tool compares forecasted and actual crop yields to calculate drift, deviation, and supply status.")

# --- Input Section
st.subheader("📥 Enter Forecast and Actual Data")

crops = st.text_input("Crop Names (comma-separated)", "Tomato, Wheat, Rice")
forecast = st.text_input("Forecast Quantities (kg)", "100, 200, 150")
actual = st.text_input("Actual Harvest Quantities (kg)", "90, 180, 160")

if st.button("🔍 Analyze"):
    try:
        df = compute_supply_gap(crops, forecast, actual)
        summary = summarize_data(df)

        st.success("✅ Analysis Completed")

        # --- Data Table
        st.subheader("📊 Supply Gap Table")
        st.dataframe(df, use_container_width=True)

        # --- Bar Chart: Forecast vs Actual
        st.subheader("📉 Forecast vs Actual Chart")
        bar_chart = px.bar(df, x="Crop", y=["Forecast (kg)", "Actual (kg)"],
                           barmode="group", color_discrete_map={
                               "Forecast (kg)": "lightblue",
                               "Actual (kg)": "darkblue"
                           })
        st.plotly_chart(bar_chart, use_container_width=True)

        # --- Line Chart: Gap Percentage
        st.subheader("📈 Gap Percentage Line Chart")
        line_chart = px.line(df, x="Crop", y="Gap (%)", markers=True)
        st.plotly_chart(line_chart, use_container_width=True)

        # --- Summary Metrics
        st.subheader("📋 Summary")
        st.markdown(f"- **Total Forecasted**: {summary['Total Forecast']} kg")
        st.markdown(f"- **Total Actual**: {summary['Total Actual']} kg")
        st.markdown(f"- **Net Gap**: {summary['Net Gap']} kg")
        st.markdown(f"- **Average Gap %**: {summary['Average Gap %']}%")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
