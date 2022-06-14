
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
        # check info on the EURUSD
        symbol_info=mt5.symbol_info("EURUSD").asdict
        print(symbol_info)

    else:
        print(mt5.last_error())


conn()

        