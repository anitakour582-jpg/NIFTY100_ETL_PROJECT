"""
Sprint 2 - Day 11

Cash Flow KPI Functions
"""

def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow (FCF)

    Formula:
    Operating Cash Flow + Investing Cash Flow
    """

    return operating_activity + investing_activity


def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity (%)

    Formula:
    abs(Investing Activity) / Sales × 100
    """

    if sales == 0:
        return None

    return (abs(investing_activity) / sales) * 100


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion Rate (%)

    Formula:
    FCF / Operating Profit × 100
    """

    if operating_profit == 0:
        return None

    return (fcf / operating_profit) * 100


def net_cash_position(operating_activity, investing_activity, financing_activity):
    """
    Net Cash Position
    """

    return operating_activity + investing_activity + financing_activity