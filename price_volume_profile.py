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


# Example usage
def generate_sample_data() -> pd.DataFrame:
    """Generate sample stock data for demonstration"""
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="B")

    np.random.seed(42)

    open_prices = 100 + np.cumsum(np.random.normal(0, 1, len(dates)))
    close_prices = open_prices + np.random.normal(0, 2, len(dates))
    high_prices = np.maximum(open_prices, close_prices) + np.abs(
        np.random.normal(0, 1, len(dates))
    )
    low_prices = np.minimum(open_prices, close_prices) - np.abs(
        np.random.normal(0, 1, len(dates))
    )
    volumes = np.random.randint(1000000, 5000000, len(dates))

    df = pd.DataFrame(
        {
            "Date": dates,
            "Open": open_prices,
            "High": high_prices,
            "Low": low_prices,
            "Close": close_prices,
            "Volume": volumes,
        }
    )
    return df


if __name__ == "__main__":

    # data = generate_sample_data()
    TICKER = "IWM"
    data = get_ohlc_from_yf(ticker=TICKER, period="5d", interval="15m")
    print(data.head())
    print(data.tail())
    print(max(data.index).day)
    chart = create_candlestick_volume_chart(data, ticker=TICKER)
    chart.write_image(f"market_volume_profile_{TICKER}.png")
