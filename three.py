from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import plotly.express as px

def conn():
    init = mt5.initialize()
    if not init:
        print(f"The Initialisation error is {mt5.last_error()}")
    account = int(810414810)
    password = "Marichu12"
    server = "EGMSecurities-Live"
    auth= mt5.login(account,password,server)
    if auth:
        innert()
    else:
        print(mt5.last_error())
def innert():
    print(mt5.account_info())
    symbol = mt5.symbol_info("EURUSD")._asdict
    print(symbol)
    print("Connection successful")
    eur_usd=pd.DataFrame(mt5.copy_rates_range("EURUSD",mt5.TIMEFRAME_D1,datetime(2021,9,8),datetime.now()))
    dig=px.line(eur_usd,x=eur_usd["time"],y=eur_usd["close"])
    dig.show()

conn()
