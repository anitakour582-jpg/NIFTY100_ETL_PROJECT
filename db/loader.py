import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "nifty100.db"
DATA_FOLDER = Path("data/raw")

conn = sqlite3.connect(DB_PATH)

files = {
    "companies.xlsx": "companies",
    "analysis.xlsx": "analysis",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "documents.xlsx": "documents",
    "profitandloss.xlsx": "profitandloss",
    "prosandcons.xlsx": "prosandcons",
    "financial_ratios.xlsx": "financial_ratios",
    "market_cap.xlsx": "market_cap",
    "peer_groups.xlsx": "peer_groups",
    "sectors.xlsx": "sectors",
    "stock_prices.xlsx": "stock_prices"
}

core_files = {
    "companies.xlsx",
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx"
}

audit = []

for excel_file, table_name in files.items():
    print(f"Loading {excel_file}...")

    if excel_file in core_files:
        df = pd.read_excel(DATA_FOLDER / excel_file, header=1)
    else:
        df = pd.read_excel(DATA_FOLDER / excel_file)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into {table_name}")

    audit.append({
        "table": table_name,
        "rows_loaded": len(df),
        "status": "SUCCESS"
    })

pd.DataFrame(audit).to_csv("load_audit.csv", index=False)

print("\nload_audit.csv created successfully!")

conn.close()

print("\nAll tables loaded successfully!")