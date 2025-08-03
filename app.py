import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from logic import SupplyGapAnalyzer
from io import BytesIO

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="Udant Supply Chain Utility",
    layout="centered",
    page_icon="🌾"
)

st.title("🌾 Udant Supply Chain Utility")
st.markdown("A cognitive tool to analyze yield forecast drift and contract risk in agri supply chains.")

# ----------------------------------------
# User Inputs
# ----------------------------------------
st.subheader("📥 Enter Crop Forecast and Actual Supply Data")

with st.form("crop_form"):
    crops = st.text_input("Crop names (comma-separated)", "Tomato, Wheat, Rice")
    forecast = st.text_input("Forecast values (kg)", "100, 200, 150")
    actual = st.text_input("Actual values (kg)", "90, 180, 160")
    submit = st.form_submit_button("🔍 Analyze Supply Gap")

# ----------------------------------------
# Analysis Section
# ----------------------------------------
if submit:
    try:
        # Analyzer object
        analyzer = SupplyGapAnalyzer(crops, forecast, actual)
        df = analyzer.compute_gap()
        summary = analyzer.get_summary()

        # Display results
        st.success("✅ Analysis Complete")
        st.subheader("📊 Forecast vs Actual Table")
        st.dataframe(df.style.format({
            "Forecast (kg)": "{:.2f}",
            "Actual (kg)": "{:.2f}",
            "Gap (kg)": "{:.2f}",
            "Gap (%)": "{:.2f}"
        }), height=300)

        # Summary Metrics
        st.subheader("📌 Summary Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Forecast (kg)", summary["Total Forecasted (kg)"])
            st.metric("Total Actual (kg)", summary["Total Actual (kg)"])
        with col2:
            st.metric("Net Gap (kg)", summary["Net Supply Gap (kg)"])
            st.metric("Average Gap (%)", f"{summary['Average Gap (%)']}%")

        # ----------------------------------------
        # Visualizations
        # ----------------------------------------
        st.subheader("📈 Visual Insights")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("**Bar Chart – Forecast vs Actual**")
            fig1, ax1 = plt.subplots()
            df.plot(kind='bar', x='Crop', y=['Forecast (kg)', 'Actual (kg)'], ax=ax1, color=['#90e0ef', '#0077b6'])
            ax1.set_ylabel("Quantity (kg)")
            ax1.set_title("Forecast vs Actual")
            st.pyplot(fig1)

        with chart_col2:
            st.markdown("**Line Chart – Gap (%)**")
            fig2, ax2 = plt.subplots()
            sns.lineplot(data=df, x='Crop', y='Gap (%)', marker="o", ax=ax2, color="#ef233c")
            ax2.set_ylabel("Gap (%)")
            ax2.set_title("Supply Drift %")
            st.pyplot(fig2)

        # ----------------------------------------
        # Export Section
        # ----------------------------------------
        st.subheader("📥 Export Analysis Report")

        def to_excel(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Gap Report')
            return output.getvalue()

        excel_data = to_excel(df)

        st.download_button(
            label="📄 Download as Excel",
            data=excel_data,
            file_name="udant_supply_gap_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"🚫 Error during processing: {str(e)}")
