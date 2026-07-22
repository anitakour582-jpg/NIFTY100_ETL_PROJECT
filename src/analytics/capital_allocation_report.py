import pandas as pd
import sqlite3
from pathlib import Path

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)


# -----------------------------
# Load Files
# -----------------------------

capital = pd.read_csv(
    OUTPUT / "capital_allocation.csv"
)

cashflow = pd.read_excel(
    OUTPUT / "cashflow_intelligence.xlsx"
)


# -----------------------------
# Company Mapping
# -----------------------------

conn = sqlite3.connect("nifty100.db")

company_map = pd.read_sql("""
SELECT 
    id AS company_id,
    company_name
FROM companies
""", conn)

conn.close()


# -----------------------------
# Add company_id to capital data
# -----------------------------

capital = capital.merge(
    company_map,
    on="company_name",
    how="left"
)


# -----------------------------
# Latest Year Allocation
# -----------------------------

capital_latest = (
    capital
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)


# -----------------------------
# Capital Allocation Summary
# -----------------------------

summary = (
    capital_latest["capital_allocation"]
    .value_counts()
    .reset_index()
)

summary.columns = [
    "capital_allocation",
    "company_count"
]


summary.to_csv(
    OUTPUT / "capital_allocation_summary.csv",
    index=False
)


# -----------------------------
# Merge with Cashflow Intelligence
# -----------------------------

cashflow = cashflow.merge(
    capital_latest[
        [
            "company_id",
            "capital_allocation"
        ]
    ],
    on="company_id",
    how="left"
)


cashflow.rename(
    columns={
        "capital_allocation":
        "capital_allocation_label"
    },
    inplace=True
)


cashflow.to_excel(
    OUTPUT / "cashflow_intelligence.xlsx",
    index=False
)


# -----------------------------
# Pattern Changes
# -----------------------------

pattern_changes = []

for company in capital["company_id"].dropna().unique():

    temp = (
        capital[
            capital["company_id"] == company
        ]
        .sort_values("year")
    )

    patterns = (
        temp["capital_allocation"]
        .dropna()
        .unique()
        .tolist()
    )


    if len(patterns) > 1:

        pattern_changes.append({

            "company_id": company,

            "company_name":
            temp["company_name"].iloc[0],

            "pattern_changes":
            " -> ".join(patterns)

        })


pattern_changes_df = pd.DataFrame(
    pattern_changes
)


pattern_changes_df.to_csv(
    OUTPUT / "pattern_changes.csv",
    index=False
)


# -----------------------------
# Validation
# -----------------------------

print()
print("Capital Allocation Report Completed")
print("----------------------------------")
print("Companies :", cashflow["company_id"].nunique())
print(
    "Pattern Changes :",
    len(pattern_changes_df)
)
print(
    "Distribution Categories :",
    len(summary)
)

print()
print("Generated Files:")
print("✓ capital_allocation_summary.csv")
print("✓ pattern_changes.csv")
print("✓ cashflow_intelligence.xlsx updated")