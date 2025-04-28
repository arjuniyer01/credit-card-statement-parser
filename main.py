import argparse
from my_parser import CreditCardStatementParser
import subprocess
import sys

def run_cli(pdf_path: str, output_path: str = "transactions.csv"):
    """Run in CLI mode - parse PDF and save to CSV."""
    parser = CreditCardStatementParser(pdf_path)
    transactions = parser.parse_transactions()
    parser.save_to_csv(output_path)

def run_ui():
    """Run in UI mode - launch Streamlit interface."""
    subprocess.run([sys.executable, "-m", "streamlit", "run", "ui.py"])

def main():
    parser = argparse.ArgumentParser(description="Credit Card Statement Parser")
    parser.add_argument("--ui", action="store_true", help="Launch the UI interface")
    parser.add_argument("--pdf", type=str, help="Path to the PDF statement")
    parser.add_argument("--output", type=str, default="transactions.csv", help="Output CSV file path")
    
    args = parser.parse_args()
    
    if args.ui:
        run_ui()
    elif args.pdf:
        run_cli(args.pdf, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
