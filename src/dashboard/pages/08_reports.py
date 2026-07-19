"""
NIFTY 100 Analytics Dashboard

Research Report Dashboard
Sprint 4 - Day 28
"""

import streamlit as st
import sqlite3
import pandas as pd


DB_PATH = "nifty100.db"


@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(
        """
        SELECT
            id AS company_id,
            company_name,
            about_company,
            website
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
            net_profit_margin_pct,
            free_cash_flow_cr,
            total_debt_cr,
            cash_from_operations_cr
        FROM financial_ratios
        """,
        conn
    )


    growth = pd.read_sql(
        """
        SELECT
            company_id,
            revenue_cagr_5y,
            pat_cagr_5y,
            eps_cagr_5y
        FROM growth_metrics
        """,
        conn
    )


    conn.close()


    df = companies.merge(
        ratios,
        on="company_id",
        how="left"
    )


    df = df.merge(
        growth,
        on="company_id",
        how="left"
    )


    return df



st.title("📄 Equity Research Report")


df = load_data()


if df.empty:
    st.warning("No report data available.")
    st.stop()



company_list = sorted(
    df["company_name"].dropna().unique()
)


company = st.selectbox(
    "Select Company",
    company_list
)



company_df = df[
    df["company_name"] == company
].sort_values("year")



latest = company_df.iloc[-1]



st.header(company)



st.subheader("🏢 Company Overview")


about = latest.get("about_company")


if pd.notna(about):
    st.write(about)
else:
    st.write("No company description available.")



st.subheader("📊 Financial Snapshot")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )


with col2:
    st.metric(
        "Net Profit Margin",
        f"{latest['net_profit_margin_pct']:.2f}%"
    )


with col3:
    st.metric(
        "Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
    )


with col4:
    st.metric(
        "Free Cash Flow",
        f"{latest['free_cash_flow_cr']:.2f} Cr"
    )



st.subheader("📈 Growth Summary")


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Revenue CAGR 5Y",
        f"{latest.get('revenue_cagr_5y',0):.2f}%"
    )


with col2:
    st.metric(
        "PAT CAGR 5Y",
        f"{latest.get('pat_cagr_5y',0):.2f}%"
    )


with col3:
    st.metric(
        "EPS CAGR 5Y",
        f"{latest.get('eps_cagr_5y',0):.2f}%"
    )



st.subheader("⚠️ Risk Analysis")


if latest["debt_to_equity"] <= 1:
    st.success("Debt level is under control")
else:
    st.warning("Higher debt exposure")


if latest["return_on_equity_pct"] >= 15:
    st.success("Strong return on equity")
else:
    st.warning("Low return on equity")



st.subheader("📋 Historical Financial Data")


st.dataframe(
    company_df,
    use_container_width=True
)



csv = company_df.to_csv(index=False).encode("utf-8")


st.download_button(
    "📥 Download Research Report",
    csv,
    file_name=f"{company}_research_report.csv",
    mime="text/csv"
)