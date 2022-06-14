
import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import numpy as np
from threading import Thread


SYMBOL = ["XAUUSD","EURUSD","USDCAD","USDJPY","AUDCAD"]
TIMEFRAME = mt5.TIMEFRAME_M1  
high_TIMEFRAME=[mt5.TIMEFRAME_M30,mt5.TIMEFRAME_M15,mt5.TIMEFRAME_H1,mt5.TIMEFRAME_H4]
VOLUME=0.1
N=0

J=""
STARTT_POS=0
NUM_BARS=1000
DEVIATION =20 # deviation for order slippage
MAGIC =10
SMA_PERIOD=20
STANDARD_DEVIATIONS=int(2) # number of deviations for calculation of bolinger bands
TP_SD =int(3)   # number of deviations for take profit
SL_SD =int(2) # number of deviations for stop loss
FSMA_PERIOD = 10 # number of periods in the fast simple moving average
SL_SMA_PERIOD = 50 # number of periods in the slow moving average
CROSS_OVER=""
trade_signal=""
def conn():
    # start the connection to MT5
    valid_conn= mt5.initialize()
    # check if the connection went through
    if not (valid_conn):
        print(f"The initialisation error is {mt5.last_error()}")
    account = int(810414810)
    # 810403203
    password= "Marichu12"
    server ="EGMSecurities-Live"
    # login into your account 
    login = mt5.login(account,password,server)
    if not login:
        print(f"The login error was{mt5.last_error()}")
    else:
        print("login Successful")


# make an order from the terminal
def market_order(symbol,volume,order_type,deviation,magic,stoploss,takeprofit):
    tick =mt5.symbol_info_tick(symbol)

    order_dict ={"buy":0,"sell":1}
    price_dict ={"buy":tick.ask,"sell":tick.bid}
    if order_type == "buy":
        taip=mt5.ORDER_TYPE_BUY
    elif order_type == "sell":
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
       

# signal generating functions
def get_signal(TIMEFRAMEs):
    # bar data
    bars =mt5.copy_rates_from_pos(J,TIMEFRAMEs,1,SMA_PERIOD)
    # converting to dataframe
    df =pd.DataFrame(bars)
    print(f"The symbol is {J}")
    # simple moving average
    sma =df['close'].mean()
    # standard deviation
    sd =df['close'].std()
    
    # lower bolinger band
    lower_band = sma -STANDARD_DEVIATIONS*sd
    # upper bolinger band
    upper_band = sma +STANDARD_DEVIATIONS*sd

    # last close price
    last_price =df.iloc[-1]["close"]

    print(f"The last price is {last_price} and upper band is {upper_band} and the lower band is {lower_band}")
    # finding the signal
    if last_price <lower_band: 
        return 'buy',sd
    elif last_price > upper_band:
        return 'sell',sd
    else: 
        return None, None
# calculate the RSI
def calculateRSI(TIMEFRAMEs):
    bars=mt5.copy_rates_from_pos(J,TIMEFRAMEs,STARTT_POS,NUM_BARS)
    
    df=pd.DataFrame(bars)[['time','open','high','low','close']]
    df['time']=pd.to_datetime(df["time"],unit='s')
    df=df[df["time"]> "2022-05-01"]
    close_delta=df["close"].diff()
    # make two series: one for lower closes and one for higher closes
    up=close_delta.clip(lower=0)
    down=-1*close_delta.clip(upper=0)

    # setting the RSI period
    rsi_period=14
    # to calculate RSI, we first need to calculate the simple weighted average gain and loss during the period
    df['gain']=(df['close']-df['open']).apply(lambda x: x if x>0 else 0)
    df['loss']=(df['close']-df['open']).apply(lambda x: -x if x<0 else 0)
    # we calculate the exponential moving average
    # df["ema_gain"]=up.rolling(rsi_period).mean()
    # df["ema_loss"]=down.rolling(rsi_period).mean()
    df["ema_gain"]=df["gain"].ewm(span=rsi_period,min_periods=rsi_period).mean()
    df["ema_loss"]=df["loss"].ewm(span=rsi_period,min_periods=rsi_period).mean()
    """
      Calculating the SMA for the symbol in the minute timeframe
    """
    # calculating the simple moving average
    df["fast_sma"]=df["close"].rolling(FSMA_PERIOD).mean()
    df["slow_sma"]=df["close"].rolling(SL_SMA_PERIOD).mean()
    # calculate the previous SMA
    df["prev_fast_sma"]=df["fast_sma"].shift(1)
    # crossover column
    df=df.fillna(0)
    df["crossover"]= np.vectorize(calculateSMA)(df["fast_sma"],df["prev_fast_sma"],df["slow_sma"])
    # the Relative strength is gotten by dividing the exponential average gain witb the exponential average loss
    df['RS']=df['ema_gain']/df['ema_loss']
    # the RSI is calculated based on the RS using the following formula
    df['rd_14']=100-(100/(df['RS']+1))
    # print(df)
    
    # define the ATR period
    atr_period=14
    # calculating the range of each candle
    df['range']=df['high']-df['low']
    # calculating the average value of ranges
    df['atr_14']=df['range'].rolling(atr_period).mean()
    # print(df)
    atr=df.iloc[-1]["atr_14"]
    rd_14=df.iloc[-1]["rd_14"]
    """
     Calculate the RSI divergence by getting the max RSI and min RSI in the periods
     Then call the getDivergence() function
    """
    data1=df[df["rd_14"] >= 70]
    highRSI=pd.DataFrame(data=data1)[["rd_14","close"]]
    # filter to the last 20 bars
    
    # print("HIGH RSI DATAFRAME ")
    # print(highRSI.tail(20))
    
    # low RSI dataframe
    data=df[df["rd_14"] <=30]
    lowRSI=pd.DataFrame(data=data)[["rd_14","close"]]
    # print("LOW RSI DATAFRAME ")
    # print(lowRSI.tail(20))
    getDivergence(highRSI,lowRSI)

    return atr,rd_14

