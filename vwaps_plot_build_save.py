from typing import List, Tuple
import pandas as pd
import plotly.graph_objects as go
from constants import DEFAULT_RESULTS_FILE


def _preprocess_anchor_dates(
    anchor_dates: List[str],
) -> Tuple[List[pd.Timestamp], pd.Timestamp]:
    """
    Convert a list of strings to a list of Timestamps,
    find the minimum date and return.
    """

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
    if min_anchor_date is None:
        min_anchor_date = min(anchor_points)
    return anchor_points, min_anchor_date


def vwaps_plot_build_save(
    input_df: pd.DataFrame,
    anchor_dates: List[str],
    file_name: str = DEFAULT_RESULTS_FILE,
    print_df: bool = True,
    hide_extended_hours=True,
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

    # Otherwise, TypeError: Invalid comparison between
    # dtype=datetime64[ns, America/New_York] and Timestamp
    df.index = df.index.tz_convert(None)

    anchor_points, min_anchor_point = _preprocess_anchor_dates(
        anchor_dates=anchor_dates
    )

    if "Typical" not in df.columns:
        df["Typical"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4
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
        print(df)
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
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
    )

    # TODO improve title, add more info

    # Add title to the chart if data is available
    # and increase the top margin to fit the title
    if input_df.attrs:
        fig.update_layout(
            title=f"{input_df.attrs}",
            title_x=0.5,
            title_y=0.99,
            margin=dict(l=10, r=10, t=20, b=10),
        )
    # TODO add latest values ​of VWAPs ​to title
    fig.update_xaxes(
        rangeslider_visible=False,
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends, Saturday to before Monday
        ],
    )
    if hide_extended_hours:
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
