from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate,
    net_cash_position,
    cfo_quality_score,
    capital_allocation_pattern,
)


def test_free_cash_flow():
    assert free_cash_flow(500, -200) == 300


def test_capex_intensity():
    assert capex_intensity(-200, 1000) == 20.0


def test_capex_zero_sales():
    assert capex_intensity(-200, 0) is None


def test_fcf_conversion():
    assert fcf_conversion_rate(300, 300) == 100.0


def test_fcf_conversion_zero_profit():
    assert fcf_conversion_rate(300, 0) is None


def test_net_cash_position():
    assert net_cash_position(500, -200, -100) == 200


def test_cfo_quality_high():
    ratio, label = cfo_quality_score(500, 400)
    assert round(ratio, 2) == 1.25
    assert label == "High Quality"


def test_cfo_quality_moderate():
    ratio, label = cfo_quality_score(300, 400)
    assert round(ratio, 2) == 0.75
    assert label == "Moderate"


def test_cfo_quality_low():
    ratio, label = cfo_quality_score(100, 400)
    assert round(ratio, 2) == 0.25
    assert label == "Accrual Risk"


def test_cfo_quality_no_pat():
    ratio, label = cfo_quality_score(100, 0)
    assert ratio is None
    assert label == "NO_PAT"


def test_capital_allocation_reinvestor():
    assert capital_allocation_pattern(500, -200, -100) == "Reinvestor"


def test_capital_allocation_shareholder_returns():
    assert (
        capital_allocation_pattern(500, -200, -100, "High Quality")
        == "Shareholder Returns"
    )