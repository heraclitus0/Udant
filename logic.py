import pandas as pd

class SupplyGapAnalyzer:
    def __init__(self, crop_string: str, forecast_string: str, actual_string: str):
        self.crops = [c.strip().title() for c in crop_string.split(",")]
        self.forecast_values = self._safe_parse_list(forecast_string)
        self.actual_values = self._safe_parse_list(actual_string)
        self.df = None

    def _safe_parse_list(self, input_str):
        try:
            return [float(x.strip()) for x in input_str.split(",")]
        except ValueError:
            raise ValueError("Forecast/Actual values must be comma-separated numbers.")

    def validate_input(self):
        if not (len(self.crops) == len(self.forecast_values) == len(self.actual_values)):
            raise ValueError("Mismatch in number of crops, forecast, and actual values.")
        if len(self.crops) == 0:
            raise ValueError("No input provided.")

    def compute_gap(self):
        self.validate_input()

        df = pd.DataFrame({
            "Crop": self.crops,
            "Forecast (kg)": self.forecast_values,
            "Actual (kg)": self.actual_values
        })

        df["Gap (kg)"] = df["Forecast (kg)"] - df["Actual (kg)"]
        df["Gap (%)"] = df.apply(
            lambda row: round((row["Gap (kg)"] / row["Forecast (kg)"]) * 100, 2)
            if row["Forecast (kg)"] else 0,
            axis=1
        )
        df["Status"] = df["Gap (kg)"].apply(self._classify_gap)
        self.df = df
        return df

    def _classify_gap(self, gap):
        if gap > 20:
            return "⚠️ Severe Shortfall"
        elif 5 < gap <= 20:
            return "Moderate Shortfall"
        elif -5 <= gap <= 5:
            return "Stable"
        elif -20 <= gap < -5:
            return "Moderate Surplus"
        else:
            return "📈 Severe Surplus"

    def get_summary(self):
        if self.df is None:
            raise RuntimeError("Run compute_gap() before get_summary().")

        total_forecast = sum(self.forecast_values)
        total_actual = sum(self.actual_values)
        net_gap = total_forecast - total_actual
        avg_gap_pct = round((net_gap / total_forecast) * 100, 2) if total_forecast else 0

        return {
            "Total Forecasted (kg)": total_forecast,
            "Total Actual (kg)": total_actual,
            "Net Supply Gap (kg)": net_gap,
            "Average Gap (%)": avg_gap_pct
        }
