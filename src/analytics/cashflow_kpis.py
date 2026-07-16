"""
Sprint 2 - Day 11

Cash Flow KPI Functions
"""


def free_cash_flow(operating_activity, investing_activity):
    return operating_activity + investing_activity


def capex_intensity(investing_activity, sales):
    if sales == 0:
        return None
    return (abs(investing_activity) / sales) * 100


def fcf_conversion_rate(fcf, operating_profit):
    if operating_profit == 0:
        return None
    return (fcf / operating_profit) * 100


def net_cash_position(operating_activity, investing_activity, financing_activity):
    return (
        operating_activity
        + investing_activity
        + financing_activity
    )


def cfo_quality_score(cfo, pat):
    if pat == 0:
        return None, "NO_PAT"

    ratio = cfo / pat

    if ratio > 1:
        label = "High Quality"
    elif ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return ratio, label


def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity,
    cfo_quality=None,
):
    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):
        if cfo_quality == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Other"