from datetime import datetime
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import pytz
import time
import warnings

warnings.filterwarnings('ignore')

class Robo(object):
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

        mt5.initialize(login=63144446, server="MetaQuotes-Demo", password="o1hffxac")

        if not mt5.initialize():
            print("initialize() failed, error code = ", mt5.last_error())
            quit()

        dataset = pd.DataFrame(mt5.copy_rates_range(self.symbol, self.time_frame, self.start, self.end))
        print("Ticks received:", len(dataset))
        dataset["time"] = pd.to_datetime(dataset["time"], unit="s")
        dataset.index = dataset["time"]
        self.data = dataset.drop(columns=["time", "tick_volume", "real_volume", "spread"])
        return pd.DataFrame(self.data)

    # Strategy
    def strategy(self):
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

        # Buy Market
        if (np.isnan(dataset["buy_price"][-1]) == False):
            lot = 0.10
            point = mt5.symbol_info(self.symbol).point # Symbol point value(SYMBOL_POINT)
            price = dataset["buy_price"][-1]
            stop_loss = dataset["stop"][-1],
            take_profit = dataset["target"][-1],
            deviation = 20
            print(point, price, stop_loss, take_profit)

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "sl": stop_loss,
                "tp": take_profit,
                "deviation": deviation,
                "magic": 234000,
                "comment": f"Open buy {self.symbol}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            
            # Send a trading request
            result = mt5.order_send(request)

            # Check the execution result
            print(f"1. Buy order_send(): by {self.symbol} in {point} point {lot} lots at {price} with deviation = {deviation} points")

            if (result.retcode != mt5.TRADE_RETCODE_DONE):
                print(f"2. order_send() failed, retcode={result.retcode}")
                # Request the result as a dictionary and display it element by element
                result_dict = result._asdict()
                for field in result_dict.keys():
                    print(f"{field}={result_dict[field]}")
                    # If this is a trading request structure, display it element by element as well
                    if field == "request":
                        traderequest_dict = result_dict[field]._asdict()
                        for tradereq_filed in traderequest_dict:
                            print(f"traderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
                print("shutdown() and quit().")
                mt5.shutdown()
                quit()

            print("2. Buy order_send done, ", result)
            print(f"Opened position with POSITION_TICKET = {result.order}")
            print(f"Sleep 2 seconds before closing position #{result.order}")
            time.sleep(2)

        self.data = dataset #dataset.dropna()
        return pd.DataFrame(self.data)
    
    # Buy Market
    def buy(self, symbol: str):
        # Load dataset
        dataset = pd.DataFrame(self.strategy())
        lot = 0.10
        point = mt5.symbol_info(symbol).point # Symbol point value(SYMBOL_POINT)
        price = mt5.symbol_info_tick(symbol).ask
        deviation = 20
        print(point, price)
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - 100 * point,
            "tp": price + 200 * point,
            "deviation": deviation,
            "magic": 234000,
            "comment": f"Open buy {symbol}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        
        # Send a trading request
        result = mt5.order_send(request)
        # Check the execution result
        print(f"1. Buy order_send(): by {symbol} in {point} point {lot} lots at {price} with deviation = {deviation} points");
        if (result.retcode != mt5.TRADE_RETCODE_DONE):
            print(f"2. order_send() failed, retcode={result.retcode}")
            # Request the result as a dictionary and display it element by element
            result_dict=result._asdict()
            for field in result_dict.keys():
                print(f"{field}={result_dict[field]}")
                # If this is a trading request structure, display it element by element as well
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print(f"traderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
            print("shutdown() and quit().")
            mt5.shutdown()
            quit()

        print("2. Buy order_send done, ", result)
        print(f"Opened position with POSITION_TICKET = {result.order}")
        print(f"Sleep 2 seconds before closing position #{result.order}")
        time.sleep(2)
    
    # Sell Market
    def sell(self, symbol: str):
        # Load dataset
        dataset = pd.DataFrame(self.strategy())
        lot = 0.10
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).bid
        deviation = 20
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": price + 100 * point,
            "tp": price - 200 * point,
            "deviation": deviation,
            "magic": 235000,
            "comment": f"Open sell {symbol}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        
        # Send a trading request
        result = mt5.order_send(request)
        # Check the execution result
        print(f"1. Sell order_send(): by {symbol} in {point} point {lot} lots at {price} with deviation = {deviation} points");
        if (result.retcode != mt5.TRADE_RETCODE_DONE):
            print(f"2. order_send() failed, retcode={result.retcode}")
            # Request the result as a dictionary and display it element by element
            result_dict=result._asdict()
            for field in result_dict.keys():
                print(f"{field}={result_dict[field]}")
                # If this is a trading request structure, display it element by element as well
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print(f"traderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
            print("shutdown() and quit().")
            mt5.shutdown()
            quit()

        print("2. Sell order_send done, ", result)
        print(f"Opened position with POSITION_TICKET = {result.order}")
        print(f"Sleep 2 seconds before closing position #{result.order}")
        time.sleep(2)