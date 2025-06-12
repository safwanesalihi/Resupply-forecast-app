import pandas as pd
import os

excel_path = "/home/ubuntu/Resupply-forecast-app/Arkeos_ - KM A3 MFPs - 2025-06-11.xlsx"

try:
    df = pd.read_excel(excel_path)
    print("File read successfully!")
    print(df.head())
except FileNotFoundError:
    print(f"Error: File not found at {excel_path}")
except Exception as e:
    print(f"An error occurred: {e}")


