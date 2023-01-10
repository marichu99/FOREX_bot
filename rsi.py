import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import numpy as np    
from threading import Thread
import json
from email.message import EmailMessage 

SYMBOL = ["XAUUSD","EURUSD","USDCAD","USDJPY","AUDCAD","GBPUSD","GBPJPY","EURJPY"]
TIMEFRAME = mt5.TIMEFRAME_M15  
high_TIMEFRAME=[mt5.TIMEFRAME_M30,mt5.TIMEFRAME_M15,mt5.TIMEFRAME_H1,mt5.TIMEFRAME_H4]
VOLUME=0.1
N=0
AWAIT_=False
mar=""
mar1=""
standa=float(0.0)
standa1=float(0.0)
# HIGH PRICE DICTIONARY
# counterHigh value dictionary
counterHigh={"XAUUSD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"EURUSD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"USDCAD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"USDJPY":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"AUDCAD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}}
xau_DictHigh={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}
eur_DictHigh={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}
jpy_DictHigh={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}
cad_DictHigh={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}
aud_DictHigh={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}


# LOW PRICE DICTIONARY
# counterHigh value dictionary
counterLow={"XAUUSD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"EURUSD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"USDCAD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"USDJPY":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"AUDCAD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}}
            
xau_DictLow={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}
eur_DictLow={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}
jpy_DictLow={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}
cad_DictLow={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}
aud_DictLow={1:{15:[],30:[],16385:[],16388:[]},
             2:{15:[],30:[],16385:[],16388:[]},
             3:{15:[],30:[],16385:[],16388:[]},
             4:{15:[],30:[],16385:[],16388:[]},
             5:{15:[],30:[],16385:[],16388:[]},
             6:{15:[],30:[],16385:[],16388:[]},
             7:{15:[],30:[],16385:[],16388:[]},
             8:{15:[],30:[],16385:[],16388:[]},
             9:{15:[],30:[],16385:[],16388:[]},
             10:{15:[],30:[],16385:[],16388:[]},
             11:{15:[],30:[],16385:[],16388:[]},
             12:{15:[],30:[],16385:[],16388:[]}}


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
symbol_info=pd.DataFrame(
    
)

def conn():
    # start the connection to MT5
    valid_conn= mt5.initialize()
    # check if the connection went through
    if not (valid_conn):
        print(f"The initialisation error is {mt5.last_error()}")
    account = int(36610) 
    # 810403203
    password= "Marichu12"
    server ="EGMSecurities-Demo"
    # login into your account 
    login = mt5.login(account,password,server)
    if not login:
        print(f"The login error was{mt5.last_error()}")
        return "no success"
    else:
        print("login Successful")
        orders=mt5.positions_get()
        if orders == None :
            print(f"The are no open positions")
        elif len(orders)>=1:
            print("We have some open positions")
            df_positions=pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())[["symbol","profit","sl","tp","volume","price_open"]]
            
            df_positions.rename(columns={"symbol":"Symbol"},inplace=True)
            df_positions["id"]=df_positions.index
            print(df_positions)
            this_Dict=df_positions.to_dict("list")            
            print(this_Dict)
            return "success"
        


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
    if mt5.positions_total() == 4:
        while True:
            orders=mt5.positions_get()
            if orders == None :
                print(f"The are no open positions")
            elif len(orders)>=1:
                df_positions=pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())[["symbol","profit","sl","tp","volume"]]
                # print(df_positions)
                this_Dict=df_positions.to_dict()
                # print(this_Dict)
            time.sleep(5)
       

# signal generating functions   
def get_signal(TIMEFRAMEs):
    # bar data
    bars =mt5.copy_rates_from_pos(J,TIMEFRAMEs,1,NUM_BARS)
    # converting to dataframe
    df =pd.DataFrame(bars)
    # print(f"The symbol is {J}")
    df=df.tail(20)
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

    # print(f"The last price is {last_price} and upper band is {upper_band} and the lower band is {lower_band}")
    # print(df)
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
    df=df[df["time"]> "2021-05-01"]
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
    current_price=df.iloc[-1]["close"]
    previous_price=df.iloc[-2]["close"]

    
    # low RSI dataframe
    data=df[df["rd_14"] <=30]
    lowRSI=pd.DataFrame(data=data)[["rd_14","close"]]
    # print("LOW RSI DATAFRAME ")
    # print(lowRSI.tail(20))
    getDivergence(highRSI,lowRSI,TIMEFRAMEs)

    return atr,rd_14
