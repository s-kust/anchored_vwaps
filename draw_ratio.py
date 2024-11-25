from typing import Callable, Optional

import matplotlib.pyplot as plt
import pandas as pd

from import_ohlc import get_ohlc_from_yf


def draw_ratio(
    ticker_1: str,
    ticker_2: str,
    cutoff_date: Optional[str] = None,
    get_ohlc_func: Callable = get_ohlc_from_yf,
):
    """
    Draw Close-Close ratio
    """
    interval = "1d"
    hist_1 = get_ohlc_func(ticker=ticker_1, period="max", interval=interval)
    hist_1 = hist_1["Close"]
    hist_2 = get_ohlc_func(ticker=ticker_2, period="max", interval=interval)
    hist_2 = hist_2["Close"]
    df = pd.merge(hist_1, hist_2, left_index=True, right_index=True)
    df["CloseCloseRatio"] = df["Close_x"] / df["Close_y"]
    if cutoff_date is not None:
        # Otherwise, TypeError: Invalid comparison between
        # dtype=datetime64[ns, America/New_York] and Timestamp
        df.index = df.index.tz_convert(None)  # type: ignore
        df = df[df.index >= pd.to_datetime(cutoff_date)]
        plot_title = f"{ticker_1}-{ticker_2} Close-Close Ratio, Min Date {cutoff_date}"
    else:
        plot_title = f"{ticker_1}-{ticker_2} Close-Close Ratio"
    df["CloseCloseRatio"].plot(title=plot_title)
    plt.savefig(f"ratio_{ticker_1}_{ticker_2}.png")
    print(df)
