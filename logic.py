import pandas as pd

def compute_supply_gap(crops, forecast_str, actual_str):
    crop_list = [c.strip() for c in crops.split(",")]
    forecast_vals = list(map(float, forecast_str.split(",")))
    actual_vals = list(map(float, actual_str.split(",")))

    if not (len(crop_list) == len(forecast_vals) == len(actual_vals)):
        raise ValueError("Mismatch in number of crops, forecast, or actual values.")

    df = pd.DataFrame({
        "Crop": crop_list,
        "Forecast (kg)": forecast_vals,
        "Actual (kg)": actual_vals
    })

    df["Gap (kg)"] = df["Forecast (kg)"] - df["Actual (kg)"]
    df["Gap (%)"] = round((df["Gap (kg)"] / df["Forecast (kg)"]) * 100, 2)

    def status(row):
        if row["Gap (kg)"] == 0:
            return "Matched"
        elif row["Gap (kg)"] > 0:
            return "Undersupply"
        else:
            return "Oversupply"

    df["Status"] = df.apply(status, axis=1)
    return df

def summarize_data(df):
    total_forecast = df["Forecast (kg)"].sum()
    total_actual = df["Actual (kg)"].sum()
    net_gap = total_forecast - total_actual
    avg_gap_pct = round(df["Gap (%)"].mean(), 2)

    return {
        "Total Forecast": total_forecast,
        "Total Actual": total_actual,
        "Net Gap": net_gap,
        "Average Gap %": avg_gap_pct
    }
