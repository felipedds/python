# Import the libraries
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
from strategy_tester import StrategyTester
import warnings

warnings.filterwarnings('ignore')

'''
symbols_icmarket = ["EURUSD", "GBPUSD", "USDCHF", "USDJPY", "USDCNH",
                    "USDRUB", "AUDUSD", "NZDUSD", "USDCAD", "USDSEK",
                    "USDHKD", "USDSGD", "USDNOK", "USDDKK", "USDTRY",
                    "USDZAR", "USDCZK", "USDHUF", "USDPLN", "USDRUR", "AUDCAD", "AUDCHF",
                    "AUDJPY", "AUDNZD", "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURCAD",
                    "EURCHF", "EURCZK", "EURDKK", "EURGBP", "EURHKD", "EURHUF", "EURJPY",
                    "EURNOK", "EURNZD", "EURPLN", "EURRUR", "EURRUB", "EURSEK",
                    "EURTRY", "EURZAR", "GBPAUD", "GBPCHF", "GBPJPY", "XAUUSD", "XAUEUR", "XAUAUD",
                    "XAGUSD", "XAGEUR", "GBPCAD", "GBPNOK", "GBPNZD", "GBPPLN", "GBPSEK", "GBPSGD",
                    "GBPZAR", "NZDCAD", "NZDCHF", "NZDJPY",
                    "NZDSGD", "SGDJPY", "XPDUSD", "XPTUSD", "USDGEL", "USDMXN",
                    "EURMXN", "GBPMXN", "CADMXN", "CHFMXN", "MXNJPY", "NZDMXN",
                    "USDCOP", "USDARS", "USDCLP", "AUS200", "FCHI40", "GDAXIm", "HSI50", "ND100m",
                    "NI225", "SP500m", "SPN35", "STOX50", "UK100", "Brent", "Crude", "NatGas",
                    "BRENT_V0", "WTI_U0", "XBRUSD", "XNGUSD", "XTIUSD", "Cocoa_Z0", "Coffee_Z0", "Corn_U0",
                    "Cotton_Z0", "OJ_U0", "Soybean_U0", "Sugar_V0", "Wheat_U0", "Wheat_Z0"]
'''

# Main
if __name__ == "__main__":
    symbols = ["BTCUSD"]
    time_frames = [mt5.TIMEFRAME_M5]
    for symbol in symbols:
        print(f'\n {symbol}')
        for time_frame in time_frames:
            strategy_tester = StrategyTester(symbol, datetime(2022, 6, 30), datetime(2023, 1, 13), time_frame)
            print(strategy_tester.load_data())
            print(strategy_tester.bollinger_bands(period=21))
            print(strategy_tester.backtest_strategy_bollinger_bands(period=21))

