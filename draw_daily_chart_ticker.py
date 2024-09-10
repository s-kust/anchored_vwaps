from typing import Callable, List
from import_ohlc import get_ohlc_from_yf
from vwaps_plot_build_save import vwaps_plot_build_save

# NOTE In case of problems with Yahoo Finance,
# pass another function as the get_ohlc_func parameter
# to retrieve data from another provider.
# For example, from Alpha Vantage.


def draw_daily_chart_ticker(
    ticker: str, anchor_dates: List[str], get_ohlc_func: Callable = get_ohlc_from_yf
):
    hist = get_ohlc_func(ticker=ticker, period="2y", interval="1d")
    anchor_dates = anchor_dates
    vwaps_plot_build_save(
        input_df=hist,
        anchor_dates=anchor_dates,
        file_name=f"daily_{ticker}.png",
    )
