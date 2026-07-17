"""
Sprint 3 - Day 16
Preset Screener Testing
"""

from src.screener.engine import load_financial_data
from src.screener.presets import run_all_presets

df = load_financial_data()


# Keep latest year snapshot only
df = (
    df.sort_values("year")
    .groupby("company_id")
    .tail(1)
)


results = run_all_presets(df)


for name, output in results.items():

    print("\n-------------------------")
    print(name)
    print("-------------------------")

    print("Companies:", len(output))

    if len(output) > 0:

        print(
            output[
                [
                    "company_name",
                    "return_on_equity_pct",
                    "debt_to_equity"
                ]
            ].head()
        )