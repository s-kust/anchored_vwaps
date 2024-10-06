import pandas as pd

from constants import ATR_SMOOTHING_N


def get_custom_chart_annotation_1d(df: pd.DataFrame) -> str:
    """
    Get custom chart annotation for OHLC daily (1d) charts
    """
    # TODO Create custom chart annotation function for intraday charts
    vwap_values = list()
    vwap_columns = [column for column in df.columns if column.startswith("A_VWAP_")]
    for vwap_column in vwap_columns:
        vwap_values.append(round(df[vwap_column].iloc[-1], 2))
    res_to_return = "VWAPs last values: " + str(sorted(vwap_values))
    res_to_return = (
        res_to_return + "; Closed last: " + str(round(df[f"Close"].values[-1], 2))
    )
    if f"atr_{ATR_SMOOTHING_N}" in df.columns:
        res_to_return = (
            res_to_return
            + f"; ATR_{ATR_SMOOTHING_N} last: "
            + str(df[f"atr_{ATR_SMOOTHING_N}"].values[-1])
        )
    return res_to_return
