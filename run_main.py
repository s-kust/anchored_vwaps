import pandas as pd

from draw_daily_chart_ticker import draw_daily_chart_ticker
from import_ohlc import get_ohlc_from_yf
from misc import get_custom_chart_annotation_1d
from vwaps_plot_build_save import vwaps_plot_build_save


def draw_qqq_intraday():
    ticker = "QQQ"
    interval = "1m"
    hist = get_ohlc_from_yf(ticker=ticker, period="2d", interval=interval)
    anchor_dates = [
        "2024-10-04 13:30:00",
        # "2024-10-04 13:44:00",
        # "2024-10-04 15:11:00",
        "x2024-10-04 19:04:00",
    ]
    chart_title = {"ticker": ticker, "interval": interval}
    chart_title_str = str(chart_title)
    vwaps_plot_build_save(
        input_df=hist,
        anchor_dates=anchor_dates,
        chart_title=chart_title_str,
        chart_annotation_func=get_custom_chart_annotation_1d,
        file_name=f"intraday_{ticker}.png",
        hide_extended_hours=True,
    )


def draw_iwm_intraday():
    ticker = "IWM"
    interval = "1m"
    hist = get_ohlc_from_yf(ticker=ticker, period="2d", interval=interval)
    anchor_dates = [
        "2024-10-04 13:30:00",
        # "2024-10-04 13:44:00",
        # "2024-10-04 15:11:00",
        "x2024-10-04 19:04:00",
    ]
    chart_title = {"ticker": ticker, "interval": interval}
    chart_title_str = str(chart_title)
    vwaps_plot_build_save(
        input_df=hist,
        anchor_dates=anchor_dates,
        chart_title=chart_title_str,
        chart_annotation_func=get_custom_chart_annotation_1d,
        file_name=f"intraday_{ticker}.png",
        hide_extended_hours=True,
    )


if __name__ == "__main__":

    # draw_all_daily_charts()

    # ticker = "IWM"
    # anchor_dates = ["2024-01-01 00:00:00"] + [
    #     "x2024-08-03 00:00:00",
    # ]
    # draw_daily_chart_ticker(ticker=ticker, anchor_dates=anchor_dates)

    draw_qqq_intraday()
    # draw_iwm_intraday()
