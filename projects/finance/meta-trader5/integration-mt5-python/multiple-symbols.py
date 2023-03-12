import matplotlib.pyplot as plt
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import seaborn as sns


mt5.initialize(login=63144446, server="MetaQuotes-Demo", password="o1hffxac")

if not mt5.initialize():
    print('initialize() failed, error code = ', mt5.last_error())
    quit()

symbols = ["AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD", "CADCHF", "CADJPY", "CADMXN", "CHFJPY", "CHFMXN", "EURAUD", "EURCAD", "EURCHF", "EURCZK", "EURDKK", "EURGBP", "EURHKD", "EURHUF", "EURJPY", "EURMXN", "EURNOK", "EURNZD", "EURPLN", "EURRUB", "EURRUR", "EURSEK", "EURTRY", "EURUSD", "EURZAR", 
           "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPMXN", "GBPNOK", "GBPNZD", "GBPPLN", "GBPSEK", "GBPSGD", "GBPUSD", "GBPZAR", "MXNJPY", "NZDCAD", "NZDCHF", "NZDJPY", "NZDMXN", "NZDSGD", "NZDUSD", "SGDJPY", "USDARS", "USDCAD", "USDCHF", "USDCNH", "USDCOP", "USDCZK", "USDDKK", "USDGEL", "USDHKD", 
           "USDHUF", "USDJPY", "USDMXN", "USDNOK", "USDPLN", "USDRUB", "USDRUR", "USDSEK", "USDSGD", "USDTRY", "USDZAR", "XAGEUR", "XAGUSD", "XAUAUD", "XAUEUR", "XAUUSD", "XPDUSD", "XPTUSD"]

dataset = pd.DataFrame()
for symbol in symbols:
    assets = pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 700))
    assets["time"] = pd.to_datetime(assets["time"], unit="s")
    dataset[symbol] = assets["close"] # Add column to dataframe.
    vars()[symbol] = pd.DataFrame(assets["close"]) # Create dataframe(name of asset) split with name of symbol.
dataset.index = assets['time']
#dataset["time"] = dataset.index
print(dataset)

