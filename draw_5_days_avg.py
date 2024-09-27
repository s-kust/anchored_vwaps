import mplfinance as mpf
import pandas as pd

from import_ohlc import get_ohlc_from_yf


def draw_5_days_avg(ticker: str, interval: str = "15m"):
    """
    Create and save plot 5_d_avg_{ticker}.png
    containing OHLC candles and 5 days simple moving average (SMA).
    Usage: avoid buying the dip until the price consolidates above 5 days SMA.
    For details, see Appendix B
    of the book "Maximum Trading Gains With Anchored VWAP".
    """
    if interval not in ["15m", "30m"]:
        raise ValueError(f"draw_5_days_avg: {interval=}, must be 15m or 30m")
    df = get_ohlc_from_yf(ticker=ticker, period="1mo", interval=interval)
    df.index = df.index.tz_convert(None)
    if interval == "15m":
        ma_candles_count = 130
    else:
        ma_candles_count = 65
    ma_values = df["Close"].rolling(ma_candles_count).mean().values
    ma_df = pd.DataFrame(dict(ma_vals=ma_values), index=df.index)
    ap = mpf.make_addplot(ma_df, type="line")
    mpf.plot(
        df,
        type="candle",
        savefig=f"5_d_avg_{ticker}.png",
        datetime_format="%b-%d",
        addplot=ap,
        figratio=(12, 8),
        title={
            "title": f"{ticker}, interval {interval}, MA last {round(ma_df['ma_vals'].iloc[-1], 2)}",
            "y": 1,
        },
        tight_layout=True,
    )
