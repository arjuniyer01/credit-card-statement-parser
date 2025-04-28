# Spending Dashboard 💳

A powerful and interactive dashboard for analyzing credit card transactions and income data. Built with Streamlit and Plotly, this application helps you track your spending patterns, monitor income, and visualize your financial health.

## Features

### Transaction Analysis
- 📊 Interactive visualizations of spending patterns
- 🏷️ Automatic transaction categorization
- 🔍 Advanced filtering by date, category, amount, and description
- 📈 Spending trends and merchant analysis
- 📱 Mobile-responsive design

### Income Tracking
- 💰 Income vs. spending comparison
- 📉 Savings rate calculation and visualization
- 📊 Income distribution analysis
- 📈 Income trend tracking

### Data Management
- 📤 CSV file upload support
- 📥 Data export to CSV and Excel
- 🔄 Real-time data filtering
- ✏️ Editable transaction details

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/credit-card-statement-parser.git
cd credit-card-statement-parser
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run ui.py
```

2. Upload your credit card statement CSV file with the following columns:
   - Transaction Date (YYYY-MM-DD)
   - Post Date (YYYY-MM-DD)
   - Description
   - Category
   - Type
   - Amount (negative for spending)
   - Memo

3. (Optional) Upload your income CSV file with:
   - date (YYYY-MM-DD)
   - income (positive number)

4. Use the interactive dashboard to:
   - Filter transactions
   - View spending patterns
   - Track income and savings
   - Export data

## Project Structure

```
credit-card-statement-parser/
├── src/
│   ├── components/
│   │   └── ui_components.py    # UI components and layouts
│   ├── utils/
│   │   └── data_loader.py      # Data loading and processing
│   └── visualizations/
│       └── plots.py            # Plotting functions
├── ui.py                       # Main application file
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Dependencies

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- Other dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/) 