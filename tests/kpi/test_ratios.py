from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)

def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20.0

def test_net_profit_margin_zero_sales():
    assert net_profit_margin(200, 0) is None

def test_operating_profit_margin():
    assert operating_profit_margin(300, 1000) == 30.0

def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(300, 0) is None

def test_return_on_equity():
    assert round(return_on_equity(500, 1000, 500), 2) == 33.33

def test_return_on_equity_negative_equity():
    assert return_on_equity(500, -1000, 500) is None

def test_return_on_capital_employed():
    assert round(return_on_capital_employed(600, 1000, 500, 500), 2) == 30.00

def test_return_on_assets():
    assert return_on_assets(400, 2000) == 20.0