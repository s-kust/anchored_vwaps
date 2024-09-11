import pandas as pd


def _check_df_input(df: pd.DataFrame) -> None:
    """
    Check input_df parameter of vwaps_plot_build_save function
    """
    if not hasattr(df, "attrs"):
        raise ValueError(
            "vwaps_plot_build_save: input_df must have attrs where metadata is stored"
        )
    if not df.attrs:
        raise ValueError(
            "vwaps_plot_build_save: input_df must have non-empty attrs where metadata is stored"
        )
    if "ticker" not in df.attrs:
        raise ValueError("vwaps_plot_build_save: input_df.attrs must contain ticker")
    if "interval" not in df.attrs:
        raise ValueError("vwaps_plot_build_save: input_df.attrs must contain interval")
