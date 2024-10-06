from typing import Callable, List

from constants import first_day_of_year
from import_ohlc import get_ohlc_from_yf
from misc import get_custom_chart_annotation_1d
from ticker_anchors import ticker_anchors
from vwaps_plot_build_save import vwaps_plot_build_save

# NOTE In case of problems with Yahoo Finance,
# pass another function as the get_ohlc_func parameter
# to retrieve data from another provider.
# For example, from Alpha Vantage.


def draw_all_daily_charts(get_ohlc_func: Callable = get_ohlc_from_yf):
    """
    For every ticker in ticker_anchors draw and save
    two daily OHLC + VWAPs charts.
    Chart 1: with year's 1st day VWAP added.
    Chart 2: without year's 1st day VWAP.
    """

    total_count = len(ticker_anchors)
    interval = "1d"
    counter = 0
    for ticker in ticker_anchors:
        counter = counter + 1
        print(
            f"draw_all_daily_charts: running {ticker=} - {counter} of {total_count}..."
        )
        hist = get_ohlc_func(ticker=ticker, period="2y", interval=interval)
        anchor_dates_2: List[str] = ticker_anchors[ticker]
        # anchor_dates_2: List[str] = list()
        anchor_dates_1 = anchor_dates_2 + [first_day_of_year]
        chart_title = {"ticker": ticker, "interval": interval}
        chart_title_str = str(chart_title)
        vwaps_plot_build_save(
            input_df=hist,
            anchor_dates=anchor_dates_1,
            chart_annotation_func=get_custom_chart_annotation_1d,
            chart_title=chart_title_str,
            file_name=f"daily_{ticker}_1.png",
            print_df=False,
        )
        vwaps_plot_build_save(
            input_df=hist,
            anchor_dates=anchor_dates_2,
            chart_annotation_func=get_custom_chart_annotation_1d,
            chart_title=chart_title_str,
            file_name=f"daily_{ticker}_2.png",
            print_df=False,
        )
