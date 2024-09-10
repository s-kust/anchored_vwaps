# Python Code to Plot Anchored VWAPs

This repository provides Python code for adding anchored VWAPs to OHLC data, generating charts, and saving them as .png files. It can help you apply the trading strategies described in Brian Shannon's book, *Maximum Trading Gains with Anchored VWAP*. The precondition is that you're familiar with running Python scripts and have some knowledge of Pandas. 

The principal function `vwaps_plot_build_save` is located in a file of the same name in the root folder. Additionally, the repository includes several other functions that use this function. These functions build and save daily charts and charts with intervals of 1 to 60 minutes. There are also functions in the `inport_ohlc` folder for importing OHLC data from ~~various providers~~ Yahoo Finance.

## How to Use This Repository

You can import the functions into the `run_main.py` file and run them from there. Before doing so, it's a good idea to complete the following tasks.

1. Install all required packages listed in the `requirements.txt` file, especially `kaleido`.
2. Try to understand in detail how the function `vwaps_plot_build_save` works. 
3. Check out the `draw_all_daily_charts` function. It can be helpful to run this function before the beginning of each trading day.
4. Take a look at the function `draw_daily_chart_ticker`. It will come in handy when you need to quickly draw a daily chart for some ticker. An example of its usage is in the `run_main.py` file.
5. If you want, try using the function `draw_qqq_intraday` in the `run_main.py` file for intraday trading.