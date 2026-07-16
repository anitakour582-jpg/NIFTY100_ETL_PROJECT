import pandas as pd


INPUT = "output/final_company_scores.csv"
OUTPUT = "output/final_company_scores_clean.csv"


df = pd.read_csv(INPUT)
# Clean company names
# Clean company names
df["company_name"] = (
    df["company_name"]
    .str.split("\n")
    .str[0]
    .str.strip()
)


# Convert year into sortable date
df["year_sort"] = pd.to_datetime(
    df["year"],
    format="%b %Y",
    errors="coerce"
)


# Keep latest year for each company
clean = (
    df.sort_values("year_sort")
      .groupby("company_name")
      .tail(1)
)


# Remove helper column
clean = clean.drop(columns=["year_sort"])


clean.to_csv(
    OUTPUT,
    index=False
)


print(
    "Clean company snapshot generated:",
    len(clean),
    "companies"
)