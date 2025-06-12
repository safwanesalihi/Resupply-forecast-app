
import pandas as pd
from prophet import Prophet
import json
import os

def run_prophet_forecast(input_csv_path, output_json_path):
    """
    Reads cleaned data, filters for 'Actual sales', trains a Prophet model,
    forecasts 12 future months, and saves the forecast to a JSON file.
    """
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"Error: Cleaned data CSV not found at {input_csv_path}")
        return
    except Exception as e:
        print(f"Error reading cleaned data CSV: {e}")
        return

    # Filter for 'Actual sales'
    df_actual_sales = df[df["type"] == "Actual sales"].copy()

    # Prepare DataFrame for Prophet
    df_actual_sales["ds"] = pd.to_datetime(df_actual_sales["date"])
    df_actual_sales["y"] = df_actual_sales["value"]

    # Train Prophet model
    model = Prophet()
    model.fit(df_actual_sales)

    # Create future DataFrame for 12 months
    future = model.make_future_dataframe(periods=12, freq='M')

    # Forecast
    forecast = model.predict(future)

    # Extract relevant columns and convert to JSON
    forecast_output = forecast[["ds", "yhat"]].copy()
    forecast_output["ds"] = forecast_output["ds"].dt.strftime("%Y-%m-%d")

    try:
        with open(output_json_path, "w") as f:
            json.dump(forecast_output.to_dict(orient="records"), f, indent=4)
        print(f"Forecast saved to {output_json_path}")
    except Exception as e:
        print(f"Error saving forecast to JSON: {e}")

if __name__ == "__main__":
    input_csv = "data/cleaned_data.csv"
    output_json = "data/forecast.json"
    run_prophet_forecast(input_csv, output_json)


