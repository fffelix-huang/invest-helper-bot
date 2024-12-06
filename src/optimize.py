import numpy as np
import pandas as pd
import yfinance as yf
import io
import datetime
import skfolio as skf
import skfolio.typing as skt
from skfolio import Population, RiskMeasure
from skfolio.optimization import RiskBudgeting
from skfolio.portfolio import BasePortfolio
from skfolio.preprocessing import prices_to_returns
from sklearn.model_selection import train_test_split
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from src.metrics import *

def optimize_portfolio(stocks: list[str]) -> io.BytesIO:
    try:
        prices = yf.download(stocks, period="5y", interval="1d")
        prices = prices["Adj Close"]

        benchmark = yf.download("SPY", period="5y", interval="1d")
        benchmark = benchmark["Adj Close"]
        benchmark = prices_to_returns(benchmark)
        _, benchmark = train_test_split(benchmark, test_size=0.75, shuffle=False)
        benchmark = BasePortfolio(
            returns=benchmark,
            observations=benchmark.index,
            name="SPY",
            annualized_factor=252.0,
            risk_free_rate=0.0,
            compounded=False
        )

        X = prices_to_returns(prices)
        X_train, X_test = train_test_split(X, test_size=0.75, shuffle=False)

        model = RiskBudgeting(
            risk_measure=RiskMeasure.VARIANCE,
            portfolio_params=dict(name="AI Portfolio"),
        )
        model.fit(X_train)
        pred_model = model.predict(X_test)

        population = Population([pred_model, benchmark])

        fig_combined = make_subplots(
            rows=2,
            cols=2,
            specs=[
                [{"colspan": 2}, None],
                [{}, {}]
            ],
            subplot_titles=(
                "Cumulative Returns",
                "Portfolios Composition",
                "Contribution to Sharpe Ratio"
            )
        )

        # 1. cumulative returns
        fig_cum_returns = population.plot_cumulative_returns()
        for trace in fig_cum_returns["data"]:
            trace.legendgroup = "1"
            fig_combined.add_trace(trace, row=1, col=1)

        # 2. portfolios composition
        fig_composition = population.plot_composition()
        for trace in fig_composition["data"]:
            trace.legendgroup = "2"
            fig_combined.add_trace(trace, row=2, col=1)

        # 3. Contribution to Sharpe Ratio
        fig_contribution = population.plot_contribution(measure=skt.RatioMeasure.SHARPE_RATIO)
        for trace in fig_contribution["data"]:
            trace.legendgroup = "3"
            fig_combined.add_trace(trace, row=2, col=2)

        fig_combined.update_layout(
            height=900,
            width=1200,
            title_text="Analysis Report",
            legend_tracegroupgap=30
        )

        buf = io.BytesIO()
        fig_combined.write_image(buf, format="png")
        buf.seek(0)

        return buf

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    image = optimize_portfolio(["AAPL", "NVDA", "TSLA", "JPM", "LLY"])
    with open("tmp.png", "wb") as f:
        f.write(image.getvalue())
