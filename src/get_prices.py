import yfinance as yf
import pandas as pd
import numpy as np

TRADING_DAYS =252
tickers = ["^GSPC", "^FTSE"]

prices = yf.download(tickers, start="2019-01-01", progress=False)["Close"].dropna()

# daily returns
returns = prices.pct_change().dropna()

# annualised volatility
vol = returns.std() * (252 ** 0.5)

# Daily returns
returns = prices.pct_change().dropna()

# Equity curve (growth of £1)
equity = (1 + returns).cumprod()

# Drawdown: % below prior peak
running_peak = equity.cummax()
drawdown = equity / running_peak - 1.0

# Summary metrics
ann_return = returns.mean() * TRADING_DAYS
ann_vol = returns.std() * np.sqrt(TRADING_DAYS)
max_dd = drawdown.min()  # most negative drawdown

summary = pd.DataFrame({
    "annual_return": ann_return,
    "volatility": ann_vol,
    "max_drawdown": max_dd,
})
summary["return_per_risk"] = summary["annual_return"] / summary["volatility"]

print("\n=== Summary ===")
print(summary.sort_values("return_per_risk", ascending=False))

print("\n=== Worst drawdown dates ===")
worst_dates = drawdown.idxmin()
for t in tickers:
    print(f"{t}: {worst_dates[t].date()} (max DD {max_dd[t]:.2%})")