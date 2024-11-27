import os
from typing import Final
from dotenv import load_dotenv
import discord
from discord.ext import commands
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import io
import datetime

load_dotenv()

TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import io
import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")

@bot.command(help=
"""
獲取指定股票在指定時間範圍內的股價並繪製圖表
使用方法: !stock <股票代碼> <時間範圍>
例如:
!stock AAPL 1m
!stock TSLA 5d
!stock 2330.TW 1y
""")
async def stock(ctx, symbol: str, period: str = "1m"):
    period = period.lower()

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

    if period not in VALID_PERIODS:
        valid_periods = ", ".join(VALID_PERIODS.keys())
        await ctx.send(f"無效的時間範圍 `{period}`。請使用以下之一：{valid_periods}")
        return

    yf_period = VALID_PERIODS[period]

    try:
        stock_data = yf.download(symbol, period=yf_period, interval="1d")

        if stock_data.empty:
            await ctx.send(f"找不到股票代碼 `{symbol}` 的資料。請確認代碼是否正確。")
            return

        symbol = symbol.upper()
        start_date = stock_data.index[0]
        end_date = stock_data.index[-1]
        SPY = yf.download("SPY", start=start_date, end=end_date, interval="1d")

        fig, (ax, ax2) = plt.subplots(1, 2, figsize=(18, 12))
        ax.plot(stock_data.index, stock_data["Close"], label=symbol)
        ax.set_title(f"{symbol} ({period})")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True)

        ax2.plot(stock_data.index[1:], (stock_data["Close"].pct_change().dropna() + 1.0).cumprod() - 1.0, label=symbol)
        ax2.plot(SPY.index[1:], (SPY["Close"].pct_change().dropna() + 1.0).cumprod() - 1.0, label="SPY")
        ax2.set_title(f"Compare with SPY")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Cumulative Return")
        ax2.legend()
        ax2.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        file = discord.File(fp=buf, filename=f"{symbol}_stock.png")

        await ctx.send(file=file)

    except Exception as e:
        await ctx.send(f"發生錯誤：{str(e)}")



def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
