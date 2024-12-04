from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots

from import_ohlc import get_ohlc_from_yf

VALUE_REGION_PERCENTILE = 0.7


def _get_volume_profile_value_region_indexes(
    volume_profile: np.ndarray,
) -> Tuple[int, int]:
    """
    Get first and last index of the middle VALUE_REGION_PERCENTILE of the input volume profile.
    """
    v_p_sum = np.sum(volume_profile)
    value_region_sum = v_p_sum * VALUE_REGION_PERCENTILE
    volume_subtracted_from_bottom = volume_subtracted_from_top = 0
    v_r_index_bottom = 0
    v_r_index_top = len(volume_profile) - 1
    iteration_num = 0
    while v_p_sum > value_region_sum:
        # NOTE Trying tu subtract equal volumes from top and bottom of the histogram
        while volume_subtracted_from_bottom <= volume_subtracted_from_top:
            if v_p_sum <= value_region_sum:
                break
            volume_subtracted_from_bottom += volume_profile[v_r_index_bottom]
            v_p_sum -= volume_profile[v_r_index_bottom]
            v_r_index_bottom += 1
        while volume_subtracted_from_top <= volume_subtracted_from_bottom:
            if v_p_sum <= value_region_sum:
                break
            volume_subtracted_from_top += volume_profile[v_r_index_top]
            v_p_sum -= volume_profile[v_r_index_top]
            v_r_index_top -= 1
        iteration_num += 1
    return v_r_index_bottom, v_r_index_top


def get_volume_profile_colors(volume_profile: np.ndarray) -> List[str]:
    v_r_index_first, v_r_index_last = _get_volume_profile_value_region_indexes(
        volume_profile=volume_profile
    )
    volume_bar_colors = list()
    for counter in range(len(volume_profile)):
        if (counter >= v_r_index_first) and (counter <= v_r_index_last):
            volume_bar_colors.append("green")
        else:
            volume_bar_colors.append("lightgray")
    return volume_bar_colors


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

    volume_bar_colors = get_volume_profile_colors(volume_profile=volume_profile)

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

    TICKER = "EWZ"

    data = get_ohlc_from_yf(ticker=TICKER, period="5d", interval="1m")
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

    # Draw five-days profile
    draw_profile_of_data(ohlc_df=data, ticker=TICKER)
