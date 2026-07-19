"""
NIFTY 100 Analytics Dashboard

Company Profile Screen
Sprint 4 - Day 23
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


DB_PATH = "nifty100.db"


def get_company_data(company_name):

    conn = sqlite3.connect(DB_PATH)

    company = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE company_name = ?
        """,
        conn,
        params=[company_name]
    )

    conn.close()

    return company


def get_ratios(company_id):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=[company_id]
    )

    conn.close()

    return df


def get_profit_loss(company_id):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=[company_id]
    )

    conn.close()

    return df



st.title("🏢 Company Profile")


# Company list

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT company_name FROM companies",
    conn
)

conn.close()


selected_company = st.selectbox(
    "Search Company",
    companies["company_name"].tolist()
)


company = get_company_data(
    selected_company
)


if not company.empty:

    company_id = company.iloc[0]["id"]


    ratios = get_ratios(
        company_id
    )


    pl = get_profit_loss(
        company_id
    )


    st.subheader(
        selected_company
    )


    # KPI cards

    if not ratios.empty:

        latest = ratios.iloc[-1]


        c1,c2,c3,c4 = st.columns(4)


        c1.metric(
            "ROE",
            f"{latest['return_on_equity_pct']}%"
        )

        c2.metric(
            "ROCE",
            f"{latest['return_on_equity_pct']}%"
        )

        c3.metric(
            "Net Profit Margin",
            f"{latest['net_profit_margin_pct']}%"
        )

        c4.metric(
            "Debt/Equity",
            latest["debt_to_equity"]
        )


    st.divider()


    # Revenue chart

    st.subheader(
        "Revenue & Net Profit Trend"
    )


    if not pl.empty:

        fig = px.line(
            pl,
            x="year",
            y=[
                "sales",
                "net_profit"
            ],
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ROE trend

    st.subheader(
        "ROE Trend"
    )


    if not ratios.empty:

        fig2 = px.line(
            ratios,
            x="year",
            y="return_on_equity_pct",
            markers=True
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


else:

    st.warning(
        "Company not found"
    )