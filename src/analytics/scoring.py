"""
Sprint 2 - Day 12

Investment Scoring Engine
"""

import pandas as pd


def quality_score(row):

    score = 0

    # Profitability
    if row["ROE"] > 15:
        score += 20

    if row["ROCE"] > 15:
        score += 20

    if row["net_profit_margin"] > 10:
        score += 10


    # Debt Risk
    if row["debt_to_equity"] <= 1:
        score += 15

    elif row["debt_to_equity"] > 3:
        score -= 10


    # Cash Flow
    if row["free_cash_flow"] > 0:
        score += 15

    if row["cfo_quality"] == "High Quality":
        score += 10


    # Capital Allocation
    if row["capital_allocation"] == "Shareholder Returns":
        score += 10


    return score


def rating(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    else:
        return "Risky"



def main():

    ratios = pd.read_csv(
        "output/ratio_analysis.csv"
    )

    cashflow = pd.read_csv(
        "output/capital_allocation.csv"
    )


    df = ratios.merge(
        cashflow,
        on=[
            "company_name",
            "year"
        ],
        how="inner"
    )


    df["score"] = df.apply(
        quality_score,
        axis=1
    )


    df["rating"] = df["score"].apply(
        rating
    )


    df.to_csv(
        "output/final_company_scores.csv",
        index=False
    )


    print(
        "Investment scores generated:",
        len(df),
        "rows"
    )


if __name__ == "__main__":
    main()