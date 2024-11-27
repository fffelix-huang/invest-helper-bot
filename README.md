# invest-helper

## Setup

Put line bot token under `.env` file as follow:

```
LINETOKEN=...
```

## Run

```py
python3 src/main.py
```

## Usage

Plot the historical stock price and compare with SPY.
Alert 5%
Member System

- Watch List
  - add()
  - remove()

- Alert
  - Interval = 1m 
  - 5% alert (5 min )

- GPT
  - summary 

- Input
  - Stock
  - Timeframe


## API List
- `schedule_alert()`
  - return: `[(email, stock, price), ...]`
