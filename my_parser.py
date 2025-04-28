import pdfplumber
import pandas as pd
from typing import List, Dict, Any
import re
from datetime import datetime

class CreditCardStatementParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.transactions = []
        self.statement_date = None
        
        # Define categories and their keywords
        self.categories = {
            'Food & Dining': ['RESTAURANT', 'CAFE', 'CUISINE', 'THAI', 'FOOD', 'PIZZA', 'BURGER', 'KITCHEN'],
            'Travel & Transportation': ['AIRLINE', 'HOTEL', 'HYATT', 'UBER', 'LYFT', 'TAXI', 'PARKING', 'TRANSIT'],
            'Shopping': ['AMAZON', 'TARGET', 'WALMART', 'COSTCO', 'STORE', 'MARKET'],
            'Entertainment': ['NETFLIX', 'SPOTIFY', 'HULU', 'CINEMA', 'THEATER', 'MOVIE'],
            'Utilities': ['ELECTRIC', 'WATER', 'GAS', 'INTERNET', 'PHONE', 'MOBILE'],
            'Other': []  # Default category
        }
        
    def clean_text(self, text: str) -> str:
        """Clean up duplicated characters in the text."""
        # Remove duplicate adjacent characters (e.g., "MMaannaaggee" -> "Manage")
        cleaned = ""
        i = 0
        while i < len(text):
            if i + 1 < len(text) and text[i] == text[i + 1]:
                cleaned += text[i]
                i += 2
            else:
                cleaned += text[i]
                i += 1
        return cleaned
        
    def extract_text_from_pdf(self) -> str:
        """Extract text content from the PDF file."""
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return self.clean_text(text)
    
    def extract_statement_date(self, text: str) -> None:
        """Extract statement month and year."""
        # Look for month and year pattern (e.g., "May 2025")
        match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', text)
        if match:
            month, year = match.groups()
            self.statement_date = datetime.strptime(f"{month} {year}", "%B %Y")
    
    def categorize_transaction(self, description: str) -> str:
        """Categorize transaction based on description."""
        description = description.upper()
        for category, keywords in self.categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        return 'Other'
    
    def parse_date(self, date_str: str) -> datetime:
        """Parse date string into datetime object."""
        try:
            # First try with year
            return datetime.strptime(date_str, '%m/%d/%y')
        except ValueError:
            try:
                # If no year, use the statement year
                if self.statement_date:
                    date = datetime.strptime(date_str, '%m/%d')
                    return date.replace(year=self.statement_date.year)
                return datetime.strptime(date_str, '%m/%d')
            except ValueError:
                return None
    
    def parse_transactions(self) -> List[Dict[str, Any]]:
        """Parse the extracted text to identify transactions."""
        text = self.extract_text_from_pdf()
        print(text)
        self.extract_statement_date(text)
        
        # Print cleaned text for debugging
        print("Cleaned text from PDF:")
        print("-" * 80)
        print(text[:2000])
        print("-" * 80)
        
        # Improved transaction pattern
        transaction_pattern = (
            r'('                # Start of the first capturing group
            r'\d{2}/\d{2}'      # Match date in MM/DD format
            r'(?:/\d{2})?'      # Optionally match /YY for year
            r')\s+'             # End of the first capturing group and match one or more spaces
            r'('                # Start of the second capturing group
            r'[A-Za-z0-9\s\.,&\-\']+?'  # Match description with alphanumeric and special characters
            r')\s+'             # End of the second capturing group and match one or more spaces
            r'('                # Start of the third capturing group
            r'[\-\$]?'          # Optionally match a negative sign or dollar sign
            r'\d{1,3}'          # Match one to three digits
            r'(?:,\d{3})*'      # Optionally match groups of three digits separated by commas
            r'(?:\.\d{2})?'     # Optionally match a decimal point followed by two digits
            r')\s'              # End of the third capturing group and match a space
        )
        
        matches = re.finditer(transaction_pattern, text)
        for match in matches:
            print(match.groups())
            date_str, description, amount_str = match.groups()
            
            # Clean up the amount string
            amount_str = amount_str.replace('$', '').replace(',', '')
            try:
                amount = float(amount_str)
            except ValueError:
                continue
                
            # Parse the date
            date = self.parse_date(date_str)
            if not date:
                continue
                
            # Clean up description
            description = description.strip()
            
            # Categorize transaction
            category = self.categorize_transaction(description)
            
            self.transactions.append({
                'date': date,
                'description': description,
                'amount': amount,
                'category': category
            })
        
        return self.transactions
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert parsed transactions to a pandas DataFrame."""
        df = pd.DataFrame(self.transactions)
        if not df.empty:
            # Sort by date
            df = df.sort_values('date')
            
            # Format amount to 2 decimal places
            df['amount'] = df['amount'].round(2)
            
            # Format date as YYYY-MM-DD
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            
        return df
    
    def save_to_csv(self, output_path: str):
        """Save parsed transactions to a CSV file."""
        df = self.to_dataframe()
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
