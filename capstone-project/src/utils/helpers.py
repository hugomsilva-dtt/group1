import pandas as pd

# Utility functions for the capstone project
def sample_helper():
    return "This is a helper function."

def read_excel_with_ids(file_path):
    """
    Reads an Excel file and adds a unique sequential ID for each entry.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: DataFrame with an added 'ID' column.
    """
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Add a unique sequential ID column
    df['ID'] = range(1, len(df) + 1)

    return df
