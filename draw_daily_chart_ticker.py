from typing import Callable, List

from import_ohlc import get_ohlc_from_yf
from misc import get_chart_annotation_1d
from vwaps_plot_build_save import vwaps_plot_build_save

# NOTE In case of problems with Yahoo Finance,
# pass another function as the get_ohlc_func parameter
# to retrieve data from another provider.
# For example, from Alpha Vantage.


def draw_daily_chart_ticker(
    ticker: str,
    anchor_dates: List[str],
    get_ohlc_func: Callable = get_ohlc_from_yf,
    chart_annotation_func: Callable = get_chart_annotation_1d,
):
    interval = "1d"
    hist = get_ohlc_func(ticker=ticker, period="max", interval=interval)
    chart_title = {"ticker": ticker, "interval": interval}
    vwaps_plot_build_save(
        input_df=hist,
        anchor_dates=anchor_dates,
        chart_title=str(chart_title),
        chart_annotation_func=chart_annotation_func,
        add_last_min_max=True,
        file_name=f"daily_{ticker}.png",
    )
