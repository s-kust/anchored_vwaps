import pandas as pd

from constants import ATR_SMOOTHING_N


def add_atr_col_to_df(
    df: pd.DataFrame, n: int = ATR_SMOOTHING_N, exponential: bool = False
) -> pd.DataFrame:
    """
    Add ATR (Average True Range) column to DataFrame.
    Average True Range is a volatility estimate.
    n - number of periods.
    If exponential is true,
    use ewm - exponentially weighted values,
    to give more weight to the recent data point.
    Otherwise, calculate simple moving average.
    """

    data = df.copy(deep=True)
    high = data["High"]
    low = data["Low"]
    close = data["Close"]
    data["tr0"] = abs(high - low)
    data["tr1"] = abs(high - close.shift())
    data["tr2"] = abs(low - close.shift())
    data["tr"] = data[["tr0", "tr1", "tr2"]].max(axis=1)
    data["tr"] = round(data["tr"], 2)

    # today use yesterday's ATR -
    # this operation is currently essential, maybe remove later
    data["tr"] = data["tr"].shift()

    if exponential:
        data[f"atr_{n}"] = (
            data["tr"].ewm(alpha=2 / (n + 1), min_periods=n, adjust=False).mean()
        )
    else:
        data[f"atr_{n}"] = data["tr"].rolling(window=n, min_periods=n).mean()
    data[f"atr_{n}"] = round(data[f"atr_{n}"], 2)
    del data["tr0"]
    del data["tr1"]
    del data["tr2"]
    # del data["tr"]
    return data
