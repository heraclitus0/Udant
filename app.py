import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from logic import SupplyGapAnalyzer
from io import BytesIO

# ---------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="Udant Supply Chain Utility",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🌾 Udant Supply Chain Utility")
st.markdown("""
**Purpose:** Detect and quantify supply-demand mismatches in contract farming.

This tool supports field pilots, farmer-buyer alignment, and stakeholder evaluations using real or simulated data.
""")

st.markdown("---")

# ---------------------------------------------------
# INPUT FORM
# ---------------------------------------------------
st.subheader("📥 Step 1: Enter Contract Data")

with st.form("contract_form"):
    crop_names = st.text_input("Crop Names (comma-separated)", "Tomato, Wheat, Rice")
    forecast = st.text_input("Forecast Quantities (kg)", "100, 200, 150")
    actual = st.text_input("Actual Yield (kg)", "90, 180, 160")
    submitted = st.form_submit_button("🔍 Analyze Supply Gap")

# ---------------------------------------------------
# ANALYSIS LOGIC
# ---------------------------------------------------
if submitted:
    try:
        analyzer = SupplyGapAnalyzer(crop_names, forecast, actual)
        df = analyzer.compute_gap()
        summary = analyzer.get_summary()

        st.success("✅ Analysis Completed")

        st.subheader("📋 Contract-Wise Supply Gap")
        st.dataframe(df.style.format({
            "Forecast (kg)": "{:.1f}",
            "Actual (kg)": "{:.1f}",
            "Gap (kg)": "{:.1f}",
            "Gap (%)": "{:.2f}"
        }))

        # ---------------------------------------------------
        # STAKEHOLDER-SAFE SUMMARY
        # ---------------------------------------------------
        st.subheader("📊 Summary Metrics")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Forecast (kg)", summary["Total Forecasted (kg)"])
            st.metric("Total Actual (kg)", summary["Total Actual (kg)"])
        with col2:
            st.metric("Net Supply Gap (kg)", summary["Net Supply Gap (kg)"])
            st.metric("Average Gap (%)", f"{summary['Average Gap (%)']}%")

        st.markdown("---")

        # ---------------------------------------------------
        # CHARTS
        # ---------------------------------------------------
        st.subheader("📈 Forecast vs Actual Visuals")

        fig1, ax1 = plt.subplots()
        df.plot(kind='bar', x='Crop', y=['Forecast (kg)', 'Actual (kg)'], ax=ax1,
                color=['#4caf50', '#2196f3'])
        ax1.set_ylabel("Quantity (kg)")
        ax1.set_title("Forecast vs Actual Yield")
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots()
        sns.lineplot(data=df, x='Crop', y='Gap (%)', marker='o', ax=ax2, color="#f44336")
        ax2.axhline(0, linestyle='--', color='gray')
        ax2.set_ylabel("Gap (%)")
        ax2.set_title("Gap Percentage by Crop")
        st.pyplot(fig2)

        # ---------------------------------------------------
        # REPORT EXPORT
        # ---------------------------------------------------
        def to_excel(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, sheet_name='Udant_Gap_Report', index=False)
            return output.getvalue()

        excel_data = to_excel(df)

        st.download_button(
            label="📥 Download Excel Report",
            data=excel_data,
            file_name="Udant_Supply_Gap_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("---")

        st.caption("Report generated using Udant's symbolic contract utility system. For institutional pilots, contact your local coordination team.")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
