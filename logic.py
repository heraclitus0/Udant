import pandas as pd

def calculate_supply_gap(crops, forecast, actual):
    crop_list = [c.strip() for c in crops.split(",")]
    forecast_list = list(map(float, forecast.split(",")))
    actual_list = list(map(float, actual.split(",")))

    df = pd.DataFrame({
        "Crop": crop_list,
        "Forecast (kg)": forecast_list,
        "Actual (kg)": actual_list
    })
    df["Gap (kg)"] = df["Forecast (kg)"] - df["Actual (kg)"]
    df["Gap (%)"] = round((df["Gap (kg)"] / df["Forecast (kg)"]) * 100, 2)

    return df