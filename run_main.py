import pandas as pd

from custom import get_custom_chart_annotation_1d
from draw_all_daily_charts import draw_all_daily_charts
from draw_daily_chart_ticker import draw_daily_chart_ticker
from draw_ratio import draw_ratio
from import_ohlc import get_ohlc_from_yf
from misc import get_chart_annotation_1d
from vwaps_plot_build_save import vwaps_plot_build_save


def draw_qqq_intraday():
    ticker = "QQQ"
    interval = "1m"
    hist = get_ohlc_from_yf(ticker=ticker, period="5d", interval=interval)
    anchor_dates = [
        "2024-11-21 14:30:00",
        "x2024-11-21 16:33:00",
        "2024-11-21 17:32:00",
    ]
    chart_title = {"ticker": ticker, "interval": interval}
    chart_title_str = str(chart_title)
    vwaps_plot_build_save(
        input_df=hist,
        anchor_dates=anchor_dates,
        chart_title=chart_title_str,
        add_last_min_max=False,
        chart_annotation_func=get_chart_annotation_1d,
        file_name=f"intraday_{ticker}.png",
        hide_extended_hours=True,
    )


def draw_iwm_intraday():
    ticker = "IWM"
    interval = "15m"
    hist = get_ohlc_from_yf(ticker=ticker, period="1mo", interval=interval)
    anchor_dates = [
        "2024-11-06 00:00:00",
    ]
    chart_title = {"ticker": ticker, "interval": interval}
    chart_title_str = str(chart_title)
    vwaps_plot_build_save(
        input_df=hist,
        anchor_dates=anchor_dates,
        chart_title=chart_title_str,
        chart_annotation_func=get_chart_annotation_1d,
        file_name=f"intraday_{ticker}.png",
        hide_extended_hours=True,
    )


if __name__ == "__main__":

    # draw_all_daily_charts(
    #     chart_annotation_func=get_custom_chart_annotation_1d,
    # )

    # ticker = "EVGO"
    # anchor_dates = ["2024-01-01 00:00:00"] + []
    # draw_daily_chart_ticker(
    #     ticker=ticker,
    #     anchor_dates=anchor_dates,
    #     chart_annotation_func=get_custom_chart_annotation_1d,
    # )

    # draw_qqq_intraday()
    # draw_iwm_intraday()

    draw_ratio(ticker_1="IWM", ticker_2="QQQ", cutoff_date="2020-01-01")
