# Crypto-Asset-Correlations
Select a Trading Pair and view the highest and lowest correlated pairs offered on Binance. Written in python.

If you don't have Python installed: download the "Corr Comp Zip," extract and run. Exchanges installation time for a large download. The file will run as an .exe with no command prompt necessary.

Type in the trading pair with no spaces or '/' (BTCUSDT), enter an interval (1m, or 1h, or 1d, etc), and a period (10, or 20, 30, etc).
Click Submit, the program will take a minute to calculate all the correlations.
When it is done, the full list of correlation coefficients will show up to the left.
To navigate the results, click the Max or Min button to view the highest and lowest correlated pairs.
To search for a specific pair, enter the second pair under "Search Symbol" and click Search.

This program was originally meant to be run from the command line with python, with no arguments.

The Symbols txt needs to be in the same directory. It contains a raw list of all the Binance trading pairs as of 7/14/2018.
