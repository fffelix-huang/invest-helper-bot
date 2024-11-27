import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import io
import datetime
from skfolio.preprocessing import prices_to_returns
from metrics import *

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

def prices_to_cumulative_returns(prices: pd.DataFrame):
    returns = prices_to_returns(prices)
    return (returns + 1.0).cumprod() - 1.0

def plot_stock_compare_with_spy(
    symbol: str,
    period: str = None,
    start_date: str = None,
    end_date: str = None,
) -> io.BytesIO:
    period = period.lower()

    if period not in VALID_PERIODS:
        raise PeriodNotFoundError(period)

    yf_period = VALID_PERIODS[period]

    try:
        if period is not None:
            stock_data = yf.download(symbol, period=yf_period, interval="1d")
        else:
            stock_data = yf.download(symbol, start=start_date, end=end_date, interval="1d")

        if stock_data.empty:
            raise StockNotFoundError(symbol)

        symbol = symbol.upper()
        if start_date is None or end_date is None:
            start_date = stock_data.index[0]
            end_date = stock_data.index[-1]
        SPY = yf.download("SPY", start=start_date, end=end_date, interval="1d")

        stock_returns = prices_to_returns(stock_data["Close"])
        spy_returns = prices_to_returns(SPY["Close"])

        gs = GridSpec(2, 2, height_ratios=[1, 1])
        fig = plt.figure(figsize=(12, 8))

        # Write summary
        columns = ["Metric", symbol, "SPY"]
        rows = [
            ["CAGR", f"{cagr(stock_returns) * 100:.2f}%", f"{cagr(spy_returns) * 100:.2f}%"],
            ["Sharpe Ratio", f"{sharpe_ratio(stock_returns):.2f}", f"{sharpe_ratio(spy_returns):.2f}"],
            ["Sortino Ratio", f"{sortino_ratio(stock_returns):.2f}", f"{sortino_ratio(spy_returns):.2f}"],
            ["Calmar Ratio", f"{calmar_ratio(stock_returns):.2f}", f"{calmar_ratio(spy_returns):.2f}"],
            ["Max Drawdown", f"{max_drawdown(stock_returns) * 100:.2f}%", f"{max_drawdown(spy_returns) * 100:.2f}%"],

        ]
        ax_summary = fig.add_subplot(gs[0, :])
        ax_summary.axis("off")
        ax_summary = ax_summary.table(
            cellText=rows,
            colLabels=columns,
            cellLoc="center",
            loc="center",
            colColours=["lightblue"] * len(columns),
            colLoc="center",
            bbox=[0, 0, 1, 1],
        )
        ax_summary.auto_set_font_size(False)
        ax_summary.set_fontsize(18)
        row_heights = [0.2, 0.3, 0.3, 0.2]  # 根據需要調整每一行的高度比例

        for (row, col), cell in ax_summary.get_celld().items():
            cell.set_height(0.3)
            if row == 0:
                cell.set_facecolor("darkblue")
                cell.set_text_props(weight="bold", color="white")
            else:
                cell.set_facecolor("whitesmoke" if row % 2 == 1 else "lightgrey")
                cell.set_text_props(color="black")

        # Plot prices
        ax_prices = fig.add_subplot(gs[1, 0])
        ax_prices.plot(stock_data.index, stock_data["Close"], label=symbol)
        ax_prices.set_title(f"{symbol} ({period})")
        ax_prices.set_xlabel("Date")
        ax_prices.set_ylabel("Price")
        plt.setp(ax_prices.get_xticklabels(), rotation=45, ha="right")
        ax_prices.legend()
        ax_prices.grid(True)

        # Plot returns
        ax_returns = fig.add_subplot(gs[1, 1])
        ax_returns.plot(stock_data.index[1:],
                        prices_to_cumulative_returns(stock_data["Close"]),
                        label=symbol)
        ax_returns.plot(SPY.index[1:],
                        prices_to_cumulative_returns(SPY["Close"]),
                        label="SPY")
        ax_returns.set_title(f"Compare with SPY")
        ax_returns.set_xlabel("Date")
        ax_returns.set_ylabel("Cumulative Return")
        plt.setp(ax_returns.get_xticklabels(), rotation=45, ha="right")
        ax_returns.legend()
        ax_returns.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        return buf
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    image = plot_stock_compare_with_spy("AAPL", "5y")
    with open("tmp.png", "wb") as f:
        f.write(image.getvalue())

