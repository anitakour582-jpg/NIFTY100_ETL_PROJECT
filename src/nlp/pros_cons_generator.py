import sqlite3
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# -------------------------------
# Load Data
# -------------------------------
conn = sqlite3.connect("nifty100.db")

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
growth = pd.read_sql("SELECT * FROM growth_metrics", conn)
pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)

conn.close()

# Latest ratios per company
latest_ratios = (
    ratios.sort_values("id")
    .groupby("company_id")
    .tail(1)
    .set_index("company_id")
)

# Latest growth per company
latest_growth = growth.set_index("company_id")

# Historical data
pnl_hist = pnl.sort_values(["company_id", "id"])
ratio_hist = ratios.sort_values(["company_id", "id"])
bs_hist = bs.sort_values(["company_id", "id"])

pros_cons = []

def add_record(company, typ, rule_id, text, confidence):
    if confidence > 60:
        pros_cons.append({
            "company_id": company,
            "type": typ,
            "rule_id": rule_id,
            "text": text,
            "confidence_pct": confidence
        })

companies = sorted(set(latest_ratios.index) | set(latest_growth.index))

for company in companies:

    if company not in latest_ratios.index:
        continue

    r = latest_ratios.loc[company]

    g = latest_growth.loc[company] if company in latest_growth.index else pd.Series(dtype=float)

    pnl_c = pnl_hist[pnl_hist["company_id"] == company]
    ratio_c = ratio_hist[ratio_hist["company_id"] == company]
    bs_c = bs_hist[bs_hist["company_id"] == company]

    # ---------------- PRO RULES ----------------

    # P1 ROE > 20%
    if r["return_on_equity_pct"] > 20:
        add_record(company, "pro", "P1",
                   "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.", 90)

    # P2 FCF positive for last 5 records
    fcf_last5 = ratio_c.tail(5)["free_cash_flow_cr"]
    if len(fcf_last5) == 5 and (fcf_last5 > 0).all():
        add_record(company, "pro", "P2",
                   "Strong free cash flow generation over 5 years signals healthy business fundamentals.", 88)

    # P3 Debt free
    if r["debt_to_equity"] == 0:
        add_record(company, "pro", "P3",
                   "Debt-free balance sheet provides financial flexibility and eliminates interest burden.", 95)

    # P4 Revenue CAGR > 15%
    if pd.notna(g.get("revenue_cagr_5y")) and g["revenue_cagr_5y"] > 15:
        add_record(company, "pro", "P4",
                   "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum.", 85)

    # P5 OPM > 25%
    if r["operating_profit_margin_pct"] > 25:
        add_record(company, "pro", "P5",
                   "Operating profit margin above 25% indicates strong pricing power and cost discipline.", 82)

    # P6 PAT CAGR > 20%
    if pd.notna(g.get("pat_cagr_5y")) and g["pat_cagr_5y"] > 20:
        add_record(company, "pro", "P6",
                   "Net profit compounding at above 20% over 5 years creates significant shareholder value.", 90)

    # P7 Interest coverage > 10 or debt free
    if r["debt_to_equity"] == 0 or r["interest_coverage"] > 10:
        add_record(company, "pro", "P7",
                   "Very high interest coverage ratio reflects negligible financial stress from debt servicing.", 80)

    # P8 Dividend payout between 20 and 80 with positive FCF
    if 20 <= r["dividend_payout_ratio_pct"] <= 80 and r["free_cash_flow_cr"] > 0:
        add_record(company, "pro", "P8",
                   "Sustainable dividend payout backed by positive free cash flow.", 72)

    # P9 EPS CAGR > 15%
    if pd.notna(g.get("eps_cagr_5y")) and g["eps_cagr_5y"] > 15:
        add_record(company, "pro", "P9",
                   "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding.", 85)

    # P10 ROE improving for 3 consecutive years
    roe_last3 = ratio_c.tail(3)["return_on_equity_pct"].tolist()
    if len(roe_last3) == 3 and roe_last3[0] < roe_last3[1] < roe_last3[2]:
        add_record(company, "pro", "P10",
                   "Return on equity improving for 3 consecutive years shows strengthening business quality.", 78)

    # P11 Operating leverage
    if pd.notna(g.get("revenue_cagr_5y")) and pd.notna(g.get("pat_cagr_5y")) and g["pat_cagr_5y"] > g["revenue_cagr_5y"]:
        add_record(company, "pro", "P11",
                   "Revenue growing slower than profits shows improving operating leverage and scale benefits.", 76)

    # P12 Assets growing while borrowings declining
    assets_last3 = bs_c.tail(3)["total_assets"].tolist()
    debt_last3 = bs_c.tail(3)["borrowings"].tolist()
    if len(assets_last3) == 3 and len(debt_last3) == 3:
        if assets_last3[0] < assets_last3[1] < assets_last3[2] and debt_last3[0] >= debt_last3[1] >= debt_last3[2]:
            add_record(company, "pro", "P12",
                       "Growing asset base funded by internal accruals reflects self-sustaining growth.", 74)

    # ---------------- CON RULES ----------------

    # C1 High debt
    if r["debt_to_equity"] > 2:
        add_record(company, "con", "C1",
                   f"Debt-to-equity ratio of {r['debt_to_equity']:.2f} is elevated and warrants monitoring.", 90)

    # C2 FCF negative for 3 consecutive years
    fcf_last3 = ratio_c.tail(3)["free_cash_flow_cr"]
    if len(fcf_last3) == 3 and (fcf_last3 < 0).all():
        add_record(company, "con", "C2",
                   "Free cash flow negative for 3 consecutive years raises concern about cash generation quality.", 88)

    # C3 OPM declining for 3 consecutive years
    opm_last3 = ratio_c.tail(3)["operating_profit_margin_pct"].tolist()
    if len(opm_last3) == 3 and opm_last3[0] > opm_last3[1] > opm_last3[2]:
        add_record(company, "con", "C3",
                   "Operating margins declining for 3 consecutive years suggest pricing or cost pressure.", 82)

    # C4 Net loss in latest year
    pnl_latest = pnl_c.tail(1)
    if not pnl_latest.empty and pnl_latest.iloc[0]["net_profit"] < 0:
        add_record(company, "con", "C4",
                   "Company reported a net loss in the most recent financial year.", 95)

    # C5 Revenue declining for 2 consecutive years
    sales_last3 = pnl_c.tail(3)["sales"].tolist()
    if len(sales_last3) == 3 and sales_last3[0] > sales_last3[1] > sales_last3[2]:
        add_record(company, "con", "C5",
                   "Revenue contraction over consecutive years indicates demand weakness or market share loss.", 80)

    # C6 Interest coverage < 1.5
    if r["interest_coverage"] < 1.5:
        add_record(company, "con", "C6",
                   "Interest coverage ratio below 1.5x indicates risk in meeting debt obligations.", 92)

    # C7 Dividend payout > 100%
    if r["dividend_payout_ratio_pct"] > 100:
        add_record(company, "con", "C7",
                   "Dividend payout ratio above 100% may be unsustainable.", 85)

    # C8 D/E rising for 3 consecutive years
    de_last3 = ratio_c.tail(3)["debt_to_equity"].tolist()
    if len(de_last3) == 3 and de_last3[0] < de_last3[1] < de_last3[2]:
        add_record(company, "con", "C8",
                   "Rising debt-to-equity ratio over 3 years suggests increasing financial leverage risk.", 78)

    # C9 EPS declining for 3 consecutive years
    eps_last3 = ratio_c.tail(3)["earnings_per_share"].tolist()
    if len(eps_last3) == 3 and eps_last3[0] > eps_last3[1] > eps_last3[2]:
        add_record(company, "con", "C9",
                   "Earnings per share declining for 3 consecutive years reflects deteriorating profitability.", 80)

    # C10 ROCE proxy using ROE < 10%
    if r["return_on_equity_pct"] < 10:
        add_record(company, "con", "C10",
                   "Return on equity below 10% suggests the business is generating weak shareholder returns.", 75)

    # C11 Net debt > 3x CFO proxy
    if r["cash_from_operations_cr"] > 0 and r["total_debt_cr"] / r["cash_from_operations_cr"] > 3:
        add_record(company, "con", "C11",
                   "Total debt exceeding 3 times operating cash flow limits financial flexibility.", 84)

    # C12 Revenue CAGR < 5%
    if pd.notna(g.get("revenue_cagr_5y")) and g["revenue_cagr_5y"] < 5:
        add_record(company, "con", "C12",
                   "Revenue growing below 5% CAGR over 5 years suggests limited business momentum.", 82)

