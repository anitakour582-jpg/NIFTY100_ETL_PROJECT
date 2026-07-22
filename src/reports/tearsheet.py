from pathlib import Path
import pandas as pd
import sqlite3

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet


# -----------------------------
# Paths
# -----------------------------

OUTPUT = Path("output")

REPORT_DIR = Path("reports/tearsheets")
REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------
# Load Data
# -----------------------------

conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql(
    """
    SELECT 
        id AS company_id,
        company_name,
        roe_percentage,
        roce_percentage
    FROM companies
    """,
    conn
)

conn.close()


cashflow = pd.read_excel(
    OUTPUT / "cashflow_intelligence.xlsx"
)


pros_cons = pd.read_csv(
    OUTPUT / "pros_cons_generated.csv"
)


capital = pd.read_csv(
    OUTPUT / "capital_allocation.csv"
)


# -----------------------------
# Create Tearsheet
# -----------------------------

def create_tearsheet(company_id):

    company_data = companies[
        companies["company_id"] == company_id
    ]

    if company_data.empty:
        raise Exception(
            "Company data not found"
        )

    company = company_data.iloc[0]


    pdf_path = (
        REPORT_DIR /
        f"{company_id}_tearsheet.pdf"
    )


    doc = SimpleDocTemplate(
        str(pdf_path)
    )


    styles = getSampleStyleSheet()

    story = []


    # Header

    story.append(
        Paragraph(
            f"{company.company_name} ({company_id})",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1,20)
    )


    # -----------------------------
    # Safe Cashflow Handling
    # -----------------------------

    cf_data = cashflow[
        cashflow.company_id == company_id
    ]


    if len(cf_data) > 0:
        cfo_quality = (
            cf_data.iloc[-1]
            ["cfo_quality_label"]
        )
    else:
        cfo_quality = "Not Available"


    # -----------------------------
    # Safe Capital Handling
    # -----------------------------

    cap_data = capital[
        capital.company_name ==
        company.company_name
    ]


    if len(cap_data) > 0:
        allocation = (
            cap_data.iloc[-1]
            ["capital_allocation"]
        )
    else:
        allocation = "Not Available"


    # -----------------------------
    # KPI Table
    # -----------------------------

    kpi_data = [

        [
            "ROE",
            f"{company.roe_percentage}%"
        ],

        [
            "ROCE",
            f"{company.roce_percentage}%"
        ],

        [
            "CFO Quality",
            str(cfo_quality)
        ],

        [
            "Capital Allocation",
            str(allocation)
        ]

    ]


    table = Table(kpi_data)


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
        Spacer(1,20)
    )


    # -----------------------------
    # Pros
    # -----------------------------

    story.append(
        Paragraph(
            "Strengths",
            styles["Heading2"]
        )
    )


    pros = pros_cons[
        (pros_cons.company_id == company_id)
        &
        (pros_cons.type == "pro")
    ]


    if len(pros) > 0:

        for text in pros.text.head(5):

            story.append(
                Paragraph(
                    "• " + str(text),
                    styles["BodyText"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No strengths available",
                styles["BodyText"]
            )
        )


    # -----------------------------
    # Cons
    # -----------------------------

    story.append(
        Paragraph(
            "Risks",
            styles["Heading2"]
        )
    )


    cons = pros_cons[
        (pros_cons.company_id == company_id)
        &
        (pros_cons.type == "con")
    ]


    if len(cons) > 0:

        for text in cons.text.head(5):

            story.append(
                Paragraph(
                    "• " + str(text),
                    styles["BodyText"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No risks available",
                styles["BodyText"]
            )
        )


    doc.build(story)


    return pdf_path



# -----------------------------
# Test 5 Companies
# -----------------------------

if __name__ == "__main__":

    test_companies = [
        "ABB",
        "TCS",
        "HDFCBANK",
        "RELIANCE",
        "SUNPHARMA"
    ]


    for c in test_companies:

        create_tearsheet(c)


    print(
        "Tearsheet generation completed"
    )

    print(
        "Generated:",
        len(test_companies),
        "PDFs"
    )