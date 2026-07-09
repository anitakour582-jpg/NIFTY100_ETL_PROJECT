import pytest
from src.etl.normalize import normalize_year, normalize_ticker

# ==================================================
# normalize_year() Tests (20)
# ==================================================

def test_year_01():
    assert normalize_year(2024) == 2024

def test_year_02():
    assert normalize_year("2024") == 2024

def test_year_03():
    assert normalize_year("2024.0") == 2024

def test_year_04():
    assert normalize_year("FY2023") == 2023

def test_year_05():
    assert normalize_year("Year 2022") == 2022

def test_year_06():
    assert normalize_year(" 2021 ") == 2021

def test_year_07():
    assert normalize_year(None) is None

def test_year_08():
    assert normalize_year("") is None

def test_year_09():
    assert normalize_year(" ") is None

def test_year_10():
    assert normalize_year("abcd") is None

def test_year_11():
    assert normalize_year("FY-2025") == 2025

def test_year_12():
    assert normalize_year("Report2026") == 2026

def test_year_13():
    assert normalize_year(2027.0) == 2027

def test_year_14():
    assert normalize_year("Data2028File") == 2028

def test_year_15():
    assert normalize_year("Year:2029") == 2029

def test_year_16():
    assert normalize_year("2030") == 2030

def test_year_17():
    assert normalize_year("FY2031") == 2031

def test_year_18():
    assert normalize_year("2032.0") == 2032

def test_year_19():
    assert normalize_year("Annual2033Report") == 2033

def test_year_20():
    assert normalize_year("FY 2034") == 2034


# ==================================================
# normalize_ticker() Tests (20)
# ==================================================

def test_ticker_01():
    assert normalize_ticker("RELIANCE") == "RELIANCE"

def test_ticker_02():
    assert normalize_ticker("reliance") == "RELIANCE"

def test_ticker_03():
    assert normalize_ticker(" reliance ") == "RELIANCE"

def test_ticker_04():
    assert normalize_ticker("TCS") == "TCS"

def test_ticker_05():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_06():
    assert normalize_ticker(" infosys ") == "INFOSYS"

def test_ticker_07():
    assert normalize_ticker(None) is None

def test_ticker_08():
    assert normalize_ticker("") is None

def test_ticker_09():
    assert normalize_ticker(" ") is None

def test_ticker_10():
    assert normalize_ticker("HDFCBANK") == "HDFCBANK"

def test_ticker_11():
    assert normalize_ticker("hdfcbank") == "HDFCBANK"

def test_ticker_12():
    assert normalize_ticker("ITC") == "ITC"

def test_ticker_13():
    assert normalize_ticker("itc") == "ITC"

def test_ticker_14():
    assert normalize_ticker("SBIN") == "SBIN"

def test_ticker_15():
    assert normalize_ticker("sbin") == "SBIN"

def test_ticker_16():
    assert normalize_ticker(" LT ") == "LT"

def test_ticker_17():
    assert normalize_ticker("axisbank") == "AXISBANK"

def test_ticker_18():
    assert normalize_ticker("maruti") == "MARUTI"

def test_ticker_19():
    assert normalize_ticker("asianpaint") == "ASIANPAINT"

def test_ticker_20():
    assert normalize_ticker("nestleind") == "NESTLEIND"