# -------------------------------
# Create DataFrame
# -------------------------------
pros_cons_df = pd.DataFrame(pros_cons)

# Ensure every company has at least one pro and one con
summary = pros_cons_df.groupby(["company_id", "type"]).size().unstack(fill_value=0)

for company in companies:
    if company not in summary.index or summary.loc[company].get("pro", 0) == 0:
        pros_cons_df = pd.concat([
            pros_cons_df,
            pd.DataFrame([{
                "company_id": company,
                "type": "pro",
                "rule_id": "P0",
                "text": "Business maintains a measurable operating and financial track record.",
                "confidence_pct": 61
            }])
        ], ignore_index=True)

    if company not in summary.index or summary.loc[company].get("con", 0) == 0:
        pros_cons_df = pd.concat([
            pros_cons_df,
            pd.DataFrame([{
                "company_id": company,
                "type": "con",
                "rule_id": "C0",
                "text": "Future performance remains subject to industry cycles and execution risks.",
                "confidence_pct": 61
            }])
        ], ignore_index=True)

# Save output
pros_cons_df.to_csv(OUTPUT_DIR / "pros_cons_generated.csv", index=False)

final_summary = pros_cons_df.groupby(["company_id", "type"]).size().unstack(fill_value=0)

print("Pros/Cons generation completed")
print("Total records:", len(pros_cons_df))
print("Companies with at least one pro:", (final_summary["pro"] >= 1).sum())
print("Companies with at least one con:", (final_summary["con"] >= 1).sum())