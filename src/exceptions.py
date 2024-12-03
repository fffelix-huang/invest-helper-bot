VALID_PERIODS = {
    "1d": "1d",
    "5d": "5d",
    "1m": "1mo",
    "3m": "3mo",
    "6m": "6mo",
    "1y": "1y",
    "2y": "2y",
    "5y": "5y",
    "10y": "10y",
    "max": "max"
}

class PeriodNotFoundError(Exception):
    def __init__(self, period: str):
        valid_periods_str = ", ".join(VALID_PERIODS.keys())
        super().__init__(f"Period should be one of {valid_periods_str}, but found {period} instead.")

class StockNotFoundError(Exception):
    def __init__(self, stock: str):
        super().__init__(f"Symbol {stock} not found.")
