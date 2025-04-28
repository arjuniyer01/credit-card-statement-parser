import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

class CreditCardCSVParser:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.transactions = []
        
    def parse_transactions(self) -> pd.DataFrame:
        """Parse the CSV file and return a DataFrame."""
        try:
            # Read the CSV file
            df = pd.read_csv(self.csv_path)
            
            # Rename columns to match our internal format
            column_mapping = {
                'Transaction Date': 'date',
                'Post Date': 'post_date',
                'Description': 'description',
                'Category': 'category',
                'Type': 'type',
                'Amount': 'amount',
                'Memo': 'memo'
            }
            
            # Rename columns if they exist
            df = df.rename(columns={col: column_mapping[col] for col in column_mapping if col in df.columns})
            
            # Convert date columns to datetime
            date_columns = ['date', 'post_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col])
            
            # Convert amount to float - handle both string and numeric values
            if 'amount' in df.columns:
                # First, convert to string to handle any numeric values
                df['amount'] = df['amount'].astype(str)
                # Then clean and convert to float
                df['amount'] = df['amount'].str.replace('$', '').str.replace(',', '').astype(float)
            
            # Fill missing categories with 'Other'
            if 'category' in df.columns:
                df['category'] = df['category'].fillna('Other')
            
            # Filter out positive transactions (keep only negative amounts)
            df = df[df['amount'] < 0]
            
            # Convert amounts to positive numbers for display
            df['amount'] = df['amount'].abs()
            
            return df
            
        except Exception as e:
            raise Exception(f"Error parsing CSV file: {str(e)}")
    
    def save_to_csv(self, output_path: str):
        """Save the processed transactions to a CSV file."""
        df = self.parse_transactions()
        df.to_csv(output_path, index=False)
        
        # Print summary
        if not df.empty:
            print("\nTransaction Summary:")
            print("-" * 80)
            print(f"Total transactions: {len(df)}")
            print("\nBy category:")
            category_summary = df.groupby('category').agg({
                'amount': ['count', 'sum']
            })
            category_summary.columns = ['Count', 'Total Amount']
            print(category_summary.round(2)) 