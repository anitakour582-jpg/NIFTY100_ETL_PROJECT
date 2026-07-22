from pathlib import Path
import pandas as pd
import sqlite3

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet


# Paths
REPORT_DIR = Path("reports/portfolio")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PDF_PATH = REPORT_DIR / "portfolio_summary.pdf"


# Database
conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name,
        roe_percentage,
        roce_percentage
    FROM companies
    ORDER BY company_name
    """,
    conn
)

conn.close()


# Load outputs
cashflow = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)


capital = pd.read_csv(
    "output/capital_allocation.csv"
)


# Create PDF

doc = SimpleDocTemplate(
    str(PDF_PATH)
)

styles = getSampleStyleSheet()

story = []


for _, company in companies.iterrows():

    company_id = company["company_id"]

    story.append(
        Paragraph(
            f"{company['company_name']} ({company_id})",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1,20)
    )


    cf = cashflow[
        cashflow["company_id"] == company_id
    ]


    if not cf.empty:

        latest = cf.iloc[-1]

        cfo_quality = latest.get(
            "cfo_quality_label",
            "N/A"
        )

        distress = latest.get(
            "distress_flag",
            False
        )

    else:

        cfo_quality = "N/A"
        distress = False



    table = Table(
        [
            ["Metric","Value"],

            [
                "ROE",
                f"{company['roe_percentage']}%"
            ],

            [
                "ROCE",
                f"{company['roce_percentage']}%"
            ],

            [
                "CFO Quality",
                str(cfo_quality)
            ],

            [
                "Distress Signal",
                str(distress)
            ]
        ]
    )


    table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    None
                )
            ]
        )
    )


    story.append(table)

    story.append(
        PageBreak()
    )


doc.build(story)


print("Portfolio Summary PDF Generated")
print(PDF_PATH)
print("Companies:", len(companies))