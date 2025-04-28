import pandas as pd
from datetime import datetime
import os
import tempfile
from csv_parser import CreditCardCSVParser

def load_transaction_data(csv_path):
    """Load and parse the credit card statement CSV."""
    try:
        parser = CreditCardCSVParser(csv_path)
        return parser.parse_transactions()
    except Exception as e:
        raise Exception(f"Error parsing CSV: {str(e)}")

def load_income_data(csv_path):
    """Load and parse the income CSV file."""
    try:
        df = pd.read_csv(csv_path)
        
        # Ensure required columns exist
        required_columns = ['date', 'income']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSV must contain 'date' and 'income' columns")
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Convert income to float
        df['income'] = pd.to_numeric(df['income'], errors='coerce')
        
        # Group by month and sum income
        df['month'] = df['date'].dt.strftime('%Y-%m')
        monthly_income = df.groupby('month')['income'].sum().reset_index()
        
        return monthly_income
    except Exception as e:
        raise Exception(f"Error parsing income CSV: {str(e)}")

def filter_transactions(df, date_range, selected_category, amount_range, search_term):
    """Apply filters to the transaction dataframe."""
    filtered_df = df.copy()
    
    # Date filter
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= date_range[0]) &
            (filtered_df['date'].dt.date <= date_range[1])
        ]
    
    # Category filter
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    # Amount filter
    filtered_df = filtered_df[
        (filtered_df['amount'] >= amount_range[0]) &
        (filtered_df['amount'] <= amount_range[1])
    ]
    
    # Description search
    if search_term:
        filtered_df = filtered_df[
            filtered_df['description'].str.contains(search_term, case=False, na=False)
        ]
    
    return filtered_df

def filter_income_data(income_df, date_range):
    """Filter income data by date range."""
    if len(date_range) == 2:
        income_df['date'] = pd.to_datetime(income_df['month'] + '-01')
        income_df = income_df[
            (income_df['date'].dt.date >= date_range[0]) &
            (income_df['date'].dt.date <= date_range[1])
        ]
    return income_df

def save_to_temp_file(uploaded_file, suffix='.csv'):
    """Save an uploaded file to a temporary file and return its path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

def cleanup_temp_file(file_path):
    """Clean up a temporary file."""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Warning: Could not clean up temporary file: {str(e)}") 