import re


def normalize_year(year):
    """
    Normalize year values to a 4-digit integer.
    """

    if year is None:
        return None

    year = str(year).strip()

    if year == "":
        return None

    # Handle values like 2024.0
    if year.endswith(".0"):
        year = year[:-2]

    # Extract a 4-digit year
    match = re.search(r"\d{4}", year)

    if match:
        return int(match.group())

    return None


def normalize_ticker(ticker):
    """
    Normalize stock ticker symbols.
    """

    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    if ticker == "":
        return None

    return ticker


if __name__ == "__main__":
    print(normalize_year("2024"))
    print(normalize_year("FY2023"))
    print(normalize_ticker(" reliance "))