import MetaTrader5 as mt5
import pandas as pd
import time 
J=""
S=""
high_TIMEFRAME=[mt5.TIMEFRAME_M30,mt5.TIMEFRAME_M15,mt5.TIMEFRAME_H1,mt5.TIMEFRAME_H4]

STARTT_POS= 0
SYMBOL=["XAUUSD","EURUSD","USDCAD","USDJPY","AUDCAD"]
NUM_BARS= int(200)

# HIGH DICTIONARY
xau_DictHigh={15:[],30:[],16385:[],16388:[]}
eur_DictHigh={15:[],30:[],16385:[],16388:[]}
cad_DictHigh={15:[],30:[],16385:[],16388:[]}
jpy_DictHigh={15:[],30:[],16385:[],16388:[]}
aud_DictHigh={15:[],30:[],16385:[],16388:[]}
# counterHigh value dictionary
counterHigh={"XAUUSD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"EURUSD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"USDCAD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"USDJPY":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"AUDCAD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}}

# low dictionary
xau_Dictlow={15:[],30:[],16385:[],16388:[]}
eur_Dictlow={15:[],30:[],16385:[],16388:[]}
cad_Dictlow={15:[],30:[],16385:[],16388:[]}
jpy_Dictlow={15:[],30:[],16385:[],16388:[]}
aud_Dictlow={15:[],30:[],16385:[],16388:[]}
# counterLow value dictionary
counterLow={"XAUUSD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"EURUSD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"USDCAD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"USDJPY":{15:int(0),30:int(0),16385:int(0),16388:int(0)}
            ,"AUDCAD":{15:int(0),30:int(0),16385:int(0),16388:int(0)}}

def conn():
    # initialise mt5
    valid_init= mt5.initialize()
    if not valid_init:
        print(f"The intialisation error was {mt5.last_error()}")
        quit()    
        # proceed to login
    account=int(810414810)
    password= "Marichu12"
    server="EGMSecurities-Live"
        # login
    login=mt5.login(account,password,server)
    if not login:
        print(f"The login error was {mt5.last_error}")
