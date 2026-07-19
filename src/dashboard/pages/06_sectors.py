"""
NIFTY 100 Analytics Dashboard

Sector Analysis Dashboard
Sprint 4 - Day 26
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


DB_PATH = "nifty100.db"


@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    sectors = pd.read_sql(
        """
        SELECT
            company_id,
            broad_sector,
            sub_sector,
            index_weight_pct,
            market_cap_category
        FROM sectors
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


    ratios = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            debt_to_equity,
            net_profit_margin_pct
        FROM financial_ratios
        """,
        conn
    )


    conn.close()


    df = sectors.merge(
        companies,
        on="company_id",
        how="left"
    )


    df = df.merge(
        ratios,
        on="company_id",
        how="left"
    )


    return df



st.title("🏭 Sector Analysis")


df = load_data()


if df.empty:
    st.warning("No sector data available.")
    st.stop()



sector_list = sorted(
    df["broad_sector"].dropna().unique()
)


sector = st.selectbox(
    "Select Sector",
    sector_list
)



sector_df = df[
    df["broad_sector"] == sector
]



st.subheader("Sector Overview")


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Companies",
        sector_df["company_name"].nunique()
    )


with col2:
    st.metric(
        "Average ROE",
        f"{sector_df['return_on_equity_pct'].mean():.2f}%"
    )


with col3:
    st.metric(
        "Average Debt/Equity",
        f"{sector_df['debt_to_equity'].mean():.2f}"
    )



st.subheader("Companies in Sector")


st.dataframe(
    sector_df[
        [
            "company_name",
            "sub_sector",
            "return_on_equity_pct",
            "debt_to_equity",
            "net_profit_margin_pct"
        ]
    ],
    use_container_width=True
)



st.subheader("Sector ROE Comparison")


roe_df = (
    df.groupby("broad_sector")
    ["return_on_equity_pct"]
    .mean()
    .reset_index()
)


fig = px.bar(
    roe_df,
    x="broad_sector",
    y="return_on_equity_pct",
    title="Average ROE by Sector"
)


st.plotly_chart(
    fig,
    use_container_width=True
)