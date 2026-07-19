"""
NIFTY 100 Analytics Dashboard

Database Utility Loader

Sprint 4 - Day 22
"""

import sqlite3
import pandas as pd
import streamlit as st


DB_PATH = "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            id AS company_id,
            company_name
        FROM companies
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_ratios(company_id, year=None):

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    """

    params = [company_id]

    if year:
        query += " AND year = ?"
        params.append(year)

    df = pd.read_sql(
        query,
        conn,
        params=params
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_pl(company_id):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        """,
        conn,
        params=[company_id]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_bs(company_id):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        """,
        conn,
        params=[company_id]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_cf(company_id):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        """,
        conn,
        params=[company_id]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM sectors
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM peer_percentiles
        WHERE peer_group_name = ?
        """,
        conn,
        params=[group_name]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_valuation(company_id):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM valuation
        WHERE company_id = ?
        """,
        conn,
        params=[company_id]
    )

    conn.close()

    return df