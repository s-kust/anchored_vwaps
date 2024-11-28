import pandas as pd
import yfinance as yf


def get_ohlc_from_yf(
    ticker: str, period: str = "2y", interval: str = "1d"
) -> pd.DataFrame:
    """
    Get OHLC DataFrame with Volume from Yahoo Finance.
    Save some supplementary data in attrs before returning.
    Valid periods:'1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
    Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    res = yf.Ticker(ticker=ticker).history(period=period, interval=interval)

    # NOTE  If period and interval mismatch, Yahoo Finance returns empty DataFrame.
    # A mismatch is an interval too small for a long period.
    if res.shape[0] == 0:
        raise RuntimeError(
            f"get_ohlc_with_typical: Yahoo Finance returned empty Df for {ticker=}, maybe mismatch between {period=} and {interval=}"
        )

    res = res[["Open", "High", "Low", "Close", "Volume"]]

    # NOTE see https://stackoverflow.com/questions/14688306/adding-meta-information-metadata-to-pandas-dataframe
    # about adding metadata to pd.DataFrame
    res.attrs["ticker"] = ticker
    res.attrs["period"] = period
    res.attrs["interval"] = interval
    return res
