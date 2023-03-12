import datetime
import MetaTrader5 as mt5
import pandas as pd
import time


print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

mt5.initialize(login=63144446, server="MetaQuotes-Demo", password="o1hffxac")

# Initialize the MetaTrader
if not mt5.initialize():
    print('initialize() failed, error code = ', mt5.last_error())
    quit()

print(mt5.version())
print("Terminal info: ", mt5.terminal_info())
print("Account info: ", mt5.account_info())

# Get the number of financial instruments.
symbols_total = mt5.symbols_total()
if symbols_total > 0:
    print("Total symbols = ", symbols_total)
else:
    print("Symbols not found.")

# Get all symbols
symbols = mt5.symbols_get()
print("Symbols: ", len(symbols))
for symbol in symbols:
    print(f"{symbol.name}")

# Check the presence of active orders
orders_total = mt5.orders_total()
if orders_total > 0:
    print("Total orders = ", orders_total)
else:
    print("Orders not found.")

# Check the presence of open positions
positions_total = mt5.positions_total()
if positions_total > 0:
    print("Total positions = ", positions_total)
else:
    print("Positions not found.")

# Get the list of positions on symbols whose names contain "*USD*"
usd_positions = mt5.positions_get(group="*USD*")
if usd_positions == None:
    print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
elif len(usd_positions) > 0:
    print(f"positions_get(group=\"*USD*\")={len(usd_positions)}")
    # display these positions as a table using pandas.DataFrame
    df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
    print(df)

# Load the data
tickers = ['EURUSD']
#tickers = ['USDX', 'ALUMINIUM', 'BRENT', 'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'COPPER', 'CADCHF', 'EURAUD', 'EURCAD', 'EURHUF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'GBPNZD', 'USDCAD', 'USDCHF', 'USDJPY', 'USDMXN', 'USDSGD', 'NZDUSD', 'NZDJPY', 'USDTRY', 'NZDUSD', 'XAGUSD', 'XAUUSD', 'WTI']
for ticker in tickers:
    time_frames = [mt5.TIMEFRAME_D1]
    for time_frame in time_frames:
        dataset = pd.DataFrame(mt5.copy_rates_from_pos(ticker, time_frame, 0, 100))
        dataset['time'] = pd.to_datetime(dataset['time'], unit='s')
        dataset.index = dataset['time']
        dataset = dataset.drop(columns=['spread', 'real_volume', 'tick_volume'])
        dataset.dropna(inplace=True)
        print(dataset)
print(f'{tickers}')

# Buy Market


def buy(symbol: str):
    lot = 0.10
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20

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
        "comment": "python script open buy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    # Send a trading request
    result = mt5.order_send(request)
    # Check the execution result
    print(
        f"1. Buy order_send(): by {symbol} in {point} point {lot} lots at {price} with deviation = {deviation} points")
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"2. order_send() failed, retcode={result.retcode}")
        # Request the result as a dictionary and display it element by element
        result_dict = result._asdict()
        for field in result_dict.keys():
            print(f"{field}={result_dict[field]}")
            # If this is a trading request structure, display it element by element as well
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print(
                        f"traderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
        print("shutdown() and quit().")
        mt5.shutdown()
        quit()

    print("2. Buy order_send done, ", result)
    print(f"Opened position with POSITION_TICKET = {result.order}")
    print(f"Sleep 2 seconds before closing position #{result.order}")
    time.sleep(2)

# Sell Market


def sell(symbol: str):
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
        "comment": "python script open sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    # Send a trading request
    result = mt5.order_send(request)
    # Check the execution result
    print(
        f"1. Sell order_send(): by {symbol} in {point} point {lot} lots at {price} with deviation = {deviation} points")
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"2. order_send() failed, retcode={result.retcode}")
        # Request the result as a dictionary and display it element by element
        result_dict = result._asdict()
        for field in result_dict.keys():
            print(f"{field}={result_dict[field]}")
            # If this is a trading request structure, display it element by element as well
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print(
                        f"traderequest: {tradereq_filed}={traderequest_dict[tradereq_filed]}")
        print("shutdown() and quit().")
        mt5.shutdown()
        quit()

    print("2. Sell order_send done, ", result)
    print(f"Opened position with POSITION_TICKET = {result.order}")
    print(f"Sleep 2 seconds before closing position #{result.order}")
    time.sleep(2)


symbol = "EURUSD"
buy(symbol)
# sell(symbol)
mt5.shutdown()

'''
symbols_icmarket = [EURUSD, GBPUSD, USDCHF, USDJPY, USDCNH,
 USDRUB, AUDUSD, NZDUSD, USDCAD, USDSEK,
 USDHKD, USDSGD, USDNOK, USDDKK, USDTRY,
 USDZAR, USDCZK, USDHUF, USDPLN, USDRUR, AUDCAD, AUDCHF,
 AUDJPY, AUDNZD, CADCHF, CADJPY, CHFJPY, EURAUD, EURCAD,
 EURCHF, EURCZK, EURDKK, EURGBP, EURHKD, EURHUF, EURJPY,
 EURNOK, EURNZD, EURPLN, EURRUR, EURRUB, EURSEK,
 EURTRY, EURZAR, GBPAUD, GBPCHF, GBPJPY, XAUUSD, XAUEUR, XAUAUD,
 XAGUSD, XAGEUR, GBPCAD, GBPNOK, GBPNZD, GBPPLN, GBPSEK, GBPSGD,
 GBPZAR, NZDCAD, NZDCHF, NZDJPY,
 NZDSGD, SGDJPY, XPDUSD, XPTUSD, USDGEL, USDMXN,
 EURMXN, GBPMXN, CADMXN, CHFMXN, MXNJPY, NZDMXN,
 USDCOP, USDARS, USDCLP, AUS200, FCHI40, GDAXIm, HSI50, ND100m,
 NI225, SP500m, SPN35, STOX50, UK100, Brent, Crude, NatGas,
 BRENT_V0, WTI_U0, XBRUSD, XNGUSD, XTIUSD, Cocoa_Z0, Coffee_Z0, Corn_U0,
 Cotton_Z0, OJ_U0, Soybean_U0, Sugar_V0, Wheat_U0, Wheat_Z0]
'''
