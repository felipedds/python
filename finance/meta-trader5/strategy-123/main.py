# https://quantbrasil.com.br/backtest-da-estrategia-123-utilizando-python
# https://www.youtube.com/watch?v=sq5ssVXoZB8 - Análise Quantitativa — Setup 123 de Compra ou Venda

# Import the libraries
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
from strategytester import StrategyTester
from robo import Robo
import time
import warnings

warnings.filterwarnings('ignore')

# MAIN
if __name__ == '__main__':
    while True:
        symbols = ['XAUUSD']
        #symbols = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'GBPNZD', 'USDCAD', 'USDCHF', 'USDJPY', 'USDSGD', 'NZDUSD', 'NZDJPY', 'XAGUSD', 'XAUUSD']
        time_frames = [mt5.TIMEFRAME_H12]
        #time_frames = [mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H8 ,mt5.TIMEFRAME_H12, mt5.TIMEFRAME_D1]
        for symbol in symbols:
            print(f'\n {symbol}')
            for time_frame in time_frames:
                robo = Robo(symbol, datetime(2022, 5, 30), datetime(2022, 10, 30), time_frame)
                print(robo.strategy())
                ''' BACKTEST           
                strategy_tester = StrategyTester(symbol, datetime(2010, 1, 1), datetime(2022, 10, 10), time_frame)
                # capital fixo(initial_capital) de R$100.000  e um risco controlado(capital_exposure) de R$1.000 
                all_profits, total_capital = strategy_tester.backtest(capital_exposure=1000, initial_capital=100000) # capital_exposure=1000, initial_capital=100000
                statistics = strategy_tester.strategy_test(all_profits, total_capital)
                statistics = pd.DataFrame.from_dict(statistics, orient='index')
                print(statistics.round(2))
                strategy_tester.capital_plot(symbol, time_frame, total_capital, all_profits)
                ev = strategy_tester.expected_value(all_profits)
                print(ev)
                '''
        time.sleep(300) # Sleep 300 seconds