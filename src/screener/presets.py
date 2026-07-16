"""
Sprint 3 - Day 16

Preset Screener Engine
"""

import pandas as pd


def quality_compounder(df):
    """
    Quality Compounder
    ROE > 15%
    D/E < 1
    FCF > 0
    Revenue CAGR 5Y > 10%
    """
    return df[
        (df["return_on_equity_pct"] > 15)
        &
        (df["debt_to_equity"] < 1)
        &
        (df["free_cash_flow_cr"] > 0)
        &
        (df["revenue_cagr_5y"] > 10)
    ]


def value_pick(df):
    """
    Value Pick
    PE < 35
    PB < 6
    D/E < 2
    Dividend Yield > 0.3%
    """
    return df[
        (df["pe_ratio"] < 35)
        &
        (df["pb_ratio"] < 6)
        &
        (df["debt_to_equity"] < 2)
        &
        (df["dividend_yield_pct"] > 0.3)
    ]


def growth_accelerator(df):
    """
    Growth Accelerator
    PAT CAGR > 15%
    Revenue CAGR > 10%
    D/E < 2
    """
    return df[
        (df["pat_cagr_5y"] > 15)
        &
        (df["revenue_cagr_5y"] > 10)
        &
        (df["debt_to_equity"] < 2)
    ]


def dividend_champion(df):
    """
    Dividend Champion
    Dividend Yield > 2%
    Dividend Payout < 80%
    FCF > 0
    """
    return df[
        (df["dividend_yield_pct"] > 2)
        &
        (df["dividend_payout_ratio_pct"] < 80)
        &
        (df["free_cash_flow_cr"] > 0)
    ]


def debt_free_blue_chip(df):
    """
    Debt-Free Blue Chip
    D/E <= 0.01
    ROE > 12%
    Sales > 5000 Crore
    """
    return df[
        (df["debt_to_equity"] <= 0.01)
        &
        (df["return_on_equity_pct"] > 12)
        &
        (df["sales"] > 5000)
    ]


def turnaround_watch(df):
    """
    Turnaround Watch
    Revenue CAGR > 10%
    Positive FCF
    """
    return df[
        (df["revenue_cagr_5y"] > 10)
        &
        (df["free_cash_flow_cr"] > 0)
    ]


PRESETS = {
    "Quality Compounder": quality_compounder,
    "Value Pick": value_pick,
    "Growth Accelerator": growth_accelerator,
    "Dividend Champion": dividend_champion,
    "Debt-Free Blue Chip": debt_free_blue_chip,
    "Turnaround Watch": turnaround_watch,
}


def run_all_presets(df):
    results = {}

    for name, function in PRESETS.items():
        results[name] = function(df)

    return results