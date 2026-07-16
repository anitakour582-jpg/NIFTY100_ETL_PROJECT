from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate,
    net_cash_position,
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