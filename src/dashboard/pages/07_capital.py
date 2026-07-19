"""
NIFTY 100 Analytics Dashboard

Capital Allocation Dashboard
Sprint 4 - Day 27
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


DB_PATH = "nifty100.db"


@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)


    capital = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            free_cash_flow_cr,
            capex_cr,
            dividend_payout_ratio_pct,
            total_debt_cr,
            cash_from_operations_cr
        FROM financial_ratios
        """,
        conn
    )


    companies = pd.read_sql(
        """
        SELECT
            id AS company_id,
            company_name
        FROM companies
        """,
        conn
    )


    conn.close()


    df = capital.merge(
        companies,
        on="company_id",
        how="left"
    )


    return df



st.title("🌳 Capital Allocation Dashboard")


df = load_data()


if df.empty:
    st.warning("No capital allocation data available.")
    st.stop()



companies = sorted(
    df["company_name"].dropna().unique()
)


company = st.selectbox(
    "Select Company",
    companies
)


company_df = df[
    df["company_name"] == company
].sort_values("year")



latest = company_df.iloc[-1]



st.subheader("Capital Allocation Snapshot")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Free Cash Flow",
        f"{latest['free_cash_flow_cr']:.2f} Cr"
    )


with col2:
    st.metric(
        "Capex",
        f"{latest['capex_cr']:.2f} Cr"
    )


with col3:
    st.metric(
        "Dividend Payout",
        f"{latest['dividend_payout_ratio_pct']:.2f}%"
    )


with col4:
    st.metric(
        "Total Debt",
        f"{latest['total_debt_cr']:.2f} Cr"
    )



st.subheader("Capital Trends")


metric = st.selectbox(
    "Select Metric",
    [
        "free_cash_flow_cr",
        "capex_cr",
        "cash_from_operations_cr",
        "total_debt_cr",
        "dividend_payout_ratio_pct"
    ]
)



fig = px.line(
    company_df,
    x="year",
    y=metric,
    markers=True,
    title=f"{company} - {metric}"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



st.subheader("Historical Data")


st.dataframe(
    company_df,
    use_container_width=True
)