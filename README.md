# QuantInsti_Inter_IIT_12.0
Hypothesis : 

We’ve used a simple price action trading strategy to place buy and sell orders on our portfolio. 
A candle has 4 prices : open,high,low and close. When the open and close prices are close, within a certain value epsilon2, where

epsilon2 = 0.001*current close price of the stock

we will  generate a buy signal if the difference between the low price and the minimum of the close and open prices lies within a certain range epsilon1, where

epsilon1 = 0.01*current close price of the stock

and we will generate a sell signal if the difference between the high price and the maximum of the close and open prices lies within a certain range epsilon1, which is again : 

epsilon1 = 0.01*current close price of the stock
Note that the current close price of the stock denotes the current price of the stock, taken from the OHLC data of the last one minute.

We’ve considered the 15 min and 5 min OHLC data of the stocks. Since in blueshift only 1 min and 1 day historical data is available, we have extracted 5 min and 15 OHLC data for testing our hypothesis. 

—-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Testing:

We have tested our hypothesis on the top 10 BANKNIFTY stocks - HDFCBANK ,ICICIBANK, KOTAKBANK ,SBIN, AXISBANK, INDUSINDBK, BANKBARODA , FEDERALBNK, IDFCFIRSTB ,PNB

The testing period is from 1 JULY 2017 to 1 JULY 2022, on NSE stock data with a capital of Rs 10000

The results obtained were:

Returns: -10.85%
Alpha: 0.06
Beta: 0.42
Sharpe: -0.12
Drawdown: -24.21%
