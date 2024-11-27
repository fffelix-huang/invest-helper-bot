from math import sqrt
import numpy as np
import pandas as pd

def standard_deviation(returns: pd.DataFrame, days: float = 252.0) -> float:
    result = returns.std() * sqrt(days)
    return float(result.iloc[0])

def downside_risk(
    returns: pd.DataFrame,
    risk_free: float = 0.0,
    days: float = 252.0
) -> float:
    result = returns[returns < risk_free].std() * sqrt(days)
    return float(result.iloc[0])

def max_drawdown(daily_return: pd.DataFrame) -> float:
    balance = (1.0 + daily_return).cumprod()
    peak = balance.cummax()
    drawdown = (peak - balance) / peak
    result = drawdown.max()
    return float(result.iloc[0])

def correlation(returns: pd.DataFrame, target: pd.DataFrame) -> float:
    merged_df = pd.merge(
        returns,
        target,
        left_index=True,
        right_index=True,
        how="inner",
        suffixes=("_returns", "_target")
    )
    merged_df.dropna(inplace=True)
    series_returns = merged_df.iloc[:, 0]
    series_target = merged_df.iloc[:, 1]
    corr = series_returns.corr(series_target)
    return float(corr)

def sharpe_ratio(
    returns: pd.DataFrame,
    risk_free: float = 0.0,
    days: float = 252.0
) -> float:
    mean_return = returns.mean()
    excess_return = mean_return - risk_free / days
    result = (excess_return * days) / standard_deviation(returns, days=days)
    return float(result.iloc[0])

def sortino_ratio(
    returns: pd.DataFrame,
    risk_free: float = 0.0,
    days: float = 252.0
) -> float:
    mean_return = returns.mean()
    excess_return = mean_return - risk_free / days
    downside_std = downside_risk(returns, risk_free, days)
    result = (excess_return * days) / downside_std
    return float(result.iloc[0])

def calmar_ratio(returns: pd.DataFrame, days: float = 252.0) -> float:
    mean_return = returns.mean()
    mdd = max_drawdown(returns)
    result = (mean_return * days) / mdd
    return float(result.iloc[0])

def cagr(returns: pd.DataFrame, days: float = 252.0) -> float:
    mean_return = returns.mean()
    result = mean_return * days
    return float(result.iloc[0])
