from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5

# from tabulate import tabulate

# connect to the terminal
# def conn():
#     initt= mt5.initialize()
#     if not initt:
#         print(f"the initialisation error was{mt5.last_error()}")
#     account = int(810403203)
#     password ="Marichu12"
#     server = "EGMSecurities"
#     auth = mt5.login(account,password,server)
#     if auth:
#         innert()
#     else:
#         print(f"The authentication error is{mt5.last_error}")
def innert():
    print("connection is successful")
    rates = pd.read_csv("trades-example.csv")
    # how many trades were placed
    number_of_trades = rates.shape[0]
    # sum of total profits
    t_profit= rates["profit"].sum()
    # when the first trade was placed
    first_trade= rates.iloc[0]["open_datetime"]
    # last trade
    last_trade=rates.iloc[-1]["open_datetime"]
    # trade with largest profit
    biggest_profit = rates.loc[rates["profit"]==rates["profit"].max()]
    # trade with the largest loss
    largest_loss= rates.loc[rates["profit"]==rates["profit"].min()]
    #  trades that took the longest and the shortest 
    rates["duration"]=pd.to_datetime(rates["close_datetime"]) - pd.to_datetime(rates["open_datetime"])
    longest_duration=rates.loc[rates["duration"] == rates["duration"].max()]
    shortest_duration=rates.loc[rates["duration"]==rates["duration"].min()]
    # most profitable and most losing months
    rates["month"]=pd.to_datetime(rates["close_datetime"]).dt.month
    # print(rates)
    rates["count_trades"]=1
    rates_by_month=rates.groupby("month").agg({
        "profit":"sum"
    }).sort_values("profit",ascending=False)
    rates_count_trades=rates.groupby("month").agg({
        "count_trades":"count"
    }).sort_values("count_trades",ascending=False)
    # see which among buy or sells was more profitable
    rates_order_by_type=rates.groupby("order_type").agg({
        "profit":"sum",
        "count_trades":"count"
    })
    print(rates_order_by_type)
    # biggest absolute drawdowns
    rates["cummulative"]=rates["profit"].cumsum()
    big_abs_dd=rates.loc[rates["cummulative"]==rates["cummulative"].min()]
    # print(big_abs_dd)
    # average profit
    # first create the proft order
    rates["profit_order"]=rates["profit"].apply( lambda x: "win" if x>=0 else "loss")
    avg_pl=rates.groupby("profit_order").agg({
        "profit":"mean"
    })
    # print(avg_pl) 
    # calculate the win rate
    win_rate= rates.groupby("profit_order").agg({
        "count_trades":"count"
    })
    print(win_rate)
    win_rate["winrate"]=(win_rate["count_trades"]/win_rate["count_trades"].sum())*100
    print(win_rate)
    # risk to reward ratio
    print(avg_pl)
    rr=abs(avg_pl.loc["win"]["profit"]/avg_pl.loc["loss"]["profit"])
    print(f"The risk to reward ratio is {rr}")
    EUR_rates =pd.DataFrame(mt5.copy_rates_range("EURUSD",mt5.TIMEFRAME_D1,datetime(2021,9,8),datetime.now()))
    
    # print(number_of_trades)
    # print(f"total profit is{t_profit}")
    # print(f"Fisrt trade was placed on {first_trade}")
    # print(f"Last trade was placed on {last_trade}")
    # print(biggest_profit)
    # print(largest_loss)
    # print("************** LONGEST DURATION ******************")
    # print(longest_duration)
    # print("************** SHORTEST DURATION ******************")
    # print(shortest_duration)

# conn()
innert()




