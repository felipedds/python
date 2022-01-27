from bot import StrategyEMA, StrategyRSI
from datetime import datetime

if __name__ == '__main__':
    time_frames = {'mt5.TIMEFRAME_H12':'h12', 'mt5.TIMEFRAME_D1':'d1', 'mt5.TIMEFRAME_W1':'w1', 'mt5.TIMEFRAME_MN1':'mn1'}
    tickers = ['AUDCAD', 'AUDNZD', 'AUDUSD', 'CADCHF', 'EURAUD', 'EURCAD', 'EURCHF', 'EURHUF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'GBPNZD', 'USDCAD', 'USDCHF', 'USDJPY', 'USDMXN', 'USDSGD', 'USDTRY', 'NZDCAD', 'NZDUSD', 'NZDJPY', 'XAGUSD', 'XAUUSD']
    for ticker in tickers:
        print('\n')
        for time_frame in time_frames:
            StrategyRSI(ticker, datetime(2021, 1, 10), datetime(2021, 12, 31), time_frames[time_frame])
            StrategyEMA(ticker, datetime(2021, 1, 10), datetime(2021, 12, 31), time_frames[time_frame])