# get the bullish and bearish divergence
def getDivergence(highRSI,lowRSI):
    global trade_signal
    # print("LOW RSI")
    # print(lowRSI)

    # HIGH PRICE
    current_high_rsi=highRSI.iloc[-1]["rd_14"]
    current_close_high=highRSI.iloc[-1]["close"]
    previous_high_rsi=highRSI.iloc[-2]["rd_14"]
    previous_close_high=highRSI.iloc[-2]["close"]

    # LOW PRICE 
    current_low_rsi=lowRSI.iloc[-1]["rd_14"]
    current_close_low=lowRSI.iloc[-1]["close"]
    previous_low_rsi=lowRSI.iloc[-2]["rd_14"]
    previous_close_low=lowRSI.iloc[-2]["close"]
    
    # logic
    """
    if current_close_high is in the range of the previous_close_high or higher than it
    And the current high rsi is lower than the previous high rsi, then there is a bearish divergence
    THE CONVERSE OF THE ABOVE ALSO APPLIES 
    """
    higher_side =current_close_high-0.8
    lower_side =current_close_low -0.8
    
    if higher_side >= previous_close_high and current_high_rsi<previous_high_rsi:
        trade_signal="sell"
        
         
                
    elif lower_side >= previous_close_low and current_low_rsi>previous_low_rsi:
        trade_signal="buy"
        
    

# calculating the SMA
def calculateSMA(fast_sma,prev_fast_sma,slow_sma): 
    """
      The main logic behind sma crossover is that if the previous fast_sma is lesser than the current 
      slow_sma this means that the is a bullish crossover which signifies a buy signal 
      And the converse is also True
    """
    # logic
    if fast_sma>slow_sma and prev_fast_sma< slow_sma:
        CROSS_OVER="bullish_cross_over"
        return "bullish_crossover"

    elif fast_sma<slow_sma and prev_fast_sma >slow_sma:
        CROSS_OVER="bearish_crossover"
        return "bearish_crossover"


   
def main():
    conn()
    # strategy loop
    while True:
        for j in  SYMBOL:
              for s in high_TIMEFRAME:
                global N
                N=s
                if N == 15:
                    t_type="15 min timeframe"
                elif N == 30:
                    t_type="30 min timeframe"
                elif N == 16385:
                    t_type="1 hour timeframe"
                elif N==16388:
                    t_type="4 Hour timeframe"
                print(N)
            
        # if no positions are open
                if mt5.positions_total() <4:
                    # get the bolinger band signal
                    global J
                    J=j
                    signal, standard_deviation =get_signal(TIMEFRAMEs=TIMEFRAME)
                    if signal != "None" and standard_deviation != "None":
                        print(f"The signal is {signal} and the standard deviation is {standard_deviation}")
                        print(f"The symbol is {J} and the Timeframe is {t_type}")
                    # get the rsi and atr signals
                    atr,rsi =calculateRSI(TIMEFRAMEs=N)
                    atr=atr*100
                    if atr >0 and rsi >0:
                        print(f"The RSI is {rsi} and the ATR is {atr} at the {t_type}")            
                    tick =mt5.symbol_info_tick(J)
                    # get the rsi divergence

                    if signal == "buy" and rsi <30 or trade_signal =="buy":
                        # check for a buy signal on the lower timeframes
                        mar,standa =get_signal(TIMEFRAMEs=TIMEFRAME)
                        atrr,rsii= calculateRSI(TIMEFRAMEs=TIMEFRAME)
                        atrr=atrr*100
                        if mar =="buy" and standa !="None" and rsii <30:
                         market_order(J,VOLUME,'buy',DEVIATION,MAGIC,tick.ask -SL_SD *standard_deviation,tick.bid +TP_SD*standard_deviation)
                    elif signal == "sell" and rsi>70:
                        # check for a sell signal on the lower timeframes
                        mar,standa =get_signal(TIMEFRAMEs=TIMEFRAME)
                        atrr,rsii= calculateRSI(TIMEFRAMEs=TIMEFRAME)
                        atrr=atrr*100
                        if mar =="sell" and standa !="None" and rsii >70:
                         market_order(J,VOLUME,"sell",DEVIATION,MAGIC,tick.bid +SL_SD*standard_deviation,tick.ask-TP_SD*standard_deviation)
                    elif trade_signal == "buy" and signal !="None":
                        market_order(J,VOLUME,'buy',DEVIATION,MAGIC,tick.ask -SL_SD * standard_deviation,tick.bid +TP_SD*standard_deviation)
                    elif trade_signal == "sell" and standard_deviation != None:
                        market_order(J,VOLUME,"sell",DEVIATION,MAGIC,tick.bid +SL_SD*standard_deviation,tick.ask-TP_SD*standard_deviation)
             
        # check for signal every 20 seconds
        time.sleep(5)
main()



    

