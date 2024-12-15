import pandas as pd

from constants import ATR_MULTIPLIER, ATR_SMOOTHING_N

from .atr import add_atr_col_to_df


def fill_is_min_max(df: pd.DataFrame) -> pd.DataFrame:
    """
    Find significant minimums and maximums,
    put the True values in the corresponding rows
    of is_min and is_max columns.
    """

    internal_df = df.copy()
    internal_df["is_min"] = False
    internal_df["is_max"] = False
    if f"atr_{ATR_SMOOTHING_N}" not in internal_df.columns:
        internal_df = add_atr_col_to_df(df=internal_df)
    # if "Typical" not in df.columns:
    #     internal_df["Typical"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4
    start_date = df.index.min()
    current_candidate = {
        "extremum_to_detect": "min",  # arbitrary choice
        "date": start_date,
        "price_val": internal_df[internal_df.index == start_date]["Close"].values[0],
    }
    for i, row in (
        internal_df[internal_df.index >= current_candidate["date"]]
        .sort_index()
        .iterrows()
    ):
        if current_candidate["extremum_to_detect"] == "max":
            if row["Close"] >= current_candidate["price_val"]:
                current_candidate["price_val"] = row["Close"]
                current_candidate["date"] = i
            elif (current_candidate["price_val"] - row["Close"]) > (
                row[f"atr_{ATR_SMOOTHING_N}"] * ATR_MULTIPLIER
            ):
                internal_df.loc[
                    internal_df.index == current_candidate["date"], "is_max"
                ] = True
                current_candidate["extremum_to_detect"] = "min"
                current_candidate["date"] = i
                current_candidate["price_val"] = row["Close"]

        else:  # looking for min, current_candidate['extremum_to_detect'] == 'min'
            if row["Close"] <= current_candidate["price_val"]:
                current_candidate["price_val"] = row["Close"]
                current_candidate["date"] = i
            elif (row["Close"] - current_candidate["price_val"]) > (
                row[f"atr_{ATR_SMOOTHING_N}"] * ATR_MULTIPLIER
            ):
                internal_df.loc[
                    internal_df.index == current_candidate["date"], "is_min"
                ] = True
                current_candidate["extremum_to_detect"] = "max"
                current_candidate["date"] = i
                current_candidate["price_val"] = row["Close"]

        # internal_df.loc[internal_df.index == i, "extremum_to_detect"] = (
        #     current_candidate["extremum_to_detect"]
        # )
        # internal_df.loc[internal_df.index == i, "price_val"] = current_candidate[
        #     "price_val"
        # ]
        # internal_df.loc[internal_df.index == i, "extremum_candidate_date"] = (
        #     current_candidate["date"]
        # )

    # print(f"{current_candidate['extremum_to_detect']=}")
    # print(f"{current_candidate['price_val']=}")
    # print(f"{current_candidate['date']=}")
    # internal_df.to_csv("temp.csv")
    return internal_df
