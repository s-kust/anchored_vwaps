from typing import Callable

import pandas as pd

from constants import first_day_of_year
from import_ohlc import get_ohlc_from_yf
from misc import get_chart_annotation_1d
from vwaps_plot_build_save import vwaps_plot_build_save

# NOTE In case of problems with Yahoo Finance,
# pass another function as the get_ohlc_func parameter
# to retrieve data from another provider.
# For example, from Alpha Vantage.


def draw_all_daily_charts(
    get_ohlc_func: Callable = get_ohlc_from_yf,
    chart_annotation_func: Callable = get_chart_annotation_1d,
):
    """
    For every ticker in tickers_notes draw and save
    two daily OHLC + VWAPs charts.
    Chart 1: with year's 1st day VWAP added.
    Chart 2: without year's 1st day VWAP.

    Fill the tickers_follow_daily.xlsx file with the tickers
    you are interested in, their notes, and anchor dates.
    You can add zero, one, or several custom anchor dates to each ticker.
    Please note that anchor dates for the last recent low and high
    are added automatically, i.e. you don't have to add and update them manually.

    See detailed explanations in the README.md.
    """

    xls = pd.ExcelFile("tickers_follow_daily.xlsx")
    tickers_notes = pd.read_excel(xls, "Notes")
    tickers_anchor_dates = pd.read_excel(xls, "Anchor_Dates")
    total_count = tickers_notes.shape[0]
    interval = "1d"
    counter = 0
    for ticker in tickers_notes["Ticker"].values:
        counter = counter + 1
        print(
            f"draw_all_daily_charts: running {ticker=} - {counter} of {total_count}..."
        )
        ohlc_df = get_ohlc_func(ticker=ticker, period="max", interval=interval)

        # adding your custom anchor dates for the ticker if they are available
        custom_anchor_dates = list()
        if ticker in tickers_anchor_dates.columns:
            custom_anchor_dates = tickers_anchor_dates[ticker].values.tolist()
        all_anchor_dates = custom_anchor_dates + [first_day_of_year]

        # adding the ticker note so that it will appear in the chart annotation
        ticker_note = tickers_notes.loc[
            tickers_notes["Ticker"] == ticker, "Note"
        ].values[0]
        if ticker_note != "":
            ohlc_df.attrs["note"] = ticker_note

        chart_title = {"ticker": ticker, "interval": interval}
        chart_title_str = str(chart_title)

        vwaps_plot_build_save(
            input_df=ohlc_df,
            anchor_dates=all_anchor_dates,
            chart_annotation_func=chart_annotation_func,
            chart_title=chart_title_str,
            add_last_min_max=True,
            file_name=f"daily_{ticker}_1.png",
            print_df=False,
        )
        vwaps_plot_build_save(
            input_df=ohlc_df,
            anchor_dates=custom_anchor_dates,
            chart_annotation_func=chart_annotation_func,
            chart_title=chart_title_str,
            add_last_min_max=True,
            file_name=f"daily_{ticker}_2.png",
            print_df=False,
        )
