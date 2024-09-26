import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page title
st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")

# Title of the dashboard
st.title("📊 Personal Finance Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file of financial transactions", type=["csv"])

# Function to load and clean data
def load_data(file):
    data = pd.read_csv(file)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# If file is uploaded, process the data
if uploaded_file is not None:
    # Load data
    df = load_data(uploaded_file)

    # Sidebar filters
    st.sidebar.header("Filters")
    category_filter = st.sidebar.multiselect("Select Categories", options=df['Category'].unique(), default=df['Category'].unique())
    
    # Apply filters
    df_filtered = df[df['Category'].isin(category_filter)]

    # Sidebar budget input
    st.sidebar.header("Budget")
    monthly_budget = st.sidebar.number_input("Set your monthly budget", value=1500)

    # Calculate totals
    total_income = df_filtered[df_filtered['Amount'] > 0]['Amount'].sum()
    total_expense = df_filtered[df_filtered['Amount'] < 0]['Amount'].sum()
    net_income = total_income + total_expense
    budget_remaining = monthly_budget + total_expense

    # Show summary at the top
    st.subheader("Monthly Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", f"${total_income:.2f}")
    col2.metric("Total Expenses", f"${-total_expense:.2f}")
    col3.metric("Net Income", f"${net_income:.2f}")
    col4.metric("Budget Remaining", f"${budget_remaining:.2f}")

    # Line chart for spending trend over time
    st.subheader("Spending Trend Over Time")
    fig, ax = plt.subplots()
    sns.lineplot(data=df_filtered, x='Date', y='Amount', hue='Category', marker='o', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Pie chart for spending by category
    st.subheader("Spending by Category")
    expense_data = df_filtered[df_filtered['Amount'] < 0]
    fig_pie = px.pie(expense_data, names='Category', values='Amount', title="Spending Breakdown")
    st.plotly_chart(fig_pie)

    # Bar chart of income vs expenses
    st.subheader("Income vs Expenses")
    income_expense_data = pd.DataFrame({
        'Type': ['Income', 'Expense'],
        'Amount': [total_income, -total_expense]
    })
    fig_bar = px.bar(income_expense_data, x='Type', y='Amount', text='Amount', title="Income vs Expenses", color='Type')
    st.plotly_chart(fig_bar)

    # Show the full table of transactions
    st.subheader("Full Transaction Data")
    st.dataframe(df_filtered)

else:
    st.info("Please upload a CSV file to analyze your finances.")
