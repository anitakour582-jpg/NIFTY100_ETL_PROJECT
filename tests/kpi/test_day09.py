from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    interest_coverage_label,
    interest_coverage_warning,
    net_debt,
    asset_turnover,
)


def test_debt_to_equity():
    assert debt_to_equity(500, 1000, 500) == 500 / 1500


def test_debt_free():
    assert debt_to_equity(0, 1000, 500) == 0


def test_interest_coverage():
    assert interest_coverage_ratio(300, 100, 100) == 4.0


def test_interest_zero():
    assert interest_coverage_ratio(300, 100, 0) is None


def test_debt_free_label():
    assert interest_coverage_label(0) == "Debt Free"


def test_high_leverage():
    assert high_leverage_flag(6, "Technology") is True


def test_net_debt():
    assert net_debt(1000, 200) == 800


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0