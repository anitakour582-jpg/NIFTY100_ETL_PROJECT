"""
Sprint 2 - Day 10

CAGR Engine
"""

def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR (Compound Annual Growth Rate)

    Formula:
    CAGR = ((Ending / Beginning) ** (1 / Years) - 1) * 100
    """

    # Edge Case 1
    if years <= 0:
        return None, "INVALID_YEARS"

    # Edge Case 2
    if start_value == 0:
        return None, "ZERO_BASE"

    # Edge Case 3
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # Edge Case 4
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # Edge Case 5
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    # Normal CAGR
    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return cagr, "NORMAL"