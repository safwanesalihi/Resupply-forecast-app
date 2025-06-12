
import pandas as pd
import os

def load_and_clean_data(excel_path, output_csv_path):
    """
    Reads an Excel file, reshapes it, cleans NaN values, parses dates,
    and saves the cleaned data to a CSV file.
    """
    print(f"Current working directory: {os.getcwd()}")
    print(f"Attempting to read Excel file from: {excel_path}")
    if not os.path.exists(excel_path):
        print(f"Error: File does not exist at {excel_path}")
        return

    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # The first column is the product identifier, and the rest are dates
    # We need to melt the DataFrame using the first column as id_vars
    # and the date columns as value_vars
    id_column = df.columns[0]
    date_columns = df.columns[1:].tolist()

    df_long = df.melt(id_vars=[id_column], value_vars=date_columns, var_name="date", value_name="value")

    # Rename the id_column to 'type' as per the requirement
    df_long.rename(columns={id_column: 'type'}, inplace=True)

    # Clean NaN values (e.g., from empty cells in Excel)
    df_long.dropna(subset=["value"], inplace=True)

    # Parse "date" as datetime
    df_long["date"] = pd.to_datetime(df_long["date"], errors="coerce")

    # Handle any remaining NaT values after coercion
    df_long.dropna(subset=["date"], inplace=True)

    # Save to CSV
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        df_long.to_csv(output_csv_path, index=False)
        print(f"Cleaned data saved to {output_csv_path}")
    except Exception as e:
        print(f"Error saving cleaned data to CSV: {e}")

if __name__ == "__main__":
    excel_file = "/home/ubuntu/Resupply-forecast-app/arkeos_data.xlsx"
    output_csv = "/home/ubuntu/Resupply-forecast-app/data/cleaned_data.csv"
    load_and_clean_data(excel_file, output_csv)


