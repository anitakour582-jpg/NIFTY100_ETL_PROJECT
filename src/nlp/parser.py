import re
import pandas as pd
from pathlib import Path

DATA_FILE = Path("data/raw/analysis.xlsx")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_excel(DATA_FILE, header=1)

pattern = re.compile(r"(\d+)\s*Years?:?\s*([\-\d.]+)%")

parsed_rows = []
failed_rows = []

metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

for _, row in df.iterrows():

    company = row["company_id"]

    for metric in metrics:

        text = str(row[metric])

        match = pattern.search(text)

        if match:

            parsed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "period_years": int(match.group(1)),
                "value_pct": float(match.group(2))
            })

        else:

            failed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "original_text": text
            })

parsed_df = pd.DataFrame(parsed_rows)
failed_df = pd.DataFrame(failed_rows)

parsed_df.to_csv(
    OUTPUT_DIR / "analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    OUTPUT_DIR / "parse_failures.csv",
    index=False
)

print("Parsing Completed")
print("Parsed Records :", len(parsed_df))
print("Failed Records :", len(failed_df))
import sqlite3

# -------------------------------
# Cross Validation
# -------------------------------

conn = sqlite3.connect("nifty100.db")

growth = pd.read_sql("""
SELECT
company_id,
revenue_cagr_5y,
pat_cagr_5y,
eps_cagr_5y
FROM growth_metrics
""", conn)

conn.close()

comparison = []

for _, row in parsed_df.iterrows():

    company = row["company_id"]

    metric = row["metric_type"]

    parsed_value = row["value_pct"]

    db_row = growth[growth["company_id"] == company]

    if db_row.empty:
        continue

    if metric == "compounded_sales_growth":
        calculated = db_row.iloc[0]["revenue_cagr_5y"]

    elif metric == "compounded_profit_growth":
        calculated = db_row.iloc[0]["pat_cagr_5y"]

    elif metric == "stock_price_cagr":
        continue

    else:
        continue

    if pd.isna(calculated):
        continue

    difference = abs(parsed_value - calculated)

    comparison.append({
        "company_id": company,
        "metric": metric,
        "parsed_value": parsed_value,
        "calculated_value": calculated,
        "difference": difference,
        "manual_review": difference > 5
    })

comparison_df = pd.DataFrame(comparison)

comparison_df.to_csv(
    OUTPUT_DIR / "cagr_validation.csv",
    index=False
)

print()
print("Validation Completed")
print("Compared :", len(comparison_df))
print("Manual Review :", comparison_df["manual_review"].sum())