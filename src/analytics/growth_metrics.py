"""
Sprint 3 - Growth Metrics Engine

Calculates:
- Revenue CAGR 5Y
- PAT CAGR 5Y
- EPS CAGR 5Y
"""

import sqlite3
import pandas as pd


DB_PATH = "nifty100.db"


def calculate_cagr(start, end, years=5):

    if start <= 0 or end <= 0:
        return None

    return ((end / start) ** (1 / years) - 1) * 100



def main():

    conn = sqlite3.connect(DB_PATH)

    pnl = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            net_profit,
            eps
        FROM profitandloss
        """,
        conn
    )


    results = []


    for company, group in pnl.groupby("company_id"):

        group = group.copy()

        group["year_num"] = (
            group["year"]
            .astype(str)
            .str.extract(r"(\d{4})")
            .astype(float)
        )

        group = group.sort_values("year_num")


        if len(group) < 6:
            continue


        latest = group.iloc[-1]
        old = group.iloc[-6]


        results.append({

            "company_id": company,

            "year": latest["year"],

            "revenue_cagr_5y":
                calculate_cagr(
                    old["sales"],
                    latest["sales"]
                ),

            "pat_cagr_5y":
                calculate_cagr(
                    old["net_profit"],
                    latest["net_profit"]
                ),

            "eps_cagr_5y":
                calculate_cagr(
                    old["eps"],
                    latest["eps"]
                )

        })


    growth = pd.DataFrame(results)


    growth.to_sql(
        "growth_metrics",
        conn,
        if_exists="replace",
        index=False
    )


    print(
        "Growth metrics generated:",
        len(growth),
        "companies"
    )



if __name__ == "__main__":
    main()