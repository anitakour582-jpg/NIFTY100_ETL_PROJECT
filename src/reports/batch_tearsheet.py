from pathlib import Path
import sqlite3
import pandas as pd

from tearsheet import create_tearsheet


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
# Load Companies
# -----------------------------

conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql(
    """
    SELECT id AS company_id
    FROM companies
    """,
    conn
)

conn.close()


# -----------------------------
# Generate All Tearsheets
# -----------------------------

generated = []
failed = []


for company_id in companies["company_id"]:

    try:

        pdf = create_tearsheet(company_id)

        generated.append(company_id)

        print(
            "Generated:",
            company_id
        )

    except Exception as e:

        failed.append(
            {
                "company_id": company_id,
                "error": str(e)
            }
        )


# -----------------------------
# Save Failures
# -----------------------------

if failed:

    pd.DataFrame(failed).to_csv(
        OUTPUT / "skipped_tearsheets.csv",
        index=False
    )


print()
print("-----------------------------")
print("Batch Generation Completed")
print("-----------------------------")
print(
    "Generated PDFs:",
    len(generated)
)

print(
    "Failed:",
    len(failed)
)