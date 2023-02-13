"""
    Title: Intraday Technical Strategies
    Description: This is a long short strategy based on RSI and moving average
        dual signals
    Style tags: Momentum, Mean Reversion
    Asset class: Equities, Futures, ETFs and Currencies
    Broker: NSE
"""
import pandas as pd
from blueshift.finance import commission, slippage
from blueshift.api import(symbol,
                            order_target_percent,
                            set_commission,
                            set_slippage,
                       )
from blueshift.api import date_rules,time_rules
from blueshift.api import schedule_function

def initialize(context):
    """
        A function to define things to do at the start of the strategy
    """
    # universe selection
    context.securities = [symbol('HDFCBANK'),symbol('ICICIBANK'),symbol('KOTAKBANK')
                          ,symbol('SBIN'),symbol('AXISBANK'),symbol('INDUSINDBK'),symbol('BANKBARODA'),
                          symbol('FEDERALBNK'),symbol('IDFCFIRSTB'),symbol('PNB')]
    # define strategy parameters
    context.params = {'indicator_lookback':375,
                      'indicator_freq':'1m',
                      'buy_signal_threshold':0.5,
                      'sell_signal_threshold':-0.5,
                      'SMA_period_short':15,
                      'SMA_period_long':60,
                      'RSI_period':60,
                      'trade_freq':5,
                      'leverage':2,
                      }

    # variable to control trading frequency
    context.bar_count = 0
    
    #variable to count the number of buy/sell signals sent
    context.buy = 0
    context.sell = 0
    # variables to track signals and target portfolio
    context.signals = dict((security,0) for security in context.securities)
    context.target_position = dict((security,0) for security in context.securities)

    # set trading cost and slippage to zero
    set_commission(commission.PerShare(cost=0.0, min_trade_cost=0.0))
    set_slippage(slippage.FixedSlippage(0.00))
    #schedule_function(final_results,date_rule = date_rules.on([pd.Timestamp(2021,7,1,15,30,0)]),
                      #time_rule = time_rules.at((pd.Timestamp(2021,7,1,15,30,0)).time()))


def handle_data(context, data):
    """
        A function to define things to do at every bar
    """
    context.bar_count = context.bar_count + 1
    if context.bar_count < context.params['trade_freq']:
        return

    # time to trade, call the strategy function
    context.bar_count = 0
    run_strategy(context, data)
    #print('buy signal '+str(context.buy))
    #print('sell signal '+str(context.sell))


def run_strategy(context, data):
    """
        A function to define core strategy steps
    """
    generate_signals(context, data)
    generate_target_position(context, data)
    rebalance(context, data)

def rebalance(context,data):
    """
        A function to rebalance - all execution logic goes here
    """
    for security in context.securities:
        order_target_percent(security, context.target_position[security])

def generate_target_position(context, data):
    """
        A function to define target portfolio
    """
    num_secs = len(context.securities)
    weight = round(1.0/num_secs,2)*context.params['leverage']

    for security in context.securities:
        if context.signals[security] > context.params['buy_signal_threshold']:
            context.target_position[security] = weight
        elif context.signals[security] < context.params['sell_signal_threshold']:
            context.target_position[security] = -weight
        else:
            context.target_position[security] = 0

'''
def generate_signals(context, data):
    """
        A function to define the signal generation
    """
    try:
        close_price_data = data.current(context.securities,['close'])
        #considering the 15 minute historical data
        price_data_hist = data.historical(context.securities,['open','high','low','close'],15,"1m")
        #considering the 5 minute historical data
        #price_data_hist = data.historical(context.securities,['open','high','low','close'],5,"1m")
    except:
        return

    for security in context.securities:
        px = close_price_data.loc[security]
        #creating the ohlc data for the 15 minute duration
        ohlc_15 = {}
        ohlc_15['open'] = price_data_hist.loc[(slice(None),security),('open')][0]
        ohlc_15['close'] = price_data_hist.loc[(slice(None),security),('close')][-1]
        ohlc_15['high'] = max(price_data_hist.loc[(slice(None),security),('open','high','low','close')]
        ohlc_15['low'] = min(price_data_hist.loc[(slice(None),security),('open','high','low','close')]
        ohlc_15_df = pd.DataFrame(ohlc_15)
        context.signals[security] = signal_function(ohlc_15_df,px)

        #creating the ohlc data for the 5 minute duration
        
        ohlc_5 = {}
        ohlc_5['open'] = price_data_hist.loc[(slice(None),security),'open'][0]
        ohlc_5['close'] = price_data_hist.loc[(slice(None),security),'close'][-1]
        ohlc_5['high'] = max(price_data_hist.loc[(slice(None),security),('open','high','low','close')]
        ohlc_5['low'] = min(price_data_hist.loc[(slice(None),security),('open','high','low','close')]
        ohlc_5_df = pd.DataFrame(ohlc_15)
        context.signals[security] = signal_function(ohlc_5_df,px)
'''

def generate_signals(context,data):
    for security in context.securities:
        try:
            #print("in try block")
            close_price = data.current(security,'close')
            hist_data = data.history(security,['open','high','low','close'],15,"1m")
            #hist_data = data.history(security,['open','high','low','close'],5,"1m")
        except:
            #print("in continue block")
            continue
        #print(close_price)
        #print(hist_data)
        ohlc_15 = {}
        ohlc_15['open'] = list(hist_data['open'])[0]
        ohlc_15['close'] = list(hist_data['close'])[-1]
        ohlc_15['high'] = max(list(hist_data['high']))
        ohlc_15['low'] = min(list(hist_data['low']))
        #ohlc_5 = {}
        #ohlc_5['open'] = list(hist_data['open'])[0]
        #ohlc_5['close'] = list(hist_data['close'])[-1]
        #ohlc_5['high'] = max(list(hist_data['high']))
        #ohlc_5['low'] = min(list(hist_data['low']))
        #print(ohlc_15)
        context.signals[security] = signal_function(context,ohlc_15,close_price)
        #context.signals[security] = signal_function(context,ohlc_5,close_price)

def signal_function(context,ohlc,cp):
    """
        The main trading logic goes here, called by generate_signals above
    """
    epsilon1 = 0.01*cp
    epsilon2 = 0.001*cp
    if(abs(ohlc['close']-ohlc['open'])<epsilon2 and abs(ohlc['low'] - min([ohlc['close'],ohlc['open']]))<epsilon1):
        signal = 1
        context.buy = context.buy + 1
    elif(abs(ohlc['close']-ohlc['open'])<epsilon2 and abs(ohlc['high'] - max([ohlc['close'],ohlc['open']]))<epsilon1):
        signal = -1
        context.sell = context.sell + 1
    else:
        signal = 0
    return signal
    
def final_results(context,data):
    print('Net Buy signals : ' + str(context.buy))
    print('Net Sell Signals: ' + str(context.sell))
    