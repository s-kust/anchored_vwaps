from draw_all_daily_charts import draw_all_daily_charts
from draw_daily_chart_ticker import draw_daily_chart_ticker
from import_ohlc import get_ohlc_from_yf
from vwaps_plot_build_save import vwaps_plot_build_save


def draw_qqq_intraday():
    hist = get_ohlc_from_yf(ticker="QQQ", period="5d", interval="1m")
    anchor_dates = [
        "2024-09-09 13:30:00",
        "x2024-09-09 18:39:00",
    ]
    vwaps_plot_build_save(
        input_df=hist, anchor_dates=anchor_dates, file_name="intraday_QQQ.png"
    )


if __name__ == "__main__":

    # draw_all_daily_charts()

    # ticker = "SMH"
    # anchor_dates = [
    #     "2024-01-01 00:00:00",
    # ] + ["2024-08-03 00:00:00", "x2024-07-11 00:00:00"]
    # draw_daily_chart_ticker(ticker=ticker, anchor_dates=anchor_dates)

    draw_qqq_intraday()
