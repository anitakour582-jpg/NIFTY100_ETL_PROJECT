"""
Financial Ratio Engine

Sprint 2 – Days 08 & 09

Profitability, Leverage and Efficiency Ratio Functions
"""


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)

    Formula:
    (Net Profit / Sales) * 100
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin (%)

    Formula:
    (Operating Profit / Sales) * 100
    """

    if sales == 0:
        return None

    return (operating_profit / sales) * 100


def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)

    Formula:
    Net Profit / (Equity Capital + Reserves) * 100
    """

    shareholders_equity = equity_capital + reserves

    if shareholders_equity <= 0:
        return None

    return (net_profit / shareholders_equity) * 100


def return_on_capital_employed(ebit, equity_capital, reserves, borrowings):
    """
    Return on Capital Employed (ROCE)

    Formula:
    EBIT / (Equity + Reserves + Borrowings) * 100
    """

    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    return (ebit / capital_employed) * 100


def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (ROA)

    Formula:
    Net Profit / Total Assets * 100
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


# -------------------------
# Day 09 Functions
# -------------------------

def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt to Equity Ratio

    Formula:
    Borrowings / (Equity + Reserves)

    Returns 0 for debt-free companies.
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return borrowings / equity


def high_leverage_flag(de_ratio, sector):
    """
    High leverage flag.
    """

    if de_ratio is None:
        return False

    return de_ratio > 5 and sector.lower() != "financials"


def interest_coverage_ratio(operating_profit, other_income, interest):
    """
    Interest Coverage Ratio (ICR)

    Formula:
    (Operating Profit + Other Income) / Interest
    """

    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def interest_coverage_label(interest):
    """
    Debt Free label.
    """

    if interest == 0:
        return "Debt Free"

    return ""


def interest_coverage_warning(icr):
    """
    Warning when ICR < 1.5
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    """
    Net Debt

    Formula:
    Borrowings - Investments
    """

    return borrowings - investments


def asset_turnover(sales, total_assets):
    """
    Asset Turnover Ratio

    Formula:
    Sales / Total Assets
    """

    if total_assets == 0:
        return None

    return sales / total_assets