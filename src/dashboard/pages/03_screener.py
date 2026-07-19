"""
NIFTY 100 Analytics Dashboard

Financial Screener Screen
Sprint 4 - Day 24
"""

import streamlit as st
import pandas as pd
import sqlite3


DB_PATH = "nifty100.db"


def load_screener_data():

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    market = pd.read_sql(
        "SELECT * FROM market_cap",
        conn
    )

    growth = pd.read_sql(
        "SELECT * FROM growth_metrics",
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

    df = ratios.merge(
        companies,
        on="company_id",
        how="left"
    )

    df = df.merge(
        market,
        on="company_id",
        how="left"
    )

    df = df.merge(
        growth,
        on="company_id",
        how="left"
    )

    return df


st.title("🔍 Financial Screener")

df = load_screener_data()

# ----------------------------------
# Preset Screeners
# ----------------------------------

st.sidebar.subheader("Preset Screeners")

preset = st.sidebar.selectbox(
    "Choose Preset",
    [
        "Custom",
        "Quality Compounder",
        "Value Pick",
        "Growth Accelerator",
        "Dividend Champion",
        "Debt-Free Blue Chip",
        "Turnaround Watch"
    ]
)

# Default values

roe_default = 0.0
debt_default = 5.0
fcf_default = 0
pe_default = 100.0
revenue_growth_default = 0.0

if preset == "Quality Compounder":
    roe_default = 15
    debt_default = 1
    revenue_growth_default = 10

elif preset == "Value Pick":
    debt_default = 2
    pe_default = 20

elif preset == "Growth Accelerator":
    debt_default = 2
    revenue_growth_default = 15

elif preset == "Dividend Champion":
    pass

elif preset == "Debt-Free Blue Chip":
    roe_default = 12
    debt_default = 0

elif preset == "Turnaround Watch":
    debt_default = 3
    revenue_growth_default = 10

# ----------------------------------
# Filters
# ----------------------------------

st.sidebar.subheader("Filters")

roe = st.sidebar.slider(
    "Minimum ROE",
    0.0,
    50.0,
    float(roe_default)
)

debt = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    float(debt_default)
)

fcf = st.sidebar.number_input(
    "Minimum Free Cash Flow",
    value=int(fcf_default)
)

pe = st.sidebar.slider(
    "Maximum P/E",
    0.0,
    100.0,
    float(pe_default)
)

revenue_growth = st.sidebar.slider(
    "Minimum Revenue CAGR",
    0.0,
    50.0,
    float(revenue_growth_default)
)

# ----------------------------------
# Apply Filters
# ----------------------------------

result = df.copy()

result = result[
    result["return_on_equity_pct"] >= roe
]

result = result[
    result["debt_to_equity"] <= debt
]

result = result[
    result["free_cash_flow_cr"] >= fcf
]

if "pe_ratio" in result.columns:

    result = result[
        result["pe_ratio"] <= pe
    ]

if "revenue_cagr_5y" in result.columns:

    result = result[
        result["revenue_cagr_5y"] >= revenue_growth
    ]

# ----------------------------------
# Display
# ----------------------------------

st.subheader(
    f"{len(result)} companies match your filters"
)

display_columns = [
    "company_name",
    "year",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pe_ratio",
    "revenue_cagr_5y"
]

display_columns = [
    col for col in display_columns
    if col in result.columns
]

st.dataframe(
    result[display_columns],
    use_container_width=True
)

csv = result.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    file_name="screener_results.csv",
    mime="text/csv"
)