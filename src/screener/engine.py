"""
Sprint 3 - Day 15
Financial Screener Filter Engine
"""

import sqlite3
import pandas as pd
import yaml


DB_PATH = "nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"


def load_config():

    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)["filters"]



def normalize_year(df):

    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    return df



def load_financial_data():

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


    pnl = pd.read_sql(
        """
        SELECT
        company_id,
        year,
        sales,
        net_profit
        FROM profitandloss
        """,
        conn
    )


    sectors = pd.read_sql(
        """
        SELECT
        company_id,
        broad_sector
        FROM sectors
        """,
        conn
    )


    companies = pd.read_sql(
        """
        SELECT
        id as company_id,
        company_name
        FROM companies
        """,
        conn
    )


    ratios = normalize_year(ratios)

    market = normalize_year(market)


    # growth metrics have TTM instead of year
    growth = growth.drop(columns=["year"], errors="ignore")


    # latest P&L year
    pnl["year"] = (
        pnl["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    pnl["year"] = pd.to_numeric(
        pnl["year"],
        errors="coerce"
    )


    df = ratios.merge(
        market,
        on=["company_id","year"],
        how="left"
    )


    df = df.merge(
        pnl,
        on=["company_id","year"],
        how="left"
    )


    df = df.merge(
        growth,
        on="company_id",
        how="left"
    )


    df = df.merge(
        sectors,
        on="company_id",
        how="left"
    )


    df = df.merge(
        companies,
        on="company_id",
        how="left"
    )


    return df




def apply_filters(df, filters):

    result = df.copy()


    if filters.get("roe_min"):

        result = result[
            result["return_on_equity_pct"]
            >= filters["roe_min"]
        ]


    if filters.get("debt_to_equity_max"):

        result = result[
            (
                result["broad_sector"]
                .fillna("")
                .str.lower()
                =="financials"
            )
            |
            (
                result["debt_to_equity"]
                <= filters["debt_to_equity_max"]
            )
        ]


    if filters.get("fcf_min"):

        result = result[
            result["free_cash_flow_cr"]
            >= filters["fcf_min"]
        ]


    if filters.get("revenue_cagr_5y_min"):

        result = result[
            result["revenue_cagr_5y"]
            >= filters["revenue_cagr_5y_min"]
        ]


    if filters.get("pat_cagr_5y_min"):

        result = result[
            result["pat_cagr_5y"]
            >= filters["pat_cagr_5y_min"]
        ]


    if filters.get("opm_min"):

        result = result[
            result["operating_profit_margin_pct"]
            >= filters["opm_min"]
        ]


    if filters.get("pe_max"):

        result = result[
            result["pe_ratio"]
            <= filters["pe_max"]
        ]


    if filters.get("pb_max"):

        result = result[
            result["pb_ratio"]
            <= filters["pb_max"]
        ]


    if filters.get("dividend_yield_min"):

        result = result[
            result["dividend_yield_pct"]
            >= filters["dividend_yield_min"]
        ]


    if filters.get("icr_min"):

        result = result[
            (
                result["interest_coverage"].isna()
            )
            |
            (
                result["interest_coverage"]
                >= filters["icr_min"]
            )
        ]


    if filters.get("market_cap_min"):

        result = result[
            result["market_cap_crore"]
            >= filters["market_cap_min"]
        ]


    if filters.get("sales_min"):

        result = result[
            result["sales"]
            >= filters["sales_min"]
        ]


    result["composite_quality_score"] = (

        result["return_on_equity_pct"].fillna(0)

        +

        result["operating_profit_margin_pct"].fillna(0)

        +

        result["net_profit_margin_pct"].fillna(0)

    )


    return result.sort_values(
        "composite_quality_score",
        ascending=False
    )




if __name__ == "__main__":


    config = load_config()

    df = load_financial_data()


    print(
        "Loaded rows:",
        len(df)
    )


    output = apply_filters(
        df,
        config
    )


    print(
        "Screener Results:",
        len(output),
        "companies"
    )


    print(
        output[
            [
                "company_name",
                "composite_quality_score"
            ]
        ].head(10)
    )