def startBackTest(TIMEFRAMEs):    
    bars=mt5.copy_rates_from_pos(J,TIMEFRAMEs,STARTT_POS,NUM_BARS)
    df=pd.DataFrame(data=bars)[["time","open","high","low","close"]]
    df["time"]=pd.to_datetime(df["time"],unit='s')
    df=df[df["time"]>"2021 *-05-01"]
    # max closing prices
    high_Close=df[df["close"]==df["close"].max()]
    highestPrice=high_Close.iloc[-1]["close"]
    # low closing prices
    low_Close=df[df["close"]==df["close"].min()]
    lowestPrice=low_Close.iloc[-1]["close"]
    # function to fill the dictionaries
    def fillDictHigh(we,you,vecna):
        if we=="XAUUSD": 
            # if the length of gold is below 2 elements, 
            if len(xau_DictHigh[you]) <2:
                # append to the high dictionary
                xau_DictHigh[you].append(vecna)
                # append the length of the gold high dictionary at a specific timeframe to the counterHigh dictionary
                counterHigh[we][you]=(len(xau_DictHigh[you]))
                counterXH=counterHigh[we][you]
            elif len(xau_DictHigh[you])>2:
               if xau_DictHigh[you][counterXH] != xau_DictHigh[you][counterXH-1]:
                xau_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(xau_DictHigh[you]))
                counterXH=counterHigh[we][you]
        if we =="EURUSD":
            if len(eur_DictHigh[you])<2:
                eur_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(eur_DictHigh[you]))
                counterEH=counterHigh[we][you]
            elif len(eur_DictHigh[you])>2:
              counterEH=counterHigh[we][you]
              if eur_DictHigh[you][counterEH] != eur_DictHigh[you][counterEH-1]:
                eur_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(eur_DictHigh[you]))
                counterEH=counterHigh[we][you]
        if we =="USDCAD":
            if len(cad_DictHigh[you])<2:
                cad_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(cad_DictHigh[you]))
                counterCH=counterHigh[we][you]
            elif len(cad_DictHigh[you])>2:
             counterCH=counterHigh[we][you]
             if  cad_DictHigh[you][counterCH] != cad_DictHigh[you][counterCH-1]:
                cad_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(cad_DictHigh[you]))
                counterCH=counterHigh[we][you]
        if we =="USDJPY":
            if len(jpy_DictHigh[you])<2:
                jpy_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(jpy_DictHigh[you]))
                counterJH=counterHigh[we][you]
            elif len(jpy_DictHigh[you])>2:
             counterJH=counterHigh[we][you]
             if jpy_DictHigh[you][counterJH] != jpy_DictHigh[you][counterJH-1]:
                jpy_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(jpy_DictHigh[you]))
                counterJH=counterHigh[we][you]
        if we =="AUDCAD":
            if len(aud_DictHigh[you])<2:
                aud_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(aud_DictHigh[you]))
                counterAH=counterHigh[we][you]
            elif len(aud_DictHigh[you])>2:
             counterAH=counterHigh[we][you]
             if aud_DictHigh[you][counterAH] != aud_DictHigh[you][counterAH-1]:
                aud_DictHigh[you].append(vecna)
                counterHigh[we][you]=(len(aud_DictHigh[you]))
                counterAH=counterHigh[we][you]
    def fillDictLow(we,you,vecna):
        if we=="XAUUSD":
            if len(xau_Dictlow[you]) <2:
                xau_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(xau_Dictlow[you]))
                counterXL=counterLow[we][you]
            elif len(xau_Dictlow[you])>2:
             counterXL=counterLow[we][you]
             if xau_Dictlow[you][counterXL] != xau_Dictlow[you][counterXL-1]:
                xau_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(xau_Dictlow[you]))
                counterXL=counterLow[we][you]
            # print(f"The counter value on GOLD low Dict is {counterXL}")
            print(f"The Gold Low Dictionary is {xau_Dictlow }")
            print(f"The length of Gold'd low dictionary is {len(xau_Dictlow[you])}")
            print(f"NUM BARS IS {NUM_BARS}")
        if we =="EURUSD":
            if len(eur_Dictlow[you])<2:
                eur_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(eur_Dictlow[you]))
                counterEL=counterLow[we][you]
                print(f"EL counter value {counterEL}")
            elif len(eur_Dictlow[you])>2:
             counterEL=counterLow[we][you]
             if eur_Dictlow[you][counterEL] != eur_Dictlow[you][counterEL-1]:
                eur_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(eur_Dictlow[you]))
                counterEL=counterLow[we][you]
        if we =="USDCAD":
            if len(cad_Dictlow[you])<2:
                cad_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(cad_Dictlow[you]))
                counterCL=counterLow[we][you]
            elif len(cad_Dictlow[you])>2:
             counterCL=counterLow[we][you]
             if cad_Dictlow[you][counterCL] != cad_Dictlow[you][counterCL-1]:
                cad_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(cad_Dictlow[you]))
                counterCL=counterLow[we][you]                
        if we =="USDJPY":
            if len(jpy_Dictlow[you])<2:
                jpy_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(jpy_Dictlow[you]))
                counterJL=counterLow[we][you]
            elif len(jpy_Dictlow[you])>2:
             counterJL=counterLow[we][you]
             if jpy_Dictlow[you][counterJL] != jpy_Dictlow[you][counterJL-1]:
                jpy_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(jpy_Dictlow[you]))
                counterJL=counterLow[we][you]
        if we =="AUDCAD":
            if len(aud_Dictlow[you])<2:
                aud_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(aud_Dictlow[you]))
                counterAL=counterLow[we][you]
            elif len(aud_Dictlow[you])>2:
             counterAL=counterLow[we][you]  
             if aud_Dictlow[you][counterAL] != aud_Dictlow[you][counterAL-1]:
                aud_Dictlow[you].append(vecna)
                counterLow[we][you]=(len(aud_Dictlow[you]))
                counterAL=counterLow[we][you]          

    
    if TIMEFRAMEs == 15:
        # fill high dictionary
        fillDictHigh(we=J,you=TIMEFRAMEs,vecna=highestPrice)
        # fill the low dictionary 
        fillDictLow(we=J,you=TIMEFRAMEs,vecna=lowestPrice)
    if TIMEFRAMEs == 30:
        fillDictHigh(we=J,you=TIMEFRAMEs,vecna=highestPrice)
        fillDictLow(we=J,you=TIMEFRAMEs,vecna=lowestPrice)
    if TIMEFRAMEs == 16385:
        fillDictHigh(we=J,you=TIMEFRAMEs,vecna=highestPrice)
        fillDictLow(we=J,you=TIMEFRAMEs,vecna=lowestPrice)
    if TIMEFRAMEs == 16388:
        fillDictHigh(we=J,you=TIMEFRAMEs,vecna=highestPrice)
        fillDictLow(we=J,you=TIMEFRAMEs,vecna=lowestPrice)
def main():
   conn()
   while True:
        for j in SYMBOL:
          for s in high_TIMEFRAME:
            global J
            # print(counter)
            J=j
            S=s
            startBackTest(S)     
            global NUM_BARS
        NUM_BARS=NUM_BARS+50
        time.sleep(7)    
main() 
