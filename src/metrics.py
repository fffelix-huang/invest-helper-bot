from math import sqrt
import numpy as np
import pandas as pd

def standard_deviation(returns: pd.DataFrame, days: float = 252.0) -> float:
    return float(returns.std() * sqrt(days))

def downside_risk(
    returns: pd.DataFrame,
    risk_free: float = 0.0,
    days: float = 252.0
) -> float:
    return float(returns[returns < risk_free].std() * sqrt(days))

def max_drawdown(daily_return: pd.DataFrame) -> float:
    balance = (1.0 + daily_return).cumprod()
    peak = balance.cummax()
    drawdown = (peak - balance) / peak
    return float(drawdown.max())

def sharpe_ratio(
    returns: pd.DataFrame,
    risk_free: float = 0.0,
    days: float = 252.0
) -> float:
    mean_return = returns.mean()
    excess_return = mean_return - risk_free / days
    return float((excess_return * days) / standard_deviation(returns, days=days))

def sortino_ratio(
    returns: pd.DataFrame,
    risk_free: float = 0.0,
    days: float = 252.0
) -> float:
    mean_return = returns.mean()
    excess_return = mean_return - risk_free / days
    downside_std = downside_risk(returns, risk_free, days)
    return float((excess_return * days) / downside_std)

def calmar_ratio(returns: pd.DataFrame, days: float = 252.0) -> float:
    mean_return = returns.mean()
    mdd = max_drawdown(returns)
    return float((mean_return * days) / mdd)

def cagr(returns: pd.DataFrame, days: float = 252.0) -> float:
    mean_return = returns.mean()
    return float(mean_return * days)
