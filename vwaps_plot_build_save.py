from typing import Callable, List, Set, Tuple

import pandas as pd
import plotly.graph_objects as go

from constants import ATR_SMOOTHING_N, DEFAULT_RESULTS_FILE
from misc import fill_is_min_max


def _preprocess_anchor_dates(
    df: pd.DataFrame,
    anchor_dates: List[str],
) -> Tuple[Set[pd.Timestamp], pd.Timestamp]:
    """
    1. Convert a list of strings to a list of Timestamps.
    2. Add last_min_date and last_max_date to the list of anchor dates.
    3. Find the minimum date.
    """

    last_min_date = df[df["is_min"] == True].index.max()
    last_max_date = df[df["is_max"] == True].index.max()

    # NOTE If an element with anchor_date[0] == "x" is found
    # in the anchor_dates list, it is assigned to min_anchor_date.
    # Otherwise, min_anchor_date = min(anchor_points).
    # The benefits of this feature are explained in the readme doc.

    min_anchor_date = None
    for anchor_date in anchor_dates:
        if anchor_date[0] == "x":
            min_anchor_date = pd.to_datetime(anchor_date[1:])
    anchor_points = [
        anchor_date[1:] if anchor_date[0] == "x" else anchor_date
        for anchor_date in anchor_dates
    ]
    anchor_points = [pd.to_datetime(anchor_dt_str) for anchor_dt_str in anchor_points]

    # NOTE Here we add last_min_date last_max_date
    # and later draw them on the chart,
    # because these Anchored VWAPs are important.
    anchor_points = anchor_points + [last_min_date, last_max_date]

    anchor_points_to_return: Set[pd.Timestamp] = set(anchor_points)
    if min_anchor_date is None:
        min_anchor_date = min(anchor_points)

    return anchor_points_to_return, min_anchor_date


def get_chart_annotation(df: pd.DataFrame) -> str:

    vwap_values = list()
    vwap_columns = [column for column in df.columns if column.startswith("A_VWAP_")]
    for vwap_column in vwap_columns:
        vwap_values.append(round(df[vwap_column].iloc[-1], 2))
    res_to_return = "VWAPs last values: " + str(sorted(vwap_values))
    res_to_return = (
        res_to_return + "; Closed last: " + str(round(df[f"Close"].values[-1], 2))
    )
    # NOTE You can add additional information to the annotation here,
    # or preferably write a custom function and pass it as a chart_annotation_func parameter
    #  when calling the function vwaps_plot_build_save.
    # See the get_custom_chart_annotation_1d function as an example.
    return res_to_return


def vwaps_plot_build_save(
    input_df: pd.DataFrame,
    anchor_dates: List[str],
    chart_title: str = "",
    chart_annotation_func: Callable = get_chart_annotation,
    file_name: str = DEFAULT_RESULTS_FILE,
    print_df: bool = True,
    hide_extended_hours: bool = False,
):
    """
    1. Transform every element of anchor_dates to pd.Timestamp.
    2. Add a new column with a typical price.
    3. For each anchor date, create a column with Anchored VWAP.
    4. Build a candlestick chart with all Anchored VWAPs and save it.

    Add x before the desired date to make the chart start from that date.
    For example, x2024-08-03 00:00:00 instead of 2024-08-03 00:00:00.
    By default, the chart will start from the minimum date in the anchor_dates list.
    See example in the readme.
    """

    df = input_df.copy()
    if (
        f"atr_{ATR_SMOOTHING_N}" not in df.columns
        or "is_min" not in df.columns
        or "is_max" not in df.columns
    ):
        df = fill_is_min_max(df=df)

    # Otherwise, TypeError: Invalid comparison between
    # dtype=datetime64[ns, America/New_York] and Timestamp
    df.index = df.index.tz_convert(None)

    anchor_points, min_anchor_point = _preprocess_anchor_dates(
        df=df, anchor_dates=anchor_dates
    )

    if "Typical" not in df.columns:
        df["Typical"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4
    if "TypicalMultiplyVolume" not in df.columns:
        df["TypicalMultiplyVolume"] = df["Typical"] * df["Volume"]

    # Add anchored VWAP column for every date passed in anchor_points
    counter = 0
    for anchor_dt in anchor_points:
        counter = counter + 1
        df[f"A_VWAP_{counter}"] = (
            df["TypicalMultiplyVolume"]
            .where(df.index >= anchor_dt)
            .groupby(df.index >= anchor_dt)
            .cumsum()
            / df["Volume"]
            .where(df.index >= anchor_dt)
            .groupby(df.index >= anchor_dt)
            .cumsum()
        )

    df = df[df.index >= min_anchor_point]
    if print_df:
        print(df[["Open", "High", "Low", "Close", "Volume"]])
    # df.to_excel("DF_before_plot_VWAP.xlsx")
    del df["TypicalMultiplyVolume"]
    del df["Typical"]

    plot_data = [
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            line=dict(width=1),
        )
    ]
    for counter in range(1, len(anchor_points) + 1):
        plot_data.append(
            go.Scatter(
                x=df.index,
                y=df[f"A_VWAP_{counter}"],
                mode="lines",
            ),
        )
    fig = go.Figure(data=plot_data)
    # fig.update_layout(
    #     margin=dict(l=10, r=10, t=10, b=10),
    # )

    # Add title to the chart if data is available
    # and increase the top margin to fit the title
    fig.update_layout(
        title=chart_title,
        title_x=0.5,
        title_y=0.99,
        margin=dict(l=10, r=10, t=20, b=10),
    )
    fig.add_annotation(
        xref="x domain",
        yref="y domain",
        x=0.01,
        y=0.99,
        text=chart_annotation_func(df=df),
        showarrow=False,
        # row=1,
        # col=1,
    )

    fig.update_xaxes(
        rangeslider_visible=False,
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends, Saturday to before Monday
        ],
    )
    if hide_extended_hours and (input_df.attrs["interval"] != "1d"):
        fig.update_xaxes(
            rangebreaks=[
                dict(
                    # NOTE You may have to adjust these bounds for hours
                    bounds=[21, 13.5],
                    pattern="hour",
                ),  # hide hours outside of trading hours, in my case 21:00-13:30
            ],
        )

    fig.update_layout(showlegend=False)

    # NOTE it requires kaleido package,
    # see https://stackoverflow.com/a/59819140/3139228
    fig.write_image(file_name)
