
import os
import MetaTrader5 as mt5
from datetime import datetime
from decouple import config


def conn():
    account=int(810403203)
    password = "Marichu12"
    server = 'EGMSecurities-Live'
    mt5.initialize()
    if not mt5.initialize():
        print(f"initialize() error is {mt5.last_error()}" )
        quit()
    auth= mt5.login(account,password,server)
    if auth:
        print("Connecting to MetaTrader 5")
        # print(mt5.account_info())
        # get information on the EURUSD pair
        symbol_info= mt5.symbol_info("EURUSD")._asdict
        print(symbol_info)
        # get the price of the EURUSD pair
        symbol_infor= mt5.symbol_info_tick("EURUSD")._asdict
        print(symbol_infor)
    else:
        print(mt5.last_error())

    symbols= mt5.symbols_total()
    if symbols>0:
        print(f"Total symbols are {symbols}")
    else:
        print("No symbols found")

conn()
        