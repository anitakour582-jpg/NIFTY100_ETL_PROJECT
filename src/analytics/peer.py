"""
Sprint 3 - Day 18

Peer Percentile Rankings
"""

import sqlite3
import pandas as pd

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from screener.engine import load_financial_data

DB_PATH = "nifty100.db"
PEER_FILE = "data/raw/peer_groups.xlsx"


# ----------------------------------------
# Load Peer Groups
# ----------------------------------------

def load_peer_groups():

    peer_df = pd.read_excel(
        PEER_FILE
    )

    return peer_df



# ----------------------------------------
# Prepare Peer Data
# ----------------------------------------

def prepare_peer_data():

    financial_df = load_financial_data()

    peer_df = load_peer_groups()

    merged = financial_df.merge(
        peer_df,
        on="company_id",
        how="left"
    )

    return merged



# ----------------------------------------
# Calculate Peer Percentiles
# ----------------------------------------

def calculate_peer_percentiles():

    df = prepare_peer_data()


    metrics = [

        "return_on_equity_pct",

        "net_profit_margin_pct",

        "debt_to_equity",

        "free_cash_flow_cr",

        "pat_cagr_5y",

        "revenue_cagr_5y",

        "eps_cagr_5y",

        "interest_coverage",

        "asset_turnover"

    ]


    records = []


    peer_df = df[
        df["peer_group_name"].notna()
    ].copy()



    for group_name, group in peer_df.groupby(
        "peer_group_name"
    ):


        for metric in metrics:


            if metric not in group.columns:

                continue



            temp = group.copy()



            # D/E lower is better
            if metric == "debt_to_equity":

                temp["percentile_rank"] = (

                    1 -

                    temp[metric]
                    .rank(
                        pct=True
                    )

                ) * 100


            else:

                temp["percentile_rank"] = (

                    temp[metric]
                    .rank(
                        pct=True
                    )

                ) * 100



            for _, row in temp.iterrows():


                records.append({

                    "company_id":
                        row["company_id"],


                    "peer_group_name":
                        group_name,


                    "metric":
                        metric,


                    "value":
                        row[metric],


                    "percentile_rank":
                        row["percentile_rank"],


                    "year":
                        row["year"]

                })



    return pd.DataFrame(records)




# ----------------------------------------
# Save to SQLite
# ----------------------------------------

def save_peer_percentiles(df):

    conn = sqlite3.connect(
        DB_PATH
    )


    df.to_sql(

        "peer_percentiles",

        conn,

        if_exists="replace",

        index=False

    )


    conn.close()


    print(
        "Peer percentiles saved successfully."
    )




# ----------------------------------------
# Main
# ----------------------------------------

if __name__ == "__main__":


    peer_percentiles = (
        calculate_peer_percentiles()
    )


    save_peer_percentiles(
        peer_percentiles
    )


    print(
        peer_percentiles.head()
    )


    print(
        "Total rows:",
        len(peer_percentiles)
    )