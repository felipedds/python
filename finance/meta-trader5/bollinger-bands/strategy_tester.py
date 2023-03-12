import matplotlib.pyplot as plt
import MetaTrader5 as mt5
import pandas as pd
import warnings
import numpy as np
from datetime import datetime


warnings.filterwarnings('ignore')
plt.style.use("ggplot")
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 1000)

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
        self.data = dataset.drop(columns=["tick_volume", "real_volume", "spread", "time", "high", "low"])
        self.data = dataset
        return pd.DataFrame(self.data)

    # Bollinger Bands
    def bollinger_bands(self, period):
        self.data[f'ma_{period}'] = self.data['close'].rolling(window=period).mean()
        self.data['upper_band'] = self.data[f'ma_{period}'] + (2 * self.data[f'ma_{period}'].rolling(window=period).std())
        self.data['lower_band'] = self.data[f'ma_{period}'] - (2 * self.data[f'ma_{period}'].rolling(window=period).std())
        return pd.DataFrame(self.data).dropna()

    # Backtest Strategy
    def backtest_strategy_bollinger_bands(self, period):
        # Load dataset
        self.data = self.bollinger_bands(period)
        
        # Defining the signal candle
        self.data["signal"] = np.select([(self.data["close"] < self.data["lower_band"]) & (self.data["close"].shift(1) >= self.data["lower_band"]),
                            (self.data["close"] > self.data["upper_band"]) & (self.data["close"].shift(1) <= self.data["upper_band"])], [1, -1], default=0)

        # Daily return
        self.data["daily_return"] = self.data["close"].pct_change(periods=1)
        
        # Calculate the Strategy Returns
        self.data["strategy_returns"] = (self.data["daily_return"] * self.data["signal"].shift(1))
        # Plotting the strategy return
        self.data["strategy_returns"].plot(figsize=(20, 15))
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
        short_trades = len(self.data[self.data["signal"] == -1])
        long_trades = len(self.data[self.data["signal"] == 1])
        total_trades = short_trades + long_trades
        print(f'Short trades: {short_trades}\nLong trades: {long_trades}\nTotal trades: {total_trades}')
        print(f'Profit Trades: {len(self.data[self.data["strategy_returns"] > 0.000001])}')
        print(f'Loss Trades: {len(self.data[self.data["strategy_returns"] < 0.000000])}\n')

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
        return pd.DataFrame(self.data).dropna().tail(60)

    