import os
import pandas as pd
from config.settings import load_env
from utils.helpers import read_excel_with_ids

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

# Call the test function in main
def main():
    load_env()
    print("Capstone Project Initialized")
    test_read_excel_with_ids()

if __name__ == "__main__":
    main()
