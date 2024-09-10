from typing import Callable
from ticker_anchors import ticker_anchors
from import_ohlc import get_ohlc_from_yf
from vwaps_plot_build_save import vwaps_plot_build_save
from constants import first_day_of_year

# NOTE In case of problems with Yahoo Finance,
# pass another function as the get_ohlc_func parameter
# to retrieve data from another provider.
# For example, from Alpha Vantage.


def draw_all_daily_charts(get_ohlc_func: Callable = get_ohlc_from_yf):
    """
    For every ticker in ticker_anchors draw and save
    two daily OHLC + VWAPs charts.
    Chart 1 - with year's 1st day VWAP added.
    Chart 2 - without year's 1st day VWAP.
    """
    total_count = len(ticker_anchors)
    counter = 0
    for ticker in ticker_anchors:
        counter = counter + 1
        print(
            f"draw_all_daily_charts: running {ticker=} - {counter} of {total_count}..."
        )
        hist = get_ohlc_func(ticker=ticker, period="2y", interval="1d")
        anchor_dates_2 = ticker_anchors[ticker]
        anchor_dates_1 = anchor_dates_2 + [first_day_of_year]
        vwaps_plot_build_save(
            input_df=hist,
            anchor_dates=anchor_dates_1,
            file_name=f"daily_{ticker}_1.png",
            print_df=False,
        )
        vwaps_plot_build_save(
            input_df=hist,
            anchor_dates=anchor_dates_2,
            file_name=f"daily_{ticker}_2.png",
            print_df=False,
        )