def await_Confirmation(TIMEFRAMEs,standa1,x,type):
    global AWAIT_
    setAwait(True)
    while True:
        mabao=mt5.copy_rates_from_pos(J,TIMEFRAMEs,STARTT_POS,NUM_BARS)
        detaFremu=pd.DataFrame(data=mabao)[["close","open","high","low","time"]]
        current_price=detaFremu.iloc[-1]["close"]
        print(f"The current price is {current_price}")
        previous_price=detaFremu.iloc[-2]["close"]
        print(f"The previous price is {previous_price}")
        latter_price=detaFremu.iloc[-3]["close"]
        
        tick=mt5.symbol_info_tick(J)
        print(f"The type is {type}")
        if type == "buy":
            if current_price >previous_price:
                if previous_price > latter_price:
                    # buy order 
                    market_order(J,VOLUME,'buy',DEVIATION,MAGIC,tick.ask -SL_SD *standa1,tick.bid +TP_SD*standa1)
                else: 
                    break
        elif type == "sell":
            if current_price<previous_price:
                if previous_price<latter_price:
                    # sell order
                    market_order(J,VOLUME,"sell",DEVIATION,MAGIC,tick.bid +x,tick.ask-TP_SD*standa1)
                else: 
                    break
    time.sleep(7)

# get the bullish and bearish divergence
def getDivergence(highRSI,lowRSI,TIMEFRAMEs):
    global trade_signal
    # print("LOW RSI")
    # print(lowRSI)

    # HIGH PRICE
    current_high_rsi=highRSI.iloc[-1]["rd_14"]
    current_close_high=highRSI.iloc[-1]["close"]
    previous_high_rsi=highRSI.iloc[-2]["rd_14"]
    previous_close_high=highRSI.iloc[-2]["close"]
    # highest price
    highest_price =highRSI.loc[highRSI["close"]==highRSI["close"].max()]
    highest_price=highest_price.iloc[-1]["close"]
    
    def fillDict(we,you,vecna):
        from_date=datetime(2022,x,v)
        to_date=datetime(2022,x,v+1)
        mbao=mt5.copy_rates_range(we,you,from_date,to_date)
        detFrem=pd.DataFrame(mbao)[["close","open","high","low","time"]]
        detFrem["time"]=pd.to_datetime(detFrem["time"],unit="s")

        if we=="XAUUSD": 
            # if the length of gold is below 2 elements, 
            if len(xau_DictHigh[x][you]) <2:
                # append to the high dictionary
                xau_DictHigh[x][you].append(vecna)
                # append the length of the gold high dictionary at a specific timeframe to the counterHigh dictionary
                counterHigh[we][you]=(len(xau_DictHigh[x][you]))
                counterXH=counterHigh[we][you]
            elif len(xau_DictHigh[x][you])>2:
               if xau_DictHigh[x][you][counterXH] != xau_DictHigh[x][you][counterXH-1]:
                xau_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(xau_DictHigh[you][x]))
                counterXH=counterHigh[we][you]
        if we =="EURUSD":
            if len(eur_DictHigh[x][you])<2:
                eur_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(eur_DictHigh[x][you]))
                counterEH=counterHigh[we][you]
            elif len(eur_DictHigh[x][you])>2:
              counterEH=counterHigh[we][you]
              if eur_DictHigh[x][you][counterEH] != eur_DictHigh[x][you][counterEH-1]:
                eur_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(eur_DictHigh[x][you]))
                counterEH=counterHigh[we][you]
        if we =="USDCAD":
            if len(cad_DictHigh[x][you])<2:
                cad_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(cad_DictHigh[x][you]))
                counterCH=counterHigh[we][you]
            elif len(cad_DictHigh[x][you])>2:
             counterCH=counterHigh[we][you]
             if  cad_DictHigh[x][you][counterCH] != cad_DictHigh[x][you][counterCH-1]:
                cad_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(cad_DictHigh[x][you]))
                counterCH=counterHigh[we][you]
        if we =="USDJPY":
            if len(jpy_DictHigh[x][you])<2:
                jpy_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(jpy_DictHigh[x][you]))
                counterJH=counterHigh[we][you]
            elif len(jpy_DictHigh[x][you])>2:
             counterJH=counterHigh[we][you]
             if jpy_DictHigh[x][you][counterJH] != jpy_DictHigh[x][you][counterJH-1]:
                jpy_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(jpy_DictHigh[x][you]))
                counterJH=counterHigh[we][you]
        if we =="AUDCAD":
            if len(aud_DictHigh[x][you])<2:
                aud_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(aud_DictHigh[x][you]))
                counterAH=counterHigh[we][you]
            elif len(aud_DictHigh[x][you])>2:
             counterAH=counterHigh[we][you]
             if aud_DictHigh[x][you][counterAH] != aud_DictHigh[x][you][counterAH-1]:
                aud_DictHigh[x][you].append(vecna)
                counterHigh[we][you]=(len(aud_DictHigh[x][you]))
                counterAH=counterHigh[we][you]
    def fillDictLow(we,you,vecna):
        from_date=datetime(2022,x,v)
        to_date=datetime(2022,x,v+1)
        mbao=mt5.copy_rates_range(we,you,from_date,to_date)
        detFrem=pd.DataFrame(mbao)[["close","open","high","low","time"]]
        detFrem["time"]=pd.to_datetime(detFrem["time"],unit="s")
        if we=="XAUUSD":
            if len(xau_DictLow[x][you]) <2:
                xau_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(xau_DictLow[x][you]))
                counterXL=counterLow[we][you]
            elif len(xau_DictLow[x][you])>2:
             counterXL=counterLow[we][you]
             if xau_DictLow[x][you][counterXL] != xau_DictLow[x][you][counterXL-1]:
                xau_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(xau_DictLow[x][you]))
                counterXL=counterLow[we][you]
            # print(f"The counter value on GOLD low Dict is {counterXL}")
            # print(f"The Gold Low Dictionary is {xau_DictLow }")
            # print(f"The length of Gold'd low dictionary is {len(xau_DictLow[x][you])}")
            # print(f"NUM BARS IS {NUM_BARS}")
        if we =="EURUSD":
            if len(eur_DictLow[x][you])<2:
                eur_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(eur_DictLow[x][you]))
                counterEL=counterLow[we][you]
                print(f"EL counter value {counterEL}")
            elif len(eur_DictLow[x][you])>2:
             counterEL=counterLow[we][you]
             if eur_DictLow[x][you][counterEL] != eur_DictLow[x][you][counterEL-1]:
                eur_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(eur_DictLow[x][you]))
                counterEL=counterLow[we][you]
        if we =="USDCAD":
            if len(cad_DictLow[x][you])<2:
                cad_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(cad_DictLow[x][you]))
                counterCL=counterLow[we][you]
            elif len(cad_DictLow[x][you])>2:
             counterCL=counterLow[we][you]
             if cad_DictLow[x][you][counterCL] != cad_DictLow[x][you][counterCL-1]:
                cad_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(cad_DictLow[x][you]))
                counterCL=counterLow[we][you]                
        if we =="USDJPY":
            if len(jpy_DictLow[x][you])<2:
                jpy_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(jpy_DictLow[x][you]))
                counterJL=counterLow[we][you]
            elif len(jpy_DictLow[x][you])>2:
             counterJL=counterLow[we][you]
             if jpy_DictLow[x][you][counterJL] != jpy_DictLow[x][you][counterJL-1]:
                jpy_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(jpy_DictLow[x][you]))
                counterJL=counterLow[we][you]
        if we =="AUDCAD":
            if len(aud_DictLow[x][you])<2:
                aud_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(aud_DictLow[x][you]))
                counterAL=counterLow[we][you]
            elif len(aud_DictLow[x][you])>2:
             counterAL=counterLow[we][you]  
             if aud_DictLow[x][you][counterAL] != aud_DictLow[x][you][counterAL-1]:
                aud_DictLow[x][you].append(vecna)
                counterLow[we][you]=(len(aud_DictLow[x][you]))
                counterAL=counterLow[we][you]      
        # create a separate file and save the backtest data
        # bTest=pd.DataFrame(xau_DictHigh)
        #   bTest.to_csv(r"C:/xampp/htdocs/Python/FOREX", index=False)

            

    # checking for highest price in the higher timeframes and updating the highprice dictionary for structure analysis
    if TIMEFRAMEs in [15,30,16385,16388]:
        if N == 15:
            t_type="15 min timeframe"
            # print(f"The highest price in {t_type}")
            # print(highest_price)
            fillDict(we=J,you=N,vecna=highest_price)
        elif N == 30:
            t_type="30 min timeframe"
            # print(f"The highest price in {t_type}")
            # print(highest_price)
            fillDict(we=J,you=N,vecna=highest_price)
        elif N == 16385:
            t_type="1 hour timeframe"
            # print(f"The highest price in {t_type}")
            # print(highest_price)
            fillDict(we=J,you=N,vecna=highest_price)
        elif N==16388:
            t_type="4 Hour timeframe"
            # print(f"The highest price in {t_type}")
            # print(highest_price)
            fillDict(we=J,you=N,vecna=highest_price)
    
    # LOW PRICE 
    current_low_rsi=lowRSI.iloc[-1]["rd_14"]
    current_close_low=lowRSI.iloc[-1]["close"]
    previous_low_rsi=lowRSI.iloc[-2]["rd_14"]
    previous_close_low=lowRSI.iloc[-2]["close"]
    lowestPrice=lowRSI.loc[lowRSI["close"]==lowRSI["close"].max()]
    lowestPrice=lowestPrice.iloc[-1]["close"]
    # checking for lowest price in the higher timeframes and updating the low price dictionary for structure analysis
    if TIMEFRAMEs in [15,30,16385,16388]:
        if N == 15:
            t_type="15 min timeframe"
            # print(f"The highest price in {t_type}")
            # print(lowestPrice)
            fillDictLow(we=J,you=N,vecna=lowestPrice)
        elif N == 30:
            t_type="30 min timeframe"
            # print(f"The highest price in {t_type}")
            # print(lowestPrice)
            fillDictLow(we=J,you=N,vecna=lowestPrice)
        elif N == 16385:
            t_type="1 hour timeframe"
            # print(f"The highest price in {t_type}")
            # print(lowestPrice)
            fillDictLow(we=J,you=N,vecna=lowestPrice)
        elif N==16388:
            t_type="4 Hour timeframe"
            # print(f"The highest price in {t_type}")
            # print(lowestPrice)
            fillDictLow(we=J,you=N,vecna=lowestPrice)
   
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
        global CROSS_OVER
        CROSS_OVER="bullish_cross_over"
        return "bullish_crossover"

    elif fast_sma<slow_sma and prev_fast_sma >slow_sma:
        CROSS_OVER="bearish_crossover"
        return "bearish_crossover"   

