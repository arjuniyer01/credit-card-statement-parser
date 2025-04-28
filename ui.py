import streamlit as st
import pandas as pd
from datetime import datetime
import os
import tempfile

from src.visualizations.plots import (
    plot_spending_by_category,
    plot_daily_spending,
    plot_spending_trends,
    plot_top_merchants,
    plot_merchant_frequency,
    plot_large_transactions,
    plot_category_comparison,
    plot_spending_by_day,
    plot_income_vs_spending,
    plot_savings_rate,
    plot_income_distribution,
    plot_income_trend
)

from src.utils.data_loader import (
    load_transaction_data,
    load_income_data,
    filter_transactions,
    filter_income_data,
    save_to_temp_file,
    cleanup_temp_file
)

from src.components.ui_components import (
    show_csv_format_info,
    show_file_uploaders,
    show_filter_section,
    show_summary_metrics,
    show_transaction_details,
    show_income_data,
    show_export_options
)

def main():
    st.set_page_config(
        page_title="Spending Dashboard",
        page_icon="💳",
        layout="wide"
    )
    
    st.title("Spending Dashboard 💳")
    
    # Show CSV format information
    show_csv_format_info()
    
    # File uploaders
    transactions_file, income_file = show_file_uploaders()
    
    if transactions_file:
        try:
            # Create a temporary file with a unique name
            temp_path = save_to_temp_file(transactions_file)
            
            # Load and parse the data
            df = load_transaction_data(temp_path)
            
            if df is not None and not df.empty:
                # Filter section at the top
                date_range, selected_category, amount_range, search_term = show_filter_section(df)
                
                # Apply filters
                filtered_df = filter_transactions(
                    df, date_range, selected_category, amount_range, search_term
                )

                # Transaction details
                st.subheader("Transaction Details (editable)")
                edited_df = show_transaction_details(filtered_df)
                
                # Show filtered summary
                show_summary_metrics(edited_df)
                
                # Create tabs for different views
                tab1, tab2 = st.tabs(["Spending Analysis", "Income Tracking"])
                
                with tab1:
                    # Visualizations
                    st.subheader("Spending Analysis")
                    
                    # First row of plots
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(plot_spending_by_category(filtered_df), use_container_width=True)
                    with col2:
                        st.plotly_chart(plot_category_comparison(filtered_df), use_container_width=True)
                    
                    # Second row of plots
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(plot_top_merchants(filtered_df), use_container_width=True)
                    with col2:
                        st.plotly_chart(plot_merchant_frequency(filtered_df), use_container_width=True)
                    
                    # Third row of plots
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(plot_large_transactions(filtered_df), use_container_width=True)
                    with col2:
                        st.plotly_chart(plot_spending_by_day(filtered_df), use_container_width=True)
                
                with tab2:
                    st.subheader("Income Tracking")
                    
                    if income_file:
                        try:
                            # Create a temporary file for income data
                            income_path = save_to_temp_file(income_file)
                            
                            # Load income data
                            income_df = load_income_data(income_path)
                            
                            # Filter income data by date range
                            filtered_income_df = filter_income_data(income_df, date_range)
                            
                            # Calculate and display income vs spending
                            st.subheader("Income vs Spending Analysis")
                            
                            # First row of plots
                            col1, col2 = st.columns(2)
                            with col1:
                                st.plotly_chart(plot_income_vs_spending(filtered_df, filtered_income_df), use_container_width=True)
                            with col2:
                                st.plotly_chart(plot_savings_rate(filtered_df, filtered_income_df), use_container_width=True)
                            
                            # Second row of plots
                            col1, col2 = st.columns(2)
                            with col1:
                                st.plotly_chart(plot_income_distribution(filtered_income_df), use_container_width=True)
                            with col2:
                                st.plotly_chart(plot_income_trend(filtered_income_df), use_container_width=True)
                            
                            # Calculate and display savings rate
                            total_income = filtered_income_df['income'].sum()
                            total_spending = filtered_df['amount'].sum()
                            savings_rate = ((total_income - total_spending) / total_income * 100) if total_income > 0 else 0
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Income", f"${total_income:.2f}")
                            with col2:
                                st.metric("Total Spending", f"${total_spending:.2f}")
                            with col3:
                                st.metric("Savings Rate", f"{savings_rate:.1f}%")
                            
                            # Show income data
                            st.subheader("Income Data")
                            show_income_data(filtered_income_df)
                            
                        except Exception as e:
                            st.error(f"Error processing income data: {str(e)}")
                        
                        finally:
                            # Clean up temporary income file
                            cleanup_temp_file(income_path)
                    else:
                        st.info("Please upload an income CSV file to begin income tracking.")
                
                # Export options
                # show_export_options(filtered_df)
            else:
                st.error("No transactions found in the CSV.")
        
        except Exception as e:
            st.error(f"Error processing the CSV: {str(e)}")
        
        finally:
            # Clean up temporary files
            cleanup_temp_file(temp_path)
    
    else:
        st.info("Please upload a credit card statement CSV to begin analysis.")
        
if __name__ == "__main__":
    main() 