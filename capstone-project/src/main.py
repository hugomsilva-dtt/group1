import os
import pandas as pd
from config.settings import load_env
from utils.helpers import read_excel_with_ids, remove_empty_entries, process_dataframe_with_currency_conversion, convert_to_usd

def test_read_excel_with_ids():
    """
    Test the read_excel_with_ids function by providing a sample Excel file path.
    """
    sample_file_path = "C:\\0_workspace\\uplift_prog\\genIA\\agents\\group1\\input\\Dataset1.xlsx"  # Replace with your actual file path
    if os.path.exists(sample_file_path):
        df = read_excel_with_ids(sample_file_path)
        print(df.head())
    else:
        print(f"File {sample_file_path} does not exist.")

def test_remove_empty_entries():
    """
    Test the remove_empty_entries function by providing a sample DataFrame.
    """
    sample_file_path = "C:\\0_workspace\\uplift_prog\\genIA\\agents\\group1\\input\\Dataset1.xlsx"  # Replace with your actual file path
    if os.path.exists(sample_file_path):
        df = read_excel_with_ids(sample_file_path)
        print("Original DataFrame:")
        print(df)

        # Remove rows with empty cells
        cleaned_df = remove_empty_entries(df)
        print("Cleaned DataFrame:")
        print(cleaned_df)
    else:
        print(f"File {sample_file_path} does not exist.")

def test_process_dataframe_with_currency_conversion():
    """
    Test the process_dataframe_with_currency_conversion function by providing a sample DataFrame.
    """
    sample_file_path = "C:\\0_workspace\\uplift_prog\\genIA\\agents\\group1\\input\\Dataset1.xlsx"  # Replace with your actual file path
    if os.path.exists(sample_file_path):
        df = read_excel_with_ids(sample_file_path)
        df = remove_empty_entries(df)
        print("Original DataFrame:")
        print(df)

        # Process the DataFrame for currency conversion
        processed_df = process_dataframe_with_currency_conversion(df)
        print("Processed DataFrame:")
        print(processed_df)
    else:
        print(f"File {sample_file_path} does not exist.")

# Call the test function in main
def main():
    load_env()
    print("Capstone Project Initialized")
    test_read_excel_with_ids()
    test_remove_empty_entries()
    test_process_dataframe_with_currency_conversion()
    print(convert_to_usd(96636.12,'EUR'))

if __name__ == "__main__":
    main()
