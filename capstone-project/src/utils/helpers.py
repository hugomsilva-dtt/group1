import pandas as pd
import requests

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

def remove_empty_entries(df):
    """
    Removes any entry (row) from the DataFrame that has at least one empty cell.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with rows containing empty cells removed.
    """
    return df.dropna()

def convert_to_usd(amount, from_currency):
    """
    Converts a given amount from a specified currency to USD using a fixed exchange rate.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency code of the amount (e.g., 'EUR', 'GBP').

    Returns:
        float: The equivalent amount in USD.
    """
    # Fixed exchange rate: 1 EUR = 1.137300 USD
    exchange_rate = 1.137

    try:
        if from_currency == 'EUR':
            return amount * exchange_rate
        else:
            raise ValueError(f"Unsupported currency: {from_currency}")
    except Exception as e:
        print(f"Error during currency conversion: {e}")
        return None

def process_dataframe_with_currency_conversion(df):
    """
    Processes a DataFrame to convert the 'Loan_Amount' and 'Income' columns to USD.

    Args:
        df (pd.DataFrame): The input DataFrame with 'Loan_Amount' and 'Income' columns.

    Returns:
        pd.DataFrame: The processed DataFrame with converted values.
    """
    for index, row in df.iterrows():
        try:
            # Process 'Loan_Amount'
            loan_str = str(row['Loan_Amount'])
            if '$' in loan_str:
                # Handle USD values
                loan_amount = float(loan_str.replace('$', '').strip())
                df.at[index, 'Loan_Amount'] = round(loan_amount, 2)
            else:
                # Handle EUR values
                # Remove € symbol and any other non-numeric characters except dot
                loan_str = ''.join(c for c in loan_str if c.isdigit() or c == '.')
                # Convert to float and round to 2 decimal places
                loan_amount = round(float(loan_str), 2)
                df.at[index, 'Loan_Amount'] = round(convert_to_usd(loan_amount, 'EUR'), 2)

            # Process 'Income'
            income_str = str(row['Income'])
            # Remove € symbol and any other non-numeric characters except dot
            income_str = ''.join(c for c in income_str if c.isdigit() or c == '.')
            income = round(float(income_str), 2)
            df.at[index, 'Income'] = round(convert_to_usd(income, 'EUR'), 2)
            
        except Exception as e:
            print(f"Error processing row {index}: {e}")

    return df
