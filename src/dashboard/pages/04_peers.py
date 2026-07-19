"""
NIFTY 100 Analytics Dashboard

Peer Comparison
Sprint 4 - Day 24
"""

import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "nifty100.db"


@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    peer = pd.read_sql(
        "SELECT * FROM peer_percentiles",
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

    peer = peer.merge(
        companies,
        on="company_id",
        how="left"
    )

    return peer


st.title("👥 Peer Comparison")

df = load_data()

if df.empty:
    st.error("peer_percentiles table is empty.")
    st.stop()

# -------------------------------
# Peer Group Selection
# -------------------------------

groups = sorted(df["peer_group_name"].dropna().unique())

group = st.selectbox(
    "Select Peer Group",
    groups
)

peer_df = df[df["peer_group_name"] == group]

# -------------------------------
# Company Selection
# -------------------------------

companies = sorted(peer_df["company_name"].dropna().unique())

if len(companies) == 0:
    st.warning("No companies found for this peer group.")
    st.stop()

company = st.selectbox(
    "Select Company",
    companies
)

# -------------------------------
# Information
# -------------------------------

st.subheader("Peer Group Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Peer Group",
        group
    )

with col2:
    st.metric(
        "Companies",
        len(companies)
    )

# -------------------------------
# Raw Peer Data
# -------------------------------

st.subheader("Peer Percentile Records")

st.dataframe(
    peer_df,
    use_container_width=True
)

# -------------------------------
# Pivot Table
# -------------------------------

st.subheader("Peer Percentile Table")

pivot = peer_df.pivot_table(
    index="company_name",
    columns="metric",
    values="percentile_rank",
    aggfunc="first"
)

pivot = pivot.reset_index()

st.dataframe(
    pivot,
    use_container_width=True
)