from datetime import datetime
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
plt.style.use("ggplot")

class StrategyTester(object):
    def __init__(self, symbol, start, end, time_frame):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.time_frame = time_frame
        self.data = self.load_data()

    # Load dataset
    def load_data(self):
        print("MetaTrader5 package author: ", mt5.__author__)
        print("MetaTrader5 package version: ", mt5.__version__)

        if not mt5.initialize():
            print("initialize() failed, error code = ", mt5.last_error())
            quit()

        dataset = pd.DataFrame(mt5.copy_rates_range(self.symbol, self.time_frame, self.start, self.end))
        dataset["time"] = pd.to_datetime(dataset["time"], unit="s")
        dataset.index = dataset["time"]
        self.data = dataset.drop(columns=["tick_volume", "real_volume", "spread"])
        return pd.DataFrame(self.data)

    def rsi(self, dataset, period:int):
        self.data = dataset.dropna()
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

    def strategy_rsi(self):
        # Load dataset
        dataset = pd.DataFrame(self.data)

        # Calculating the RSI
        dataset["RSI21"] = self.rsi(dataset["close"], 21)
        dataset["RSI34"] = self.rsi(dataset["close"], 34)
        
        # Definindo o candle sinal (Defining the signal candle)
        dataset["signal"] = np.select([(dataset["RSI21"] > 70) & (dataset["RSI34"] > 70), 
                                       (dataset["RSI21"] < 30) & (dataset["RSI34"] < 30)], [-1, 1], default=0) # -1: SELL / 1: BUY / 0: NOTHING

        # Definindo o preço de compra (Setting the purchase price)
        tick = 0.01

        self.data = dataset.dropna()
        return pd.DataFrame(self.data)
    
    def backtest_strategy_rsi(self):
        dataset = pd.DataFrame(self.data)
        dataset["daily_return"] = self.data["close"].pct_change(periods=1)
        # Calculate the Strategy Returns
        dataset["strategy_returns"] = (self.data["daily_return"] * self.data["signal"].shift(1))
        # Plotting the strategy return
        dataset["strategy_returns"].plot(figsize=(20, 15))
        plt.title(f"Strategy Returns / {self.symbol}")
        plt.xlabel("Date")
        plt.ylabel("Strategy Returns")
        plt.legend()
        plt.show()

         # Calculating the accumulated result / Calculate Cumulative Strategy Returns
        self.data["cumulative_strategy_returns"] = 0
        self.data["cumulative_daily_returns"] = 0
        self.data["cumulative_strategy_returns"] = (1 + self.data["strategy_returns"]).cumprod()
        self.data["cumulative_daily_returns"] = (1 + self.data["daily_return"]).cumprod()
        # Plotting Strategy Returns and Daily returns / Equity Curve
        plt.figure(figsize=(20, 15))
        plt.plot(self.data["cumulative_strategy_returns"], color='green', label="Cummulative Strategy Returns")
        plt.plot(self.data["cumulative_daily_returns"], color='red', label="Cummulative Daily Returns")
        plt.title(f"Cumulative Strategy Returns - {self.symbol} / {str(self.time_frame)}")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Strategy/Daily Returns")
        plt.axhline(y=1, color="blue")
        plt.legend()
        plt.show()

        # Calculate the running Maximum (maximum cumulative cumulative_strategy_returns)
        peak_value = np.maximum.accumulate(self.data["cumulative_strategy_returns"].dropna())
        # Ensure the value never drops below 1
        peak_value[peak_value < 1] = 1
        # Calculate the Percentage Drawdown
        drawdown = ((self.data["cumulative_strategy_returns"]) / peak_value - 1) * 10
        
        # Plot Drawdown
        plt.figure(figsize=(20, 15))
        plt.plot(drawdown, color="red")
        plt.fill_between(drawdown.index, drawdown.values, color="red", label="Drawdown")
        plt.title("Strategy Drawdown")
        plt.xlabel("Year")
        plt.ylabel("Drawdown(%)")
        plt.legend()
        plt.show()

        # Difference between dates in timedelta(range of days that strategy operates)
        delta = datetime.date(self.data.index[-1]) - datetime.date(self.data.index[0])
        print(f'\nFirst Day is: {self.data.index[0]} / Last Day is: {self.data.index[-1]} / Difference: {delta.days} days.')
        
        # Number of trades, calculate the number of trades generated.
        trades = np.count_nonzero(self.data["signal"])
        print(f'Number of trades: {trades}')

        # Calculate the Cumulative Strategy Returns Final Result in percent(%)
        cumulative_strategy_returns = (self.data["cumulative_strategy_returns"][-1] - 1) * 100
        print(f"The Cumulative Strategy Returns is: {'{:.2f}'.format(cumulative_strategy_returns)}%.")

        # Calculate the Annualised Strategy Returns Final Result in percent(%)
        annualised_strategy_return = ((self.data["cumulative_strategy_returns"][-1]) ** (252 / self.data.shape[0]) - 1) * 100
        print(f"The Annualised Strategy Returns is: {'{:.2f}'.format(annualised_strategy_return)}%.")

        # Calculate the Maximum Drawdown
        max_drawdown = drawdown.min()
        print(f"The Maximum Drawdown is: {'{:.2f}'.format(max_drawdown)}%")

        # Calculate the Sharpe Ratio
        sharpe_ratio = round(self.data["strategy_returns"].mean() / self.data["strategy_returns"].std() * np.sqrt(252), 2)
        print(f"The Sharpe Ratio is: {'{:.2f}'.format(sharpe_ratio)}%")

        # Calculate the Annualised Volatility
        annualised_volatility = self.data["strategy_returns"].std()*np.sqrt(252) * 100
        print(f"The Annualised Volatility is {'{:.2f}'.format(annualised_volatility)}%")
        return pd.DataFrame(self.data)
        