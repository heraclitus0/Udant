import pandas as pd

class SupplyGapAnalyzer:
    """
    Analyze forecast vs. actual supply data for contract farming.
    Returns a structured dataframe with gap metrics and summary.
    """

    def __init__(self, crop_string: str, forecast_string: str, actual_string: str):
        self.crops = [c.strip().title() for c in crop_string.split(",")]
        self.forecast_values = self._parse_float_list(forecast_string)
        self.actual_values = self._parse_float_list(actual_string)
        self.df = None

    def _parse_float_list(self, raw_string: str):
        try:
            return [float(x.strip()) for x in raw_string.split(",")]
        except ValueError:
            raise ValueError("All forecast and actual values must be valid numbers.")

    def validate_input(self):
        if not (len(self.crops) == len(self.forecast_values) == len(self.actual_values)):
            raise ValueError("The number of crops, forecast values, and actual values must match.")
        if len(self.crops) == 0:
            raise ValueError("Input fields cannot be empty.")

    def compute_gap(self):
        self.validate_input()

        df = pd.DataFrame({
            "Crop": self.crops,
            "Forecast (kg)": self.forecast_values,
            "Actual (kg)": self.actual_values
        })

        df["Gap (kg)"] = df["Forecast (kg)"] - df["Actual (kg)"]
        df["Gap (%)"] = df.apply(lambda row: round((row["Gap (kg)"] / row["Forecast (kg)"]) * 100, 2)
                                 if row["Forecast (kg)"] != 0 else 0, axis=1)
        df["Status"] = df["Gap (kg)"].apply(self._classify_gap)

        self.df = df
        return df

    def _classify_gap(self, gap):
        """
        Returns a label for the type of supply deviation.
        """
        if gap > 20:
            return "🚨 Severe Shortfall"
        elif 5 < gap <= 20:
            return "⚠️ Moderate Shortfall"
        elif -5 <= gap <= 5:
            return "✅ Stable"
        elif -20 <= gap < -5:
            return "🟢 Moderate Surplus"
        else:
            return "🟩 Severe Surplus"

    def get_summary(self):
        """
        Returns summary statistics across all inputs.
        """
        if self.df is None:
            raise RuntimeError("Run compute_gap() before accessing summary.")

        total_forecast = round(sum(self.forecast_values), 2)
        total_actual = round(sum(self.actual_values), 2)
        net_gap = round(total_forecast - total_actual, 2)
        avg_gap_pct = round((net_gap / total_forecast) * 100, 2) if total_forecast != 0 else 0

        return {
            "Total Forecasted (kg)": total_forecast,
            "Total Actual (kg)": total_actual,
            "Net Supply Gap (kg)": net_gap,
            "Average Gap (%)": avg_gap_pct
        }
