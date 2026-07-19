"""
NIFTY 100 Analytics Dashboard

Trends Dashboard
Sprint 4 - Day 25
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


DB_PATH = "nifty100.db"


@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    pnl = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            operating_profit,
            net_profit
        FROM profitandloss
        """,
        conn
    )

    ratios = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            operating_profit_margin_pct,
            net_profit_margin_pct
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


    df = pnl.merge(
        ratios,
        on=["company_id", "year"],
        how="left"
    )

    df = df.merge(
        companies,
        on="company_id",
        how="left"
    )

    return df



st.title("📈 Financial Trends Dashboard")


df = load_data()


if df.empty:
    st.warning("No trend data available.")
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



metrics = {

    "Revenue": "sales",

    "Operating Profit": "operating_profit",

    "Net Profit": "net_profit",

    "ROE %": "return_on_equity_pct",

    "Operating Margin %": "operating_profit_margin_pct",

    "Net Margin %": "net_profit_margin_pct"

}



metric_name = st.selectbox(
    "Select Metric",
    list(metrics.keys())
)


column = metrics[metric_name]



fig = px.line(
    company_df,
    x="year",
    y=column,
    markers=True,
    title=f"{company} - {metric_name} Trend"
)



fig.update_layout(
    height=500,
    xaxis_title="Year",
    yaxis_title=metric_name
)



st.plotly_chart(
    fig,
    use_container_width=True
)



st.subheader("Historical Data")


st.dataframe(
    company_df[
        [
            "year",
            "sales",
            "net_profit",
            "return_on_equity_pct",
            "operating_profit_margin_pct",
            "net_profit_margin_pct"
        ]
    ],
    use_container_width=True
)



csv = company_df.to_csv(index=False).encode("utf-8")


st.download_button(
    "📥 Download Trend Data",
    csv,
    file_name=f"{company}_trends.csv",
    mime="text/csv"
)