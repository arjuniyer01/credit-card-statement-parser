import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import calendar

def plot_spending_by_category(df):
    """Create a pie chart of spending by category."""
    category_totals = df.groupby('category')['amount'].sum().reset_index()
    fig = px.pie(
        category_totals,
        values='amount',
        names='category',
        title='Spending by Category',
        hole=0.4,
    )
    return fig

def plot_daily_spending(df):
    """Create a line chart of daily spending."""
    df['date'] = pd.to_datetime(df['date'])
    daily_spending = df.groupby('date')['amount'].sum().reset_index()
    daily_spending['cumulative'] = daily_spending['amount'].cumsum()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_spending['date'],
        y=daily_spending['cumulative'],
        mode='lines+markers',
        name='Cumulative Spending'
    ))
    fig.update_layout(
        title='Cumulative Daily Spending',
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        hovermode='x unified'
    )
    return fig

def plot_spending_trends(df):
    """Create a bar chart of spending trends by category over time."""
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')
    
    monthly_category = df.groupby(['month', 'category'])['amount'].sum().reset_index()
    
    fig = px.bar(
        monthly_category,
        x='month',
        y='amount',
        color='category',
        title='Monthly Spending by Category',
        labels={'month': 'Month', 'amount': 'Amount ($)', 'category': 'Category'}
    )
    return fig

def plot_top_merchants(df, top_n=10):
    """Create a bar chart of top merchants by spending."""
    merchant_totals = df.groupby('description')['amount'].sum().reset_index()
    merchant_totals = merchant_totals.sort_values('amount', ascending=False).head(top_n)
    
    fig = px.bar(
        merchant_totals,
        x='description',
        y='amount',
        title=f'Top {top_n} Merchants by Spending',
        labels={'description': 'Merchant', 'amount': 'Amount ($)'}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig

def plot_merchant_frequency(df, top_n=10):
    """Create a bar chart of most frequent merchants."""
    merchant_counts = df.groupby('description').size().reset_index(name='count')
    merchant_counts = merchant_counts.sort_values('count', ascending=False).head(top_n)
    
    fig = px.bar(
        merchant_counts,
        x='description',
        y='count',
        title=f'Top {top_n} Most Frequent Merchants',
        labels={'description': 'Merchant', 'count': 'Number of Transactions'}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig

def plot_large_transactions(df, threshold=100):
    """Create a bar chart of large transactions."""
    large_transactions = df[df['amount'] >= threshold].sort_values('amount', ascending=False)
    
    fig = px.bar(
        large_transactions,
        x='description',
        y='amount',
        title=f'Large Transactions (${threshold}+)',
        labels={'description': 'Merchant', 'amount': 'Amount ($)'}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig

def plot_category_comparison(df):
    """Create a radar chart comparing categories."""
    category_totals = df.groupby('category')['amount'].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=category_totals['amount'],
        theta=category_totals['category'],
        fill='toself',
        name='Spending'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, category_totals['amount'].max()]
            )
        ),
        title='Category Comparison'
    )
    
    return fig

def plot_spending_by_day(df):
    """Create a bar chart of spending by day of week."""
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    
    daily_totals = df.groupby('day_of_week')['amount'].sum().reset_index()
    
    # Reorder days of week
    days_order = list(calendar.day_name)
    daily_totals['day_of_week'] = pd.Categorical(
        daily_totals['day_of_week'],
        categories=days_order,
        ordered=True
    )
    daily_totals = daily_totals.sort_values('day_of_week')
    
    fig = px.bar(
        daily_totals,
        x='day_of_week',
        y='amount',
        title='Spending by Day of Week',
        labels={'day_of_week': 'Day', 'amount': 'Amount ($)'}
    )
    
    return fig

def plot_income_vs_spending(df, income_df):
    """Create a bar chart comparing income and spending by month."""
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')
    
    monthly_spending = df.groupby('month')['amount'].sum().reset_index()
    
    # Merge spending and income data
    comparison_df = pd.merge(monthly_spending, income_df, on='month', how='outer')
    comparison_df = comparison_df.fillna(0)
    
    # Create the comparison chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=comparison_df['month'],
        y=comparison_df['amount'],
        name='Spending',
        marker_color='red'
    ))
    
    fig.add_trace(go.Bar(
        x=comparison_df['month'],
        y=comparison_df['income'],
        name='Income',
        marker_color='green'
    ))
    
    fig.update_layout(
        title='Monthly Income vs Spending',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        barmode='group'
    )
    
    return fig

def plot_savings_rate(df, income_df):
    """Create a line chart showing savings rate over time."""
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')
    
    monthly_spending = df.groupby('month')['amount'].sum().reset_index()
    
    # Merge spending and income data
    comparison_df = pd.merge(monthly_spending, income_df, on='month', how='outer')
    comparison_df = comparison_df.fillna(0)
    
    # Calculate savings rate
    comparison_df['savings_rate'] = ((comparison_df['income'] - comparison_df['amount']) / comparison_df['income'] * 100)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=comparison_df['month'],
        y=comparison_df['savings_rate'],
        mode='lines+markers',
        name='Savings Rate'
    ))
    
    fig.update_layout(
        title='Monthly Savings Rate',
        xaxis_title='Month',
        yaxis_title='Savings Rate (%)',
        hovermode='x unified'
    )
    
    return fig

def plot_income_distribution(income_df):
    """Create a histogram of income distribution."""
    fig = px.histogram(
        income_df,
        x='income',
        title='Income Distribution',
        labels={'income': 'Income ($)'},
        nbins=20
    )
    
    return fig

def plot_income_trend(income_df):
    """Create a line chart showing income trend."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=income_df['month'],
        y=income_df['income'],
        mode='lines+markers',
        name='Income'
    ))
    
    fig.update_layout(
        title='Income Trend',
        xaxis_title='Month',
        yaxis_title='Income ($)',
        hovermode='x unified'
    )
    
    return fig 