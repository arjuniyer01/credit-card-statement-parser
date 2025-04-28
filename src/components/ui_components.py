import streamlit as st
import pandas as pd
from datetime import datetime

def show_csv_format_info():
    """Show CSV format requirements in an expander."""
    with st.expander("CSV Format Requirements"):
        st.markdown("""
        ### Credit Card Statement CSV
        The credit card statement CSV should have the following columns:
        - `Transaction Date`: Date of the transaction (YYYY-MM-DD)
        - `Post Date`: Date the transaction was posted (YYYY-MM-DD)
        - `Description`: Description of the transaction
        - `Category`: Transaction category
        - `Type`: Transaction type
        - `Amount`: Transaction amount (negative for spending)
        - `Memo`: Additional transaction notes
        
        ### Income CSV
        The income CSV should have the following columns:
        - `date`: Date of the income (YYYY-MM-DD)
        - `income`: Amount of income (positive number)
        """)

def show_file_uploaders():
    """Show file uploaders for transactions and income data."""
    col1, col2 = st.columns(2)
    with col1:
        transactions_file = st.file_uploader("Upload your credit card statement (CSV)", type="csv")
    with col2:
        income_file = st.file_uploader("Upload your income data (CSV)", type="csv")
    return transactions_file, income_file

def show_filter_section(df):
    """Show the filter section for transactions."""
    st.subheader("Filter Transactions")
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        # Date range filter
        min_date = df['date'].min()
        max_date = df['date'].max()
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Category filter
        categories = ['All'] + sorted(df['category'].unique().tolist())
        selected_category = st.selectbox("Category", categories)
    
    with filter_col2:
        # Amount range filter
        min_amount = df['amount'].min()
        max_amount = df['amount'].max()
        amount_range = st.slider(
            "Amount Range ($)",
            min_value=float(min_amount),
            max_value=float(max_amount),
            value=(float(min_amount), float(max_amount))
        )
        
        # Description search
        search_term = st.text_input("Search Description", "")
    
    return date_range, selected_category, amount_range, search_term

def show_summary_metrics(df):
    """Show summary metrics for the filtered data."""
    st.subheader("Filtered Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spending", f"${df['amount'].sum():.2f}")
    with col2:
        st.metric("Number of Transactions", len(df))
    with col3:
        st.metric("Average Transaction", f"${df['amount'].mean():.2f}")
    with col4:
        st.metric("Unique Categories", df['category'].nunique())

def show_transaction_details(df):
    """Display transaction details in a sortable table."""
    return st.data_editor(
        df,
        column_config={
            "date": st.column_config.DateColumn(
                "Transaction Date",
                format="YYYY-MM-DD"
            ),
            "post_date": st.column_config.DateColumn(
                "Post Date",
                format="YYYY-MM-DD"
            ),
            "description": "Description",
            "category": "Category",
            "type": "Type",
            "amount": st.column_config.NumberColumn(
                "Amount",
                format="$%.2f"
            ),
            "memo": "Memo"
        },
        hide_index=True,
        use_container_width=True
    )

def show_income_data(income_df):
    """Display income data in a table."""
    st.dataframe(
        income_df,
        column_config={
            "month": "Month",
            "income": st.column_config.NumberColumn(
                "Income",
                format="$%.2f"
            )
        },
        hide_index=True
    )

def show_export_options(df):
    """Show export options for the data."""
    st.subheader("Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Download CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Click to Download",
                data=csv,
                file_name="transactions.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Download Excel"):
            df.to_excel("transactions.xlsx", index=False)
            with open("transactions.xlsx", "rb") as f:
                st.download_button(
                    label="Click to Download",
                    data=f,
                    file_name="transactions.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ) 