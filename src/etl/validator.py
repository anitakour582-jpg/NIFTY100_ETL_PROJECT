import pandas as pd
from pathlib import Path

DATA_FOLDER = Path("data/raw")
OUTPUT_FILE = "validation_failures.csv"

failures = []

# Expected columns for each file
EXPECTED_SCHEMA = {
    "analysis.xlsx": [
        "id","company_id","compounded_sales_growth",
        "compounded_profit_growth","stock_price_cagr","roe"
    ],
    "balancesheet.xlsx": [
        "id","company_id","year","equity_capital","reserves",
        "borrowings","other_liabilities","total_liabilities",
        "fixed_assets","cwip","investments","other_asset","total_assets"
    ],
    "cashflow.xlsx": [
        "id","company_id","year","operating_activity",
        "investing_activity","financing_activity","net_cash_flow"
    ],
    "companies.xlsx": [
        "id","company_logo","company_name","chart_link",
        "about_company","website","nse_profile","bse_profile",
        "face_value","book_value","roce_percentage","roe_percentage"
    ],
    "documents.xlsx": [
        "id","company_id","Year","Annual_Report"
    ],
    "profitandloss.xlsx": [
        "id","company_id","year","sales","expenses",
        "operating_profit","opm_percentage","other_income",
        "interest","depreciation","profit_before_tax",
        "tax_percentage","net_profit","eps","dividend_payout"
    ],
    "prosandcons.xlsx": [
        "id","company_id","pros","cons"
    ]
}

for file in DATA_FOLDER.glob("*.xlsx"):

    print(f"Checking {file.name}...")

    df = pd.read_excel(file, header=1)

    # Rule 1 Missing values
    missing = df.isnull().sum().sum()
    if missing > 0:
        failures.append([file.name,"Missing Values",missing])

    # Rule 2 Duplicate rows
    dup_rows = df.duplicated().sum()
    if dup_rows > 0:
        failures.append([file.name,"Duplicate Rows",dup_rows])

    # Rule 3 Duplicate IDs
    if "id" in df.columns:
        dup_ids = df["id"].duplicated().sum()
        if dup_ids > 0:
            failures.append([file.name,"Duplicate IDs",dup_ids])

    # Rule 4 Empty file
    if df.empty:
        failures.append([file.name,"Empty Dataset",1])

    # Rule 5 Required columns
    expected = EXPECTED_SCHEMA[file.name]

    for col in expected:
        if col not in df.columns:
            failures.append([file.name,f"Missing Column: {col}",1])

    # Rule 6 Column count
    if len(df.columns)!=len(expected):
        failures.append([file.name,"Column Count Mismatch",len(df.columns)])

    # Rule 7 Year exists
    if "year" in df.columns:
        invalid = df["year"].isnull().sum()
        if invalid>0:
            failures.append([file.name,"Missing Year",invalid])

    # Rule 8 Invalid year range
if "year" in df.columns:
    year_numeric = pd.to_numeric(df["year"], errors="coerce")
    bad = ((year_numeric < 1990) | (year_numeric > 2035)).sum()

    if bad > 0:
        failures.append([file.name, "Invalid Year", int(bad)])

    # Rule 9 Negative IDs
    if "id" in df.columns:
        neg=(df["id"]<0).sum()
        if neg>0:
            failures.append([file.name,"Negative IDs",neg])

    # Rule 10 Blank company name
    if "company_name" in df.columns:
        blank=df["company_name"].astype(str).str.strip().eq("").sum()
        if blank>0:
            failures.append([file.name,"Blank Company Name",blank])

    # Rule 11 Duplicate company_id
    if "company_id" in df.columns:
        dup=df["company_id"].duplicated().sum()
        if dup>0:
            failures.append([file.name,"Duplicate Company ID",dup])

    # Rule 12 Numeric columns
    for c in df.columns:
        if "percentage" in c.lower():
            bad=df[c].isnull().sum()
            if bad>0:
                failures.append([file.name,f"Missing {c}",bad])

    # Rule 13 All column names lowercase except Year
    for c in df.columns:
        if c!="Year":
            if c!=c.lower():
                failures.append([file.name,"Column Naming Issue",c])

    # Rule 14 Duplicate columns
    if len(df.columns)!=len(set(df.columns)):
        failures.append([file.name,"Duplicate Columns",1])

    # Rule 15 Completely empty rows
    empty_rows=df.isna().all(axis=1).sum()
    if empty_rows>0:
        failures.append([file.name,"Empty Rows",empty_rows])

    # Rule 16 File readable
    if len(df)==0:
        failures.append([file.name,"Unreadable File",1])

report=pd.DataFrame(
    failures,
    columns=["file","rule","count"]
)

report.to_csv(OUTPUT_FILE,index=False)

print("\nValidation Complete")
print(report)