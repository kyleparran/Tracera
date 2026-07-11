"""Grain futures prices (free, via Yahoo Finance continuous contracts).

Prototype & docs: cme.ipynb  (CME direct feeds are paid; Yahoo is the free path.)
"""
import pandas as pd

TICKERS = {"Corn": "ZC=F", "Soybeans": "ZS=F", "Wheat": "ZW=F"}


def grain_futures(start="2021-01-01", end=None, tickers=TICKERS) -> pd.DataFrame:
    """Daily front-month close in $/bushel (Yahoo quotes cents/bushel)."""
    import yfinance as yf
    px = yf.download(list(tickers.values()), start=start, end=end,
                     auto_adjust=True, progress=False)["Close"]
    if hasattr(px, "columns"):
        px = px.rename(columns={v: k for k, v in tickers.items()})
    return (px / 100).round(2)     # cents/bu -> $/bu
