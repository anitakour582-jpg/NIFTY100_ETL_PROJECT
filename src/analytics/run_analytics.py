"""
Sprint 2 Analytics Runner

Generates Ratio + Cashflow Analytics Reports
"""

import sqlite3
import pandas as pd

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    debt_to_equity,
    asset_turnover,
    net_debt
)

from cashflow_kpis import (
    free_cash_flow,
    net_cash_position,
    cfo_quality_score,
    capital_allocation_pattern
)


DB_PATH = "nifty100.db"


def main():

    conn = sqlite3.connect(DB_PATH)

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    companies = pd.read_sql(
        "SELECT id, company_name FROM companies",
        conn
    )


    # Merge financial tables

    df = pnl.merge(
        bs,
        on=["company_id", "year"],
        suffixes=("_pnl", "_bs")
    )

    df = df.merge(
        cashflow,
        on=["company_id", "year"],
        how="left"
    )

    df = df.merge(
        companies,
        left_on="company_id",
        right_on="id"
    )


    ratio_results = []

    cashflow_results = []


    for _, row in df.iterrows():

        ratio_results.append({

            "company_name": row["company_name"],
            "year": row["year"],

            "net_profit_margin":
                net_profit_margin(
                    row["net_profit"],
                    row["sales"]
                ),

            "operating_profit_margin":
                operating_profit_margin(
                    row["operating_profit"],
                    row["sales"]
                ),

            "ROE":
                return_on_equity(
                    row["net_profit"],
                    row["equity_capital"],
                    row["reserves"]
                ),

            "ROCE":
                return_on_capital_employed(
                    row["operating_profit"],
                    row["equity_capital"],
                    row["reserves"],
                    row["borrowings"]
                ),

            "debt_to_equity":
                debt_to_equity(
                    row["borrowings"],
                    row["equity_capital"],
                    row["reserves"]
                ),

            "asset_turnover":
                asset_turnover(
                    row["sales"],
                    row["total_assets"]
                ),

            "net_debt":
                net_debt(
                    row["borrowings"],
                    row["investments"]
                )
        })


        cfo_ratio, cfo_label = cfo_quality_score(
            row["operating_activity"],
            row["net_profit"]
        )


        cashflow_results.append({

            "company_name": row["company_name"],
            "year": row["year"],

            "free_cash_flow":
                free_cash_flow(
                    row["operating_activity"],
                    row["investing_activity"]
                ),

            "net_cash_position":
                net_cash_position(
                    row["operating_activity"],
                    row["investing_activity"],
                    row["financing_activity"]
                ),

            "cfo_quality_ratio": cfo_ratio,

            "cfo_quality":
                cfo_label,

            "capital_allocation":
                capital_allocation_pattern(
                    row["operating_activity"],
                    row["investing_activity"],
                    row["financing_activity"],
                    cfo_label
                )
        })


    ratio_report = pd.DataFrame(ratio_results)

    cashflow_report = pd.DataFrame(cashflow_results)


    ratio_report.to_csv(
        "output/ratio_analysis.csv",
        index=False
    )


    cashflow_report.to_csv(
        "output/capital_allocation.csv",
        index=False
    )


    print("Ratio report generated:", len(ratio_report), "rows")
    print("Cashflow report generated:", len(cashflow_report), "rows")


if __name__ == "__main__":
    main()