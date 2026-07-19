"""
NIFTY 100 Analytics Dashboard

Home Screen
Sprint 4 - Day 23
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_sectors
)
import sqlite3


DB_PATH = "nifty100.db"


def load_home_data():

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

    conn.close()

    return ratios, market, growth



st.title("📊 Nifty 100 Analytics Dashboard")

st.write(
    "Company analysis, financial screener, peer comparison, "
    "sector analysis and valuation insights."
)


# Load data

companies = get_companies()
sectors = get_sectors()

ratios, market, growth = load_home_data()


# Year selector

year = st.sidebar.selectbox(
    "Select Year",
    sorted(
        ratios["year"].dropna().unique(),
        reverse=True
    )
)


ratios_year = ratios[
    ratios["year"] == year
]


# KPI calculations

avg_roe = round(
    ratios_year["return_on_equity_pct"].mean(),
    2
)

median_pe = round(
    market["pe_ratio"].median(),
    2
)

median_de = round(
    ratios_year["debt_to_equity"].median(),
    2
)

median_growth = round(
    growth["revenue_cagr_5y"].median(),
    2
)


debt_free = len(
    ratios_year[
        ratios_year["debt_to_equity"] == 0
    ]
)



# KPI cards

c1,c2,c3,c4,c5,c6 = st.columns(6)


c1.metric(
    "Average ROE",
    f"{avg_roe}%"
)

c2.metric(
    "Median P/E",
    median_pe
)

c3.metric(
    "Median D/E",
    median_de
)

c4.metric(
    "Companies",
    len(companies)
)

c5.metric(
    "Revenue CAGR",
    f"{median_growth}%"
)

c6.metric(
    "Debt Free",
    debt_free
)



st.divider()


# Sector chart

st.subheader(
    "Sector Breakdown"
)


sector_count = (
    sectors["broad_sector"]
    .value_counts()
    .reset_index()
)


sector_count.columns = [
    "Sector",
    "Companies"
]


fig = px.pie(
    sector_count,
    names="Sector",
    values="Companies",
    hole=0.4
)


st.plotly_chart(
    fig,
    use_container_width=True
)



st.divider()


st.subheader(
    "Top Companies by Quality Score"
)


try:

    scores = pd.read_csv(
        "output/final_company_scores_clean.csv"
    )

    st.dataframe(
        scores.head(5),
        use_container_width=True
    )

except:

    st.info(
        "Composite score file not available"
    )