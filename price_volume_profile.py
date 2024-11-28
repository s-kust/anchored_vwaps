from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots

from import_ohlc import get_ohlc_from_yf


def create_candlestick_volume_chart(
    df: pd.DataFrame, ticker: Optional[str] = None
) -> Figure:
    """
    Create a candlestick chart with volume profile and price profile using Plotly
    """
    bins_count = 50
    # Calculate volume profile
    price_bins = np.linspace(df["Low"].min(), df["High"].max(), bins_count)
    volume_profile, volume_bin_edges = np.histogram(
        df["Close"], bins=price_bins, weights=df["Volume"]
    )

    # Calculate Price Profile (distribution of prices)
    price_profile, price_bin_edges = np.histogram(df["Close"], bins=bins_count)

    if ticker is not None:
        title_main = f"Candlestick: {ticker}"
    else:
        title_main = "Candlestick"

    fig = make_subplots(
        rows=1,
        cols=3,
        column_widths=[0.2, 0.2, 0.6],
        subplot_titles=("Price Profile", "Volume Profile", title_main),
    )

    volume_bar_colors = [
        "green" if vol > np.percentile(volume_profile, 70) else "lightgray"
        for vol in volume_profile
    ]

    fig.add_trace(
        go.Bar(
            x=price_profile,
            y=price_bin_edges[:-1],
            orientation="h",
            marker_color="blue",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            x=volume_profile,
            y=volume_bin_edges[:-1],
            orientation="h",
            marker_color=volume_bar_colors,
        ),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
        ),
        row=1,
        col=3,
    )

    fig.update_layout(
        height=600,
        width=1500,
        xaxis1=dict(rangeslider=dict(visible=False)),
        xaxis2=dict(rangeslider=dict(visible=False)),
        xaxis3=dict(
            rangeslider=dict(visible=False),
            rangebreaks=[
                dict(bounds=["sat", "mon"]),
                dict(
                    # NOTE You may have to adjust these bounds for hours, see details in README.md
                    bounds=[16, 9.5],
                    pattern="hour",
                ),
            ],
        ),
        yaxis1=dict(range=[min(df["Low"]), max(df["High"])]),
        yaxis2=dict(range=[min(df["Low"]), max(df["High"])]),
        yaxis3=dict(range=[min(df["Low"]), max(df["High"])]),
        showlegend=False,
        margin=dict(l=10, r=20, t=25, b=10),
    )
    return fig


def draw_profile_of_data(ohlc_df: pd.DataFrame, ticker: str) -> None:
    """
    1. Run create_candlestick_volume_chart.
    2. Save png file
    """

    figure = create_candlestick_volume_chart(ohlc_df, ticker=ticker)

    all_index_dates = set(ohlc_df.index.date)  # type: ignore
    len_all_index_dates = len(all_index_dates)
    if len_all_index_dates == 1:
        index_date = ohlc_df.index[-1].date()
        chart_file_name = f"profile_{ticker}_{index_date}.png"
    else:
        chart_file_name = f"profile_{ticker}_{len_all_index_dates}d.png"
    figure.write_image(chart_file_name)


if __name__ == "__main__":

    TICKER = "TLT"

    data = get_ohlc_from_yf(ticker=TICKER, period="5d", interval="5m")
    print(data.head())
    print(data.tail())

    sorted_dates = sorted(list(set(data.index.date)))  # type: ignore
    if len(sorted_dates) != 5:
        raise ValueError(
            f"We ask Yahoo Finance for 5 days of data, so len should be 5, {sorted_dates=}"
        )

    # Draw one-day profile for yesterday
    data_slice: pd.DataFrame = data[data.index.date == sorted_dates[-1]]  # type: ignore
    draw_profile_of_data(ohlc_df=data_slice, ticker=TICKER)

    # Draw one-day profile for the day before yesterday
    data_slice: pd.DataFrame = data[data.index.date == sorted_dates[-2]]  # type: ignore
    draw_profile_of_data(ohlc_df=data_slice, ticker=TICKER)

    # Draw one-day profile for the day 3 days ago
    data_slice: pd.DataFrame = data[data.index.date == sorted_dates[-3]]  # type: ignore
    draw_profile_of_data(ohlc_df=data_slice, ticker=TICKER)

    # Draw two-days profile for the day before yesterday and yesterday
    data_slice: pd.DataFrame = data[data.index.date >= sorted_dates[-2]]  # type: ignore
    draw_profile_of_data(ohlc_df=data_slice, ticker=TICKER)

    # Draw three-days profile
    data_slice: pd.DataFrame = data[data.index.date >= sorted_dates[-3]]  # type: ignore
    draw_profile_of_data(ohlc_df=data_slice, ticker=TICKER)
