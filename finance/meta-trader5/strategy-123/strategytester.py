import math
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

    # Trade's Éden(Éden dos Traders) strategy
    def strategy_eden(self):
        # Load dataset
        dataset = pd.DataFrame(self.data)

        # Definindo o candle sinal (Defining the signal candle)
        condition_1 = dataset["low"] > dataset["low"].shift(1)
        condition_2 = dataset["low"].shift(1) < dataset["low"].shift(2)
        dataset["signal"] = condition_1 & condition_2

        # Calculando o Éden dos Traders e EWM (Calculating Trade's Éden and EWM)
        dataset["ewm8"] = dataset["close"].ewm(span=8, min_periods=8).mean() # Exponentially Weighted (EW)
        dataset["ewm80"] = dataset["close"].ewm(span=80, min_periods=80).mean()        
        dataset["eden"] = (dataset["ewm8"] > dataset["ewm8"].shift(1)) & (dataset["ewm80"] > dataset["ewm80"].shift(1))
        
        # Definindo o preço de compra (Setting the purchase price)
        condition_1 = dataset["signal"].shift(1) == True
        condition_2 = dataset["eden"].shift(1) == True 
        condition_3 = dataset["high"] > dataset["high"].shift(1)
        tick = 0.01

        dataset["buy_price"] = np.where(
            condition_1 & condition_2 & condition_3, 
            np.where(dataset["open"] > dataset["high"].shift(1), dataset["open"], dataset["high"].shift(1) + tick),
            np.nan
        )

        # Definindo o alvo (Setting the target)
        max_high = dataset["high"].rolling(3).max()
        min_low = dataset["low"].rolling(3).min()

        amplitude = (max_high.shift(1) - min_low.shift(1))
        entry = dataset["high"].shift(1)
        dataset["target"] = amplitude + entry

        # Definindo o stop (Setting the stop)
        dataset["stop"] = dataset["low"].shift(2) - tick

        self.data = dataset.dropna()
        return pd.DataFrame(self.data)
    
    # Definindo o algoritmo para realizar o backtest e simular as operações
    def backtest(self, capital_exposure:float, initial_capital:float):
        # Load dataset
        dataset = pd.DataFrame(self.strategy_eden())

        # List with the total capital after every operation
        total_capital = [initial_capital]

        # List with profits for every operation
        all_profits = []

        ongoing = False

        for i in range(0, len(dataset)):

            if ongoing == True:

                if (dataset["open"][i] >= target) | (dataset["open"][i] <= stop): 
                    exit = dataset["open"][i]

                    profit = shares * (exit - entry)
                    # Append profit to list and create a new entry with the capital, after the operation is complete
                    all_profits += [profit]
                    current_capital = total_capital[-1] # current capital is the last entry in the list
                    total_capital += [current_capital + profit]

                    ongoing = False

                elif dataset["low"][i] <= stop: 
                    exit = stop

                    profit = shares * (exit - entry)
                    # Append profit to list and create a new entry with the capital, after the operation is complete
                    all_profits += [profit]
                    current_capital = total_capital[-1] # current capital is the last entry in the list
                    total_capital += [current_capital + profit]

                    ongoing = False

                elif dataset["high"][i] >= target: 
                    exit = target

                    profit = shares * (exit - entry)
                    # Append profit to list and create a new entry with the capital, after the operation is complete
                    all_profits += [profit]
                    current_capital = total_capital[-1] # current capital is the last entry in the list
                    total_capital += [current_capital + profit]

                    ongoing = False

            else:
                if ~(np.isnan(dataset["buy_price"][i])):
                    entry = dataset["buy_price"][i]
                    stop = dataset["stop"][i]
                    
                    if dataset["low"][i] > stop: 
                        ongoing = True
                        risk = entry - stop
                        target = dataset["target"][i]
                        shares = int(math.floor((capital_exposure / risk) / 100.0)) * 100

        return all_profits, total_capital
    
    def max_drawdown(self):
        # Load dataset
        dataset = pd.DataFrame(self.data)
        dataset["max"] = dataset["close"].cummax()
        dataset["delta"] = dataset['max'] - dataset["close"]
        dataset["drawdown"] = 100 * (dataset["delta"] / dataset["max"])
        max_drawdown = dataset["drawdown"].max()
        return max_drawdown

    def strategy_test(self, all_profits:float, total_capital:float):
        gains = sum(x >= 0 for x in all_profits)
        losses = sum(x < 0 for x in all_profits)
        num_operations = gains + losses
        pct_gains = 100 * (gains / num_operations)
        pct_losses = 100 - pct_gains
        total_profit = sum(all_profits)
        pct_profit = (total_profit / total_capital[0]) * 100
        
        # Compute drawdown
        total_capital = pd.DataFrame(data=total_capital, columns=["total_capital"])
        max_drawdown = self.max_drawdown()

        # Compute profit per operation
        profit_per_operation = pct_profit / num_operations

        return {
            "num_operations": num_operations,
            "gains": gains ,
            "pct_gains": pct_gains.round(),
            "losses": losses,
            "pct_losses": pct_losses.round(), 
            "total_profit": total_profit,
            "pct_profit": pct_profit,
            "drawdown": max_drawdown,
            "profit_per_operation": profit_per_operation
        }
    
    def capital_plot(self, symbol:str, time_frame:str, total_capital:float, all_profits:float):
        all_profits = [0] + all_profits # make sure both lists are the same size
        capital_evolution = pd.DataFrame({"capital": total_capital, "profit": all_profits})
        plt.title(f"Curva de Capital / {symbol} / {time_frame}")
        plt.xlabel("Total Operações")
        plt.ylabel("Value $")
        capital_evolution["capital"].plot()
        plt.show()
    
    def expected_value(self, all_profits:float):
        all_positives = [x for x in all_profits if x >= 0]
        average_gain = sum(all_positives) / len(all_positives)

        all_negatives = [x for x in all_profits if x < 0]
        average_loss = sum(all_negatives) / len(all_negatives)

        num_operations = len(all_profits)
        pct_gains = (len(all_positives) / num_operations)
        pct_losses = 1 - pct_gains
        
        expected_value = (average_gain * pct_gains) + (average_loss * pct_losses)
        
        result = pd.DataFrame.from_dict({
            "average_gain": average_gain,
            "average_loss": average_loss,
            "pct_gains": pct_gains,
            "pct_losses": pct_losses,
            "expected_value": expected_value
        }, orient="index")
        result.columns = ["result"]
        return result
