import pandas as pd
import numpy as np
import sqlite3
import datetime
import yfinance as yf

class Forex(object):
    def __init__(self, ticker: str, start: datetime, end: datetime, time_frame: str):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.time_frame = time_frame
        
    def load_data(self, ticker: str, time_frame: str): # Load dataset.
        params_dic = {
         'host': 'localhost',
         'database': '../data/forex.db'
        }
        connection = sqlite3.connect(f"{params_dic['database']}")
        dataset = pd.read_sql_query("SELECT * FROM "+ticker.lower()+"_"+time_frame, connection)
        dataset = dataset.astype({'time':'datetime64'})
        connection.close()
        return dataset

class Commodities(object):
    def __init__(self, ticker: str, start: datetime, end: datetime, time_frame: str):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.time_frame = time_frame
        
    def load_data(self, ticker: str, time_frame: str): # Load dataset.
        params_dic = {
         'host': 'localhost',
         'database': '../data/forex.db'
        }
        connection = sqlite3.connect(f"{params_dic['database']}")
        dataset = pd.read_sql_query("SELECT * FROM "+ticker.lower()+"_"+time_frame, connection)
        dataset = dataset.astype({'time':'datetime64'})
        connection.close()
        return dataset

# Bot RSI with time in 21 days and 34 days.
class StrategyRSI(Forex):
    def __init__(self, ticker: str, start: datetime, end: datetime, time_frame: str):
        super().__init__(ticker, start, end, time_frame)
        self.strategy_rsi()
        
    def load_data(self): # Load dataset.
        dataset = Forex.load_data(self, self.ticker, self.time_frame)
        return pd.DataFrame(dataset.dropna())
    
    def rsi(self, dataset, period): # Indicator RSI.
        self.data = dataset.dropna()
        delta = self.data.diff()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period-1]] = np.mean(u[:period]) # first value is sum of average gains.
        u = u.drop(u.index[:(period-1)])
        d[d.index[period-1]] = np.mean(d[:period]) # first value is sum of average losses.
        d = d.drop(d.index[:(period-1)])
        rs = u.ewm(com=period-1, adjust=False).mean() / d.ewm(com=period-1, adjust=False).mean()
        return 100 - 100 / (1 + rs)
        
    def strategy_rsi(self): # Strategy RSI.
        dataset = self.load_data().dropna()
        dataset['RSI21'] = self.rsi(dataset['close'], 21)
        dataset['RSI34'] = self.rsi(dataset['close'], 34)
        rsi21 = dataset['RSI21'].tail(1)
        rsi34 = dataset['RSI34'].tail(1)
        
        if rsi34.iloc[:1].values > 70: # RSI 34 above 70.
            print(f'Overbought RSI 34: {rsi34.iloc[:1].values} {self.ticker} {self.time_frame}.')
        if rsi34.iloc[:1].values < 30: # RSI 34 under 30.
            print(f'Oversold RSI 34: {rsi34.iloc[:1].values} {self.ticker} {self.time_frame}.')

        if rsi21.iloc[:1].values > 70: # RSI 21 above 70.
            print(f'Overbought RSI 21: {rsi21.iloc[:1].values} {self.ticker} {self.time_frame}.')
        if rsi21.iloc[:1].values < 30: # RSI 21 under 30.
            print(f'Oversold RSI 21: {rsi21.iloc[:1].values} {self.ticker} {self.time_frame}.') 
        
        my_dict = {'Ticker':[], 'RSI':[], 'Time':[]}
        my_dict['Ticker'].append(self.ticker)
        my_dict['RSI'].append(rsi21.iloc[:1].values)
        my_dict['Time'].append(self.time_frame)
        print(my_dict)

# Bot EMA in 9 days and 21 days.
class StrategyEMA(Forex):
    def __init__(self, ticker: str, start: datetime, end: datetime, time_frame: str):
        super().__init__(ticker, start, end, time_frame)
        self.strategy_ema()

    def load_data(self): # Load dataset.
        dataset = Forex.load_data(self, self.ticker, self.time_frame)
        dataset = dataset.dropna()
        return pd.DataFrame(dataset)

    def strategy_ema(self): # Strategy EMA(Exponential Moving Average).
        dataset = self.load_data().dropna()
        dataset['EMA9'] = dataset['close'].ewm(span=8, adjust=False).mean() # EMA Fast
        dataset['EMA21'] = dataset['close'].ewm(span=21, adjust=False).mean() # EMA Medium
        ema9 = dataset['EMA9'].tail(1)
        ema21 = dataset['EMA21'].tail(1)
        close = dataset['close'].tail(1)

        if (ema9.iloc[:1].values > close.iloc[:1].values and ema21.iloc[:1].values > close.iloc[:1].values): # RSI 34 above 70.
            print(f'Sell - Close: {close.iloc[:1].values} - EMA9 {ema9.iloc[:1].values} - EMA21 {ema21.iloc[:1].values} {self.ticker} {self.time_frame}.')
        if (ema9.iloc[:1].values < close.iloc[:1].values and ema21.iloc[:1].values < close.iloc[:1].values): # RSI 34 above 70.
            print(f'Buy - Close: {close.iloc[:1].values} - EMA9 {ema9.iloc[:1].values} - EMA21 {ema21.iloc[:1].values} {self.ticker} {self.time_frame}.')