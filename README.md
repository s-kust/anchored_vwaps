# Python Code to Plot Anchored VWAPs

This repository provides Python code for adding anchored VWAPs to OHLC data, generating charts, and saving them as `.png` files. It can help you apply the trading strategies described in Brian Shannon's book, *Maximum Trading Gains with Anchored VWAP*. The precondition is that you're familiar with running Python scripts and have some knowledge of Pandas. 

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/daily_chart_example.png" />

The principal function `vwaps_plot_build_save` is located in a file of the same name in the root folder. Additionally, the repository includes several other functions that use this function. These functions build and save daily charts and charts with intervals of 1 to 60 minutes. There are also functions in the `import_ohlc` folder for importing OHLC data from ~~various providers~~ Yahoo Finance.

## How to Use This Repository

You can import the functions into the `run_main.py` file and run them from there. Before doing so, it's a good idea to complete the following tasks.

1. Install all required packages listed in the `requirements.txt` file, especially `kaleido`.
2. Try to understand in detail how the function `vwaps_plot_build_save` works. 
3. Check out the `draw_all_daily_charts` function. It can be helpful to run this function before the beginning of each trading day.
4. Take a look at the function `draw_daily_chart_ticker`. It will come in handy when you need to quickly draw a daily chart for some ticker. An example of its usage is in the `run_main.py` file.
5. *Advanced, optional, risky* If you want, try to use the function `draw_qqq_intraday` in the `run_main.py` file for intraday trading.

## Constructing OHLC Charts with Anchored VWAPs

The primary function responsible for building and saving Anchored VWAPs charts is `vwaps_plot_build_save`. Its declaration is as follows:

```python
def vwaps_plot_build_save(
    input_df: pd.DataFrame,
    anchor_dates: List[str],
    chart_title: str = "",
    chart_annotation_func: Callable = get_chart_annotation,
    add_last_min_max: bool = False,
    file_name: str = DEFAULT_RESULTS_FILE,
    print_df: bool = True,
    hide_extended_hours: bool = False,
):
```

To plot the anchored VWAPs chart, you'll need a DataFrame that contains the following columns: `Open`, `High`, `Low`, `Close`, and `Volume`. Also, you'll have to provide a list of anchor dates.

### Clearing Outdated Data from the Chart

By default, the first point on the chart's X-axis will be the earliest date in the anchor dates list. To adjust this behavior, add `x` to the date you want the chart to start. For example, `x2024-08-03 00:00:00` instead of `2024-08-03 00:00:00`.

Anchored VWAPs that start from the first day of the year or the first minute of the trading day are popular and valuable. However, as the year or trading day progresses, the charts can become overburdened and less helpful. For example, the intraday chart below with a 1-minute interval, plotted towards the end of the trading day, is overcrowded. It doesn't allow us to see the details of the recent market activity.

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/intraday_QQQ_full.png" />

Use the method described above to create a new chart that isn’t cluttered with old data. This approach shows recent market activity clearly. 

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/intraday_QQQ_cut.png" />

You won’t need to increase the candle interval, such as switching from one minute to five minutes or from one day to a week.

### Adding Last Min and Max Anchored VWAPS Automatically

I have found that VWAPs anchored to the dates of the last minimum and maximum are very important for swing trading. They are more significant than the *Maximum Trading Gains with Anchored VWAP* book says. Therefore, the `vwaps_plot_build_save` function acquired an additional parameter `add_last_min_max`. It saves me a lot of time and effort because I no longer have to follow and update these dates manually.

For intraday charts, VWAPs anchored to the dates of the last minimum and maximum are of little help. They are usually redundant. When building such charts, it is better not to add them.

### Customizing Chart Title and Annotation

Creating chart titles is straightforward. You can refer to the example below in the section on drawing intraday charts. Also, explore the code of the `get_custom_chart_annotation_1d` function to see what information is included in the default annotation. 

You may want to put different data in the titles and annotations of your charts. To make the annotation more informative, consider modifying the `get_custom_chart_annotation_1d` function. It is even better to create one or more custom annotation functions.

## Drawing Intraday Charts

To draw intraday charts, you can use the following function as inspiration and a starting example.

