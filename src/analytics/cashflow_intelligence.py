import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
DB = "nifty100.db"

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

conn = sqlite3.connect(DB)

# -----------------------------
# Load Data
# -----------------------------
cashflow = pd.read_sql("SELECT * FROM cashflow", conn)

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

profit = pd.read_sql("SELECT * FROM profitandloss", conn)

balance = pd.read_sql("SELECT * FROM balancesheet", conn)

conn.close()

# -----------------------------
# Remove duplicate company-year
# -----------------------------
cashflow = (
    cashflow
    .sort_values("id")
    .drop_duplicates(
        subset=["company_id", "year"],
        keep="last"
    )
)

ratios = (
    ratios
    .sort_values("id")
    .drop_duplicates(
        subset=["company_id", "year"],
        keep="last"
    )
)

profit = (
    profit
    .sort_values("id")
    .drop_duplicates(
        subset=["company_id", "year"],
        keep="last"
    )
)

balance = (
    balance
    .sort_values("id")
    .drop_duplicates(
        subset=["company_id", "year"],
        keep="last"
    )
)

print("Cashflow rows :", len(cashflow))
print("Ratios rows :", len(ratios))
print("Profit rows :", len(profit))
print("Balance rows :", len(balance))
# ----------------------------------------
# Build Cash Flow Intelligence
# ----------------------------------------

results = []

companies = sorted(cashflow["company_id"].unique())

for company in companies:

    cf = cashflow[cashflow["company_id"] == company].sort_values("id")

    pr = profit[profit["company_id"] == company].sort_values("id")

    rt = ratios[ratios["company_id"] == company].sort_values("id")

    if cf.empty or pr.empty or rt.empty:
        continue

    latest_cf = cf.iloc[-1]
    latest_profit = pr.iloc[-1]
    latest_ratio = rt.iloc[-1]

    # -----------------------
    # CFO Quality
    # -----------------------

    if latest_profit["net_profit"] != 0:
        cfo_ratio = (
            latest_ratio["cash_from_operations_cr"]
            / latest_profit["net_profit"]
        )
    else:
        cfo_ratio = np.nan

    if pd.isna(cfo_ratio):
        quality = "Unknown"
    elif cfo_ratio > 1:
        quality = "High Quality"
    elif cfo_ratio >= 0.5:
        quality = "Moderate"
    else:
        quality = "Accrual Risk"

    # -----------------------
    # CapEx Intensity
    # -----------------------

    if latest_profit["sales"] != 0:

        capex_pct = abs(
            latest_cf["investing_activity"]
        ) / latest_profit["sales"] * 100

    else:
        capex_pct = np.nan

    if pd.isna(capex_pct):
        capex_label = "Unknown"
    elif capex_pct < 3:
        capex_label = "Asset Light"
    elif capex_pct <= 8:
        capex_label = "Moderate"
    else:
        capex_label = "Capital Intensive"

    # -----------------------
    # Distress Signal
    # -----------------------

    distress = (
        latest_cf["operating_activity"] < 0
        and
        latest_cf["financing_activity"] > 0
    )

    # -----------------------
    # Deleveraging
    # -----------------------

    deleveraging = False

    if len(rt) >= 2:

        prev = rt.iloc[-2]

        if (
            latest_cf["financing_activity"] < 0
            and
            latest_ratio["total_debt_cr"] < prev["total_debt_cr"]
        ):
            deleveraging = True

    results.append({

        "company_id": company,

        "cfo_quality_score": round(cfo_ratio,2)
        if not pd.isna(cfo_ratio)
        else np.nan,

        "cfo_quality_label": quality,

        "capex_intensity_pct": round(capex_pct,2)
        if not pd.isna(capex_pct)
        else np.nan,

        "capex_label": capex_label,

        "distress_flag": distress,

        "deleveraging_flag": deleveraging

    })

cashflow_df = pd.DataFrame(results)

cashflow_df.to_excel(
    OUTPUT / "cashflow_intelligence.xlsx",
    index=False
)

cashflow_df[
    cashflow_df["distress_flag"]
].to_csv(
    OUTPUT / "distress_alerts.csv",
    index=False
)

print()
print("Cash Flow Intelligence Completed")
print("Companies :", len(cashflow_df))
print("Distress Alerts :", cashflow_df["distress_flag"].sum())