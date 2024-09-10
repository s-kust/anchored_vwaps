import pandas as pd


def get_ohlc_from_av(
    ticker: str, period: str = "2y", interval: str = "1d"
) -> pd.DataFrame:
    pass


# TODO implement similar to get_ohlc_from_yf,
# as a backup data provider in case of Yahoo Finance failure.
