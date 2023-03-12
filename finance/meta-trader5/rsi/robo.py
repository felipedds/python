import matplotlib.pyplot as plt
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import ta
import warnings

warnings.filterwarnings('ignore')

class Robo(object):
    def __init__(self, symbol, start, end, time_frame, verbose=True):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.time_frame = time_frame
        self.data = self.load_data()

    # Load dataset
    def load_data(self):
        if not mt5.initialize():
            print('initialize() failed, error code = ', mt5.last_error())
            quit()
        dataset = pd.DataFrame(mt5.copy_rates_range(self.symbol, self.time_frame, self.start, self.end))
        dataset['time'] = pd.to_datetime(dataset['time'], unit='s')
        dataset.index = dataset['time']
        self.data = dataset.drop(columns=['time', 'real_volume'])
        return pd.DataFrame(self.data)

    # Indicator
    def rsi(self, period): # RSI
        delta = self.data.diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period-1]] = np.mean(u[:period]) #first value is sum of avg gains.
        u = u.drop(u.index[:(period-1)])
        d[d.index[period-1]] = np.mean(d[:period]) #first value is sum of avg losses.
        d = d.drop(d.index[:(period-1)])
        rs = u.ewm(com=period-1, adjust=False).mean() / d.ewm(com=period-1, adjust=False).mean()
        return 100 - 100 / (1 + rs)

    # Strategy RSI
    def backtest_strategy_rsi(self, period):
        # Rule of trade, if the condition is True then continue in trading of the period defined above
        self.data['rsi'] = self.rsi(period)
        self.data['signal'] = np.where(self.data['rsi'] >= 71, -1, 0)
        self.data['signal'] = np.where(self.data['rsi'] <= 29, 1, self.data['signal'])

        self.data['daily_return'] = self.data['close'].pct_change(window=1)
        self.data['target'] = self.data['daily_return'].shift(-1)
        self.data['strategy_return'] = self.data['signal'] * self.data['target']

        # Calculating the accumulated result
        self.data['cu_strategy_return'] = 0
        self.data['cu_daily_return'] = 0
        self.data.iloc[:, self.data.columns.get_loc('cu_strategy_return')] = (self.data['strategy_return'] + 1).cumprod()
        self.data.iloc[:, self.data.columns.get_loc('cu_daily_return')] = (self.data['daily_return'] + 1).cumprod()
        self.data['excess_daily_strategy_return'] = self.data['strategy_return'][:] - 0.05 / 252 # Calculate the excess daily return by assuming an annual risk free rate of return of 5%

        # Plotting the Strategy Return RSI
        plt.figure(figsize=(20, 15))
        plt.title(self.symbol + str(self.time_frame))
        plt.plot(self.data['cu_strategy_return'], color='g', label='Strategy Returns')
        plt.xlabel('Date')
        plt.ylabel('Returns')
        plt.legend()
        plt.show()

        # Calculate the annualized Sharpe ratio
        sharpe = (self.data['cu_strategy_return'].iloc[-1] - self.data['cu_daily_return'].iloc[-1]) / self.data['cu_strategy_return'].std()
        annualized_sharpe_ratio = (np.sqrt(252) * self.data['strategy_return'].mean()) / self.data['strategy_return'].std()
        print('Sharpe', sharpe)
        print('Annualized Sharpe Ratio', annualized_sharpe_ratio)    
        return self.data.dropna()