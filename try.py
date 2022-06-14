
from datetime import datetime
import time

import MetaTrader5 as mt5
import pandas as pd


# settings
SYMBOL="XAUUSD"
TIMEFRAME=mt5.TIMEFRAME_M1 
STARTT_POS=0
NUM_BARS=28
VOLUME=0.1
DEVIATION =20 # deviation for order slippage
MAGIC =10
SMA_PERIOD=20
STANDARD_DEVIATIONS=2 # number of deviations for calculation of bolinger bands
TP_SD =2 # number of deviations for take profit
SL_SD =3 # number of deviations for stop loss

# connect to the client terminal
def conn():
    # initialise mt5
    initt= mt5.initialize()
    if not initt:
        print(f"The initialisation error was {mt5.last_error()}")
    else:
        print("initialisation done successfully")
    # login details
    account= int(810403203)
    password="Marichu12"
    server="EGMSecuritiesLive"
    # login into your account
    loginn=mt5.login(account,password,server)
    if not loginn:
        print(f"The login error was {mt5.last_error}")
    else:
        print("Login was successful")
        calculateRSI()
def calculateRSI():
    bars=mt5.copy_rates_from_pos(SYMBOL,TIMEFRAME,STARTT_POS,NUM_BARS)
    df=pd.DataFrame(bars)[['time','open','high','low','close']]
    df['time']=pd.to_datetime(df["time"],unit='s')
    df=df[df["time"]> "2022-05-01"]

    # setting the RSI period
    rsi_period=14
    # to calculate RSI, we first need to calculate the exponential weighted average gain and loss during the period
    df['gain']=(df['close']-df['open']).apply(lambda x: x if x>0 else 0)
    df['loss']=(df['close']-df['open']).apply(lambda x: -x if x<0 else 0)
    # we calculate the exponential moving average
    df['ema_gain']=df['gain'].rolling(rsi_period).mean()
    df['ema_loss']=df['loss'].rolling(rsi_period).mean()
    # the Relative strength is gotten by dividing the exponential average gain witb the exponential average loss
    df['RS']=df['ema_gain']/df['ema_loss']
    # the RSI is calculated based on the RS using the following formula
    df['rd_14']=100-(100/(df['RS']+1))
    print(df)
    # define the ATR period
    atr_period=14
    # calculating the range of each candle
    df['range']=df['high']-df['low']
    # calculating the average value of ranges
    df['atr_14']=df['range'].rolling(atr_period).mean()
    # print(df)
    atr=df.iloc[-1]["atr_14"]
    rd_14=df.iloc[-1]["rd_14"]
    return atr,rd_14


   

def marketOrder(symbol,volume,order_type,deviation,magic,stoploss,takeprofit):
    tick= mt5.symbol_info_tick(symbol)
    price_dict={"buy":tick.ask,"sell":tick.bid}
    if order_type =="buy":
        taip=mt5.ORDER_TYPE_BUY
    elif order_type =="sell":
        taip=mt5.ORDER_TYPE_SELL
    price=price_dict[order_type]
    request ={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": taip,
        "price": price,
        "deviation": deviation,
        "magic": magic,
        "sl":stoploss,
        "tp":takeprofit,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(request)
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,volume,price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
def main():
    conn()
    # strategy loop
    while True:
        tick=mt5.symbol_info_tick(SYMBOL)
        # if there are any open positions in the terminal
        total_pos=mt5.positions_total()
        if total_pos ==0:
            # check whether the rsi is less than 30 for a sell signal
            atr,rsi =calculateRSI()
            # print the atr
            atr=atr*100
            print(f"The atr is {atr} and the rsi is {rsi}")
            
            # buy
            if rsi <30:
                # stop loss and take profit for buy signal
                stop_loss=(tick.ask -2)+atr
                take_profit =(tick.bid+2)+atr
                marketOrder(SYMBOL,VOLUME,'buy',DEVIATION,MAGIC,stop_loss ,take_profit)
            elif rsi>70:
                # stop loss and take profit for sell signal
                stop_loss=(tick.bid+2)+atr
                take_profit=(tick.ask-2)+atr
                marketOrder(SYMBOL,VOLUME,'buy',DEVIATION,MAGIC,stop_loss,take_profit)
        time.sleep(10)
    # check for signal after every 10 seconds
main()
