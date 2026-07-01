import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="MYNTRA Financial Intelligence Dashboard",
    layout="wide"
)

st.title("📊 MYNTRA Financial Intelligence Dashboard")

# Upload file
uploaded_file = st.file_uploader(
    "Upload MYNTRA Excel File",
    type=["xlsx"]
)

if uploaded_file:

    monthly = pd.read_excel(uploaded_file, sheet_name="Monthly_Report")
    expense = pd.read_excel(uploaded_file, sheet_name="Expense_Breakdown")
    cashflow = pd.read_excel(uploaded_file, sheet_name="Cash_Flow_Statement")
    budget = pd.read_excel(uploaded_file, sheet_name="Budget_vs_Actual")
    executive = pd.read_excel(uploaded_file, sheet_name="Executive_Summary")

    # ---------------- KPI SECTION ----------------
    st.subheader("Executive Summary")

    total_revenue = executive.loc[
        executive["Metric"] == "Total Revenue", "Actual"
    ].values[0]

    total_expense = executive.loc[
        executive["Metric"] == "Total Expenses & CAPEX", "Actual"
    ].values[0]

    net_result = executive.loc[
        executive["Metric"] == "Net Result", "Actual"
    ].values[0]

    closing_cash = cashflow["Closing_Balance"].iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"₹ {total_revenue:,.2f} Cr"
    )

    col2.metric(
        "Total Expenses",
        f"₹ {total_expense:,.2f} Cr"
    )

    col3.metric(
        "Net Result",
        f"₹ {net_result:,.2f} Cr"
    )

    col4.metric(
        "Closing Cash Balance",
        f"₹ {closing_cash:,.2f} Cr"
    )

    st.divider()

    # ---------------- REVENUE VS EXPENSE ----------------
    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            monthly,
            x="Month",
            y=["Total_Revenue", "Operating_Expenses"],
            markers=True,
            title="Monthly Revenue vs Operating Expenses"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        expense_cols = [
            "Operating_Expenses",
            "Employee_Costs",
            "Marketing_Costs",
            "R&D_Costs",
            "CAPEX"
        ]

        expense_values = expense[expense_cols].iloc[0]

        pie = px.pie(
            names=expense_cols,
            values=expense_values,
            title="Expense Breakdown"
        )

        st.plotly_chart(pie, use_container_width=True)

    # ---------------- CASH FLOW ----------------
    st.subheader("Cash Flow Analysis")

    cash_fig = px.bar(
        cashflow,
        x="Month",
        y="Net_Cash_Flow",
        title="Monthly Net Cash Flow"
    )

    st.plotly_chart(cash_fig, use_container_width=True)

    balance_fig = px.line(
        cashflow,
        x="Month",
        y=["Opening_Balance", "Closing_Balance"],
        markers=True,
        title="Cash Balance Trend"
    )

    st.plotly_chart(balance_fig, use_container_width=True)

    # ---------------- BUDGET VS ACTUAL ----------------
    st.subheader("Budget vs Actual")

    comparison = px.bar(
        budget,
        x="Category",
        y=["Budget_Annual", "Actual_Annual"],
        barmode="group",
        title="Budget vs Actual Comparison"
    )

    st.plotly_chart(comparison, use_container_width=True)

    st.dataframe(
        budget,
        use_container_width=True
    )

    # ---------------- SHEET VIEWER ----------------
    st.subheader("Excel Sheet Viewer")

    sheet_names = [
        "Monthly_Report",
        "Expense_Breakdown",
        "Cash_Flow_Statement",
        "Inflows_vs_Outflows",
        "Budget_vs_Actual",
        "Revenue_Budget_Actual",
        "Expenses_Budget_Actual",
        "Executive_Summary",
        "Raw_Data_Sample"
    ]

    selected_sheet = st.selectbox(
        "Select Sheet",
        sheet_names
    )

    df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.info("Upload the MYNTRA Excel file to generate the dashboard.")