def setAwait(booly):
    global AWAIT_
    AWAIT_=booly
def await_Details(type):
    if J in ["USDJPY","GBPJPY","EURJPY"]:
        SL=0.50
    else:
        SL=0.0050
    current_price=dfs.iloc[-1]["close"]
    print(f"The current price is {current_price}")
    previous_price=dfs.iloc[-2]["close"]
    print(f"The previous price is {previous_price}")
    latter_price=dfs.iloc[-3]["close"]
    
    tick=mt5.symbol_info_tick(J)
    print(f"The type is {type}")
    if type == "buy":
        if current_price >previous_price:
            if previous_price > latter_price:
                # buy order 
                market_order(J,VOLUME,'buy',DEVIATION,MAGIC,tick.ask -SL_SD *standa1,tick.bid +TP_SD*standa1)
             
                
    elif type == "sell":
        if current_price<previous_price:
            if previous_price<latter_price:
                # sell order
                market_order(J,VOLUME,"sell",DEVIATION,MAGIC,tick.bid +x,tick.ask-TP_SD*standa1)
             
                
def main():
    
    connection=conn()
    # strategy loop
    print(f"The connection is {connection}")
        
    resy={
        "Symbol":"",
        "Type":"",
        "Multi-Time Frame":""
    }
    def wholeThing(): 
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
                # print(N)
                global v
                global x
                # x and v are variables used to control dates, which are in turn used to control short and long term price dataframe es
                v=int(1)
                v=v+1
                x=int(5)
                if v >29:
                    x=x+1
                    v= int(1)
                    if x > 11:
                        x=int(1)
                        v=int(1)
            
              # if no positions are open
                if mt5.positions_total() <4:
                    # get the bolinger band signal
                    global J
                    J=j
                    
                    global NUM_BARS
                    bars =mt5.copy_rates_from_pos(J,TIMEFRAME,1,NUM_BARS)
                    
                    # converting to dataframe
                    global dfs
                    dfs =pd.DataFrame(bars)  
                    # print(dfs) 
                    current_price=dfs.iloc[-1]["close"] 
                    current_price_high=dfs.iloc[-1]["high"]
                    current_price_low=dfs.iloc[-1]["low"]
                    previous_price=dfs.iloc[-2]["close"]
                    previous_price_high=dfs.iloc[-2]["high"]
                    previous_price_low=dfs.iloc[-2]["low"]
                    previous_price_open=dfs.iloc[-2]["open"]
                    latter_price=dfs.iloc[-3]["close"]
                    latter_price_high=dfs.iloc[-3]["high"]
                    latter_price_low=dfs.iloc[-3]["low"]
                    # bearish candle
                    if previous_price<previous_price_open:
                        if (previous_price_high-previous_price_open) > (previous_price-previous_price_low):
                            pinbar="bearish"
                    # bullish candle
                    if previous_price>previous_price_open:
                        if (previous_price_high-previous_price_open) < (previous_price-previous_price_low):
                            pinbar="bullish"
                    if current_price<previous_price and previous_price<latter_price:
                        t_sell=True
                    elif current_price>previous_price and previous_price>latter_price:
                        t_buy=True
                    # we are trying to get price data on different pairs
                    xau=mt5.symbol_info(J)._asdict()
                    gold=pd.DataFrame.from_dict([xau])[["ask","bid"]]
                    gold.index=J
                    print(gold)
                    orders=mt5.positions_get()
                    if orders == None :
                        print(f"The are no open positions")
                    elif len(orders)>=1:
                        df_positions=pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())[["symbol","profit","sl","tp","volume"]]
                        # print(df_positions)
                        this_Dict=df_positions.to_dict()
                        # print(this_Dict)
                        with open("data1.json","w") as posit:
                            json.dump(this_Dict,posit)
                    signal, standard_deviation =get_signal(TIMEFRAMEs=s)
                    
                    if signal != None and standard_deviation !=None:
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
                                mar1,standa1 =get_signal(TIMEFRAMEs=TIMEFRAME)
                                if mar1!= None and standa1!=None:
                                    print("We have a multitimeframe buy signal")
                                    resy["Type"]="buy"
                                    resy["Symbol"]=J
                                    resy["Multi-Time Frame"]="NOT"
                                    
                                        
                                atrr1,rsii1= calculateRSI(TIMEFRAMEs=TIMEFRAME)
                                atrr1=atrr1*100
                                if J in ["USDJPY","GBPJPY","EURJPY"]:
                                        SL=0.50
                                else:
                                        SL=0.0050
                                if mar1 =="buy" and standa1 != None and rsii1 <30:   
                                    print("Multi- Time frame signal to buy low")
                                    resy["Type"]="buy"
                                    resy["Symbol"]=J
                                    resy["Multi-Time Frame"]="YES"
                                        # candle stick confirmation
                                    # if t_buy==True or pinbar== "bullish":
                                    market_order(J,VOLUME,'buy',DEVIATION,MAGIC,tick.ask -SL_SD *standa1,tick.bid +TP_SD*standa1)                 
                                    # market_order(J,VOLUME,'buy',DEVIATION,MAGIC,tick.ask -SL_SD *standa1,tick.bid +TP_SD*standa1)
                            elif signal == "sell" and rsi>70 or trade_signal =="sell":
                                # check for a sell signal on the lower timeframes
                                mar,standa =get_signal(TIMEFRAMEs=TIMEFRAME)
                                if mar != None and standa != None:
                                    print("We have multitimeframe sell signal")
                                atrr,rsii= calculateRSI(TIMEFRAMEs=TIMEFRAME)
                                atrr=atrr*100  
                                if J in ["USDJPY","GBPJPY","EURJPY"]:
                                        SL=0.50
                                else:
                                        SL=0.0050
                                if mar =="sell" and standa != None and rsii >70:
                                     print("Multi-timeframe signal to sell high")
                                    #  if t_sell==True and pinbar== "bearish":
                                     market_order(J,VOLUME,"sell",DEVIATION,MAGIC,tick.bid +x,tick.ask-TP_SD*standa)
                                    #  market_order(J,VOLUME,"sell",DEVIATION,MAGIC,tick.bid +SL,tick.ask-TP_SD*standa)
                            elif trade_signal == "buy" and signal !=None:
                                market_order(J,VOLUME,'buy',DEVIATION,MAGIC,tick.ask -SL ,tick.bid +TP_SD*standard_deviation)
                            elif trade_signal == "sell" and signal != None:
                                market_order(J,VOLUME,"sell",DEVIATION,MAGIC,tick.bid +SL,tick.ask-TP_SD*standard_deviation)
                                                 
            # check for signal every 5 seconds
                with open("data.json","w") as dataF:
                    json.dump(resy,dataF)
    if connection == "success":
        wholeThing()  
    time.sleep(12)
main()



    

