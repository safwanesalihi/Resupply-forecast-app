
import pandas as pd

excel_path = "/home/ubuntu/Resupply-forecast-app/arkeos_data.xlsx"

try:
    df = pd.read_excel(excel_path)
    print("Columns in the Excel file:")
    print(df.columns.tolist())
except FileNotFoundError:
    print(f"Error: File not found at {excel_path}")
except Exception as e:
    print(f"An error occurred: {e}")