```python
def draw_qqq_intraday():
    ticker = "QQQ"
    interval = "1m"
    hist = get_ohlc_from_yf(ticker=ticker, period="2d", interval=interval)
    anchor_dates = [
        "2024-10-07 13:30:00",
        "2024-10-07 18:00:00",
        "2024-10-07 19:42:00",
    ]
    chart_title = {"ticker": ticker, "interval": interval}
    chart_title_str = str(chart_title)
    vwaps_plot_build_save(
        input_df=hist,
        anchor_dates=anchor_dates,
        chart_title=chart_title_str,
        chart_annotation_func=get_chart_annotation,
        add_last_min_max=False,
        file_name=f"intraday_{ticker}.png",
        print_df=True,
        hide_extended_hours=True,
    )
```

At the start of the trading day, you only have the initial date and time to build the first and most important Anchored VWAP. As the day progresses, other key anchor points gradually become evident.

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/intraday_1.png" />

Throughout the day, you might want to tidy up the chart by removing outdated data. Rather than increasing the candle interval, you can set one of your Anchored VWAPs as the minimum threshold for the X-axis.

For example, this is what happened after I replaced `2024-10-07 18:00:00` with `x2024-10-07 18:00:00` in the `anchor_dates` list.

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/intraday_2.png" />

It's a good idea to set the `print_df` parameter to `True`. It allows you to monitor the quality of the intraday data you receive from your provider using the DataFrame's tail displayed on the screen.

## Effortlessly Tracking Your Favorite Stocks and ETFs

The `draw_all_daily_charts` function makes it easy to build updated charts for all the tickers you're tracking. Previously, these charts primarily depended on custom anchor dates provided by the user. While the option to add custom anchor dates remains, you can now generate helpful charts without needing to specify them.

Key dates include January 1 of the current year and the dates of recent significant price highs and lows. The system automatically adds VWAPs anchored to these material dates to the chart. 

Below is an example of a daily OHLC chart that doesn't include any custom anchor dates but features a custom annotation.

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/daily_chart_example_2.png" />

Before running the `draw_all_daily_charts` function, enter the tickers you're interested in into the `tickers_follow_daily.xlsx` file. This file contains two worksheets. On the first worksheet, specify the tickers and any relevant notes, as shown in the image below. Adding notes is optional.

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/tickers_follow_1_notes.PNG" />

On the second worksheet, enter the tickers in the columns and list their custom anchor dates below them. If you place an "X" before a date, the system will use that date as the minimum threshold for the chart's X-axis.

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/tickers_follow_2_anchors.PNG" />

For every ticker you are interested in, you can specify one or more custom anchor dates or none at all. The charts remain highly useful even without custom dates. If you don't want to assign custom anchor dates, there is no need to enter that ticker on the second worksheet.

You can modify the value of `first_day_of_year` in the `constants.py` file. It’s generally better not to set it to the first day of the current year in January. Instead, consider waiting until February or even March before updating this value.

See also the function `draw_daily_chart_ticker`. It will come in handy when you need to quickly draw a daily chart for some ticker. Fill in the ticker and anchor dates, then call it as shown below.

```python
ticker = "NVDA"
anchor_dates = [
    "2024-01-01 00:00:00",
] + ["2024-08-03 00:00:00", "2024-07-11 00:00:00"]
draw_daily_chart_ticker(ticker=ticker, anchor_dates=anchor_dates)
```

Check the function code to see how the `.png` file name for saving the chart is generated.

## Visualizing the 5-Day Moving Average

Brian Shannon, author of *Maximum Trading Gains with Anchored VWAP*, emphasizes the importance of 5-day moving averages, particularly on 15-minute and 30-minute candlestick charts. You can use the `draw_5_days_avg` function to plot such charts.

Its declaration:

```python
def draw_5_days_avg(ticker: str, interval: str = "15m"):
    """
    Create and save plot 5_d_avg_{ticker}.png
    containing OHLC candles and 5 days simple moving average (SMA).
    Usage: avoid buying the dip until the price consolidates above 5 days SMA.
    For details, see Appendix B
    of the book "Maximum Trading Gains With Anchored VWAP".
    """
```

Here is an example of a chart produced by this function.

<img src="https://github.com/s-kust/anchored_vwaps/blob/main/pics/5_d_avg_IWM.png" />