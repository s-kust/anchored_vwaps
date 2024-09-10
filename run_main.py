from draw_all_daily_charts import draw_all_daily_charts
from draw_daily_chart_ticker import draw_daily_chart_ticker
from import_ohlc import get_ohlc_from_yf
from vwaps_plot_build_save import vwaps_plot_build_save


def draw_qqq_intraday():
    hist = get_ohlc_from_yf(ticker="AAPL", period="5d", interval="1m")
    anchor_dates = [
        "2024-09-10 13:30:00",
        "x2024-09-10 17:00:00",
        "2024-09-10 18:04:00",
    ]
    vwaps_plot_build_save(
        input_df=hist,
        anchor_dates=anchor_dates,
        file_name="intraday_QQQ.png",
    )


def draw_msft_intraday():
    hist = get_ohlc_from_yf(ticker="MSFT", period="5d", interval="1m")
    anchor_dates = [
        "2024-09-10 13:30:00",
        "x2024-09-10 15:30:00",
        "2024-09-10 16:14:00",
    ]
    vwaps_plot_build_save(
        input_df=hist, anchor_dates=anchor_dates, file_name="intraday_QQQ.png"
    )


def draw_aapl_intraday():
    hist = get_ohlc_from_yf(ticker="AAPL", period="5d", interval="1m")
    anchor_dates = [
        "2024-09-10 13:30:00",
        "2024-09-10 16:03:00",
        "2024-09-10 16:14:00",
    ]
    vwaps_plot_build_save(
        input_df=hist, anchor_dates=anchor_dates, file_name="intraday_QQQ.png"
    )


if __name__ == "__main__":

    # draw_all_daily_charts()

    # ticker = "KLAC"
    # anchor_dates = [
    #     "2024-01-01 00:00:00",
    # ] + ["2024-08-03 00:00:00", "2024-07-11 00:00:00"]
    # draw_daily_chart_ticker(ticker=ticker, anchor_dates=anchor_dates)

    # draw_msft_intraday()
    draw_qqq_intraday()
