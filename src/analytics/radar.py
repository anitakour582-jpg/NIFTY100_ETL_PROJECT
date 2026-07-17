"""
Sprint 3 - Day 19

Peer Comparison Radar Charts
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from screener.engine import load_financial_data

OUTPUT_DIR = "reports/radar_charts"


# ----------------------------------------
# Prepare Radar Data
# ----------------------------------------

def prepare_radar_data():

    df = load_financial_data()

    return df



# ----------------------------------------
# Normalize Metric
# ----------------------------------------

def normalize(series):

    minimum = series.min()
    maximum = series.max()

    if minimum == maximum:
        return pd.Series(
            50,
            index=series.index
        )

    return (
        (series - minimum)
        /
        (maximum - minimum)
        *
        100
    )



# ----------------------------------------
# Create Radar Chart
# ----------------------------------------

def create_radar_chart(company_row, peer_average):


    metrics = [

        "ROE",

        "NPM",

        "D/E",

        "FCF",

        "PAT CAGR",

        "Revenue CAGR",

        "EPS CAGR",

        "Composite Score"

    ]


    company_values = [

        company_row.get(
            "return_on_equity_pct",
            0
        ),

        company_row.get(
            "net_profit_margin_pct",
            0
        ),

        company_row.get(
            "debt_to_equity",
            0
        ),

        company_row.get(
            "free_cash_flow_cr",
            0
        ),

        company_row.get(
            "pat_cagr_5y",
            0
        ),

        company_row.get(
            "revenue_cagr_5y",
            0
        ),

        company_row.get(
            "eps_cagr_5y",
            0
        ),

        company_row.get(
            "composite_quality_score",
            0
        )

    ]


    peer_values = peer_average



    angles = np.linspace(
        0,
        2*np.pi,
        len(metrics),
        endpoint=False
    )


    company_values += company_values[:1]

    peer_values += peer_values[:1]

    angles = np.append(
        angles,
        angles[0]
    )


    fig = plt.figure(
        figsize=(7,7)
    )


    ax = fig.add_subplot(
        111,
        polar=True
    )


    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label="Company"
    )


    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )


    ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )


    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        metrics,
        fontsize=9
    )


    ax.set_title(
        company_row["company_name"],
        pad=20
    )


    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.2,1.1)
    )


    filename = (

    str(company_row["company_id"])

    +

    "_"

    +

    str(company_row["year"])

    +

    "_radar.png"

)


    path = os.path.join(
        OUTPUT_DIR,
        filename
    )


    plt.savefig(
        path,
        bbox_inches="tight"
    )


    plt.close()


    print(
        "Saved:",
        path
    )



# ----------------------------------------
# Generate Charts
# ----------------------------------------

def generate_all_radar_charts():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    df = prepare_radar_data()


    # generate first 10 companies
    # for testing

    for _, row in df.drop_duplicates("company_id").head(10).iterrows():

        peer_average = [

            50,
            50,
            50,
            50,
            50,
            50,
            50,
            50

        ]


        create_radar_chart(
            row,
            peer_average
        )



# ----------------------------------------
# Main
# ----------------------------------------

if __name__ == "__main__":

    generate_all_radar_charts()