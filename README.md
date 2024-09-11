# Python Code to Plot Anchored VWAPs

This repository provides Python code for adding anchored VWAPs to OHLC data, generating charts, and saving them as `.png` files. It can help you apply the trading strategies described in Brian Shannon's book, *Maximum Trading Gains with Anchored VWAP*. The precondition is that you're familiar with running Python scripts and have some knowledge of Pandas. 

The principal function `vwaps_plot_build_save` is located in a file of the same name in the root folder. Additionally, the repository includes several other functions that use this function. These functions build and save daily charts and charts with intervals of 1 to 60 minutes. There are also functions in the `inport_ohlc` folder for importing OHLC data from ~~various providers~~ Yahoo Finance.

## How to Use This Repository

You can import the functions into the `run_main.py` file and run them from there. Before doing so, it's a good idea to complete the following tasks.

1. Install all required packages listed in the `requirements.txt` file, especially `kaleido`.
2. Try to understand in detail how the function `vwaps_plot_build_save` works. 
3. Check out the `draw_all_daily_charts` function. It can be helpful to run this function before the beginning of each trading day.
4. Take a look at the function `draw_daily_chart_ticker`. It will come in handy when you need to quickly draw a daily chart for some ticker. An example of its usage is in the `run_main.py` file.
5. If you want, try using the function `draw_qqq_intraday` in the `run_main.py` file for intraday trading.

## Constructing OHLC Charts with Anchored VWAPs

The primary function responsible for building and saving Anchored VWAPs charts is `vwaps_plot_build_save`. Its declaration is as follows:

```python
def vwaps_plot_build_save(
    input_df: pd.DataFrame,
    anchor_dates: List[str],
    file_name: str = DEFAULT_RESULTS_FILE,
    print_df: bool = True,
    hide_extended_hours=True,
):
```

To plot the anchored VWAPs chart, you'll need a DataFrame that contains the following columns: `Open`, `High`, `Low`, `Close`, and `Volume`. Also, you'll have to provide a list of anchor dates. Ensure the dates in the list are in text format. The function will convert them to `pd.Timestamp` internally.

### Clearing Outdated Data from the Chart

By default, the first point on the chart's X-axis will be the earliest date in the anchor dates list. To adjust this behavior, add `x` to the date you want the chart to start. For example, `x2024-08-03 00:00:00` instead of `2024-08-03 00:00:00`.

Anchored VWAPs that start from the first day of the year or the first minute of the trading day are popular and valuable. However, as the year or trading day progresses, the charts can become overburdened and less helpful. For example, the intraday chart below with a 1-minute interval, plotted towards the end of the trading day, is overcrowded. It doesn't allow us to see the details of the recent market activity.

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/intraday_QQQ_full.png" />

Use the method described above to create a new chart that isn’t cluttered with old data. This approach shows recent market activity clearly. 

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/intraday_QQQ_cut.png" />

You won’t need to increase the candle interval, such as switching from one minute to five minutes or from one day to a week.

### Understanding the Source of the Chart Title

Ideally, the `input_df` DataFrame you pass to the function should include an `attrs` attribute that stores the data for the title. The data import functions in the `import_ohlc` folder automatically add this attribute. If you import OHLC data without calling these functions, you can add and populate this attribute yourself.

## Effortlessly Tracking Your Favorite Stocks and ETFs

The `ticker_anchors.py` file contains a dictionary where you can store the tickers you're interested in, along with their anchor dates. When you run the `draw_all_daily_charts` function, it generates two updated charts for each ticker listed in the dictionary. The first chart shows anchored VWAPs starting from the dates specified in the list. The second chart includes all the data from the first chart, plus an additional anchored VWAP that starts from the `first_day_of_year`.

You can modify the value of `first_day_of_year` in the `constants.py` file. It’s generally better not to set it to the first day of the current year in January. Instead, consider waiting until February or even March before updating this value.

See also the function `draw_daily_chart_ticker`. It will come in handy when you need to quickly draw a daily chart for some ticker. An example of its usage is in the `run_main.py` file.