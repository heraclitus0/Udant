import streamlit as st
import pandas as pd
from io import BytesIO
from logic import SupplyGapAnalyzer

# -----------------------------
# App Metadata
# -----------------------------
st.set_page_config(page_title="Udant Utility", layout="centered")
st.title("🌾 Udant Supply Chain Utility")

st.markdown("""
Analyze and visualize yield mismatches in contract farming.

This tool compares **forecasted** and **actual** crop yields to calculate drift, deviation, and supply status.
""")

# -----------------------------
# Input Section
# -----------------------------
st.subheader("📥 Enter Forecast and Actual Data")

with st.form("form"):
    crop_names = st.text_input("Crop Names (comma-separated)", "Tomato, Wheat, Rice")
    forecast = st.text_input("Forecast Quantities (kg)", "100, 200, 150")
    actual = st.text_input("Actual Harvested Quantities (kg)", "90, 180, 160")
    submitted = st.form_submit_button("Analyze")

# -----------------------------
# Analysis & Output
# -----------------------------
if submitted:
    try:
        analyzer = SupplyGapAnalyzer(crop_names, forecast, actual)
        df = analyzer.compute_gap()
        summary = analyzer.get_summary()

        st.success("✅ Analysis Completed")

        st.subheader("📊 Supply Gap Table")
        st.dataframe(df)

        st.subheader("📈 Forecast vs Actual Chart")
        chart_df = df.set_index("Crop")[["Forecast (kg)", "Actual (kg)"]]
        st.bar_chart(chart_df)

        st.subheader("📉 Gap Percentage Line Chart")
        st.line_chart(df.set_index("Crop")[["Gap (%)"]])

        st.subheader("🧾 Summary")
        st.write(f"**Total Forecasted:** {summary['Total Forecasted (kg)']} kg")
        st.write(f"**Total Actual:** {summary['Total Actual (kg)']} kg")
        st.write(f"**Net Gap:** {summary['Net Supply Gap (kg)']} kg")
        st.write(f"**Avg Gap (%):** {summary['Average Gap (%)']}%")

        # -----------------------------
        # Download Section
        # -----------------------------
        def convert_df_to_excel(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Supply Gap')
            return output.getvalue()

        excel_data = convert_df_to_excel(df)

        st.download_button(
            label="📥 Download Excel Report",
            data=excel_data,
            file_name="udant_supply_gap.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
