import yfinance as yf
import sqlite3

# Create tables in database.
def create_tables_forex():
    # Parameters to database URL.
    params_dic = {
         'host': 'localhost',
         'database': '../data/forex.db'
    }
    try:
        currency_pair = ['AUDCAD', 'AUDNZD', 'AUDUSD', 'CADCHF', 'EURAUD', 'EURBRL', 'EURCAD', 'EURCHF', 'EURHUF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'GBPNZD', 'USDCAD', 'USDCHF', 'USDJPY', 'USDMXN', 'USDSGD', 'USDTRY', 'NZDCAD', 'NZDUSD', 'NZDJPY']
        for currency in currency_pair:
            time_frames = ['1d', '1wk', '1mo', '3mo'] # Intervals: “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
            for time_frame in time_frames:
                connection = sqlite3.connect(f"{params_dic['database']}")
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS "+currency.lower()+'_'+time_frame+" (date STRING PRIMARY KEY, open FLOAT NOT NULL, high FLOAT NOT NULL, low FLOAT NOT NULL, close FLOAT NOT NULL);")
                cursor.close()
                connection.close()
                print(f'{currency.lower()}_{time_frame} \nCreate with success.')
    except (RuntimeError, TypeError, NameError, ValueError, KeyboardInterrupt) as err:
        print(err)
        pass

def create_tables_commodities():
    # Parameters to database URL.
    params_dic = {
         'host': 'localhost',
         'database': '../data/commodities.db'
    }
    try:
        commodities = ['BZ', 'CL', 'GC', 'SI']
        for commodity in commodities:
            time_frames = ['1d', '1wk', '1mo', '3mo'] # Intervals: “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
            for time_frame in time_frames:
                connection = sqlite3.connect(f"{params_dic['database']}")
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS "+commodity.lower()+'_'+time_frame+" (date STRING PRIMARY KEY, open FLOAT NOT NULL, high FLOAT NOT NULL, low FLOAT NOT NULL, close FLOAT NOT NULL);")
                cursor.close()
                connection.close()
                print(f'{commodity.lower()}_{time_frame} \nCreate with success.')
    except (RuntimeError, TypeError, NameError, ValueError, KeyboardInterrupt) as err:
        print(err)
        pass    

# Insert the dataset in database.
def insert_data_forex():
    params_dic = {
         'host': 'localhost',
         'database': '../data/forex.db'
    }
    currency_pair = ['AUDCAD', 'AUDNZD', 'AUDUSD', 'CADCHF', 'EURAUD', 'EURBRL', 'EURCAD', 'EURCHF', 'EURHUF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'GBPNZD', 'USDCAD', 'USDCHF', 'USDJPY', 'USDMXN', 'USDSGD', 'USDTRY', 'NZDCAD', 'NZDUSD', 'NZDJPY']
    for currency in currency_pair:
        time_frames = ['1d', '1wk', '1mo', '3mo'] # Intervals: “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
        for time_frame in time_frames:
            ticket = yf.Ticker(f'{currency}=X')
            dataset = ticket.history(period='max', interval=time_frame, auto_adjust=True).drop(columns=['Volume', 'Dividends', 'Stock Splits']).rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}) # periods: “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
            dataset['date'] = dataset.index
            dataset.reset_index(drop=True, inplace=True)
            for i in dataset.index:
                connection = sqlite3.connect(f"{params_dic['database']}")
                cursor = connection.cursor()
                cursor.execute("INSERT OR IGNORE INTO "+currency.lower()+"_"+time_frame+" (date, open, high, low, close) VALUES(?, ?, ?, ?, ?);", (str(dataset['date'][i]), float(dataset['open'][i]), float(dataset['high'][i]), float(dataset['low'][i]), float(dataset['close'][i])))
                connection.commit()
                cursor.close()
                connection.close()
            print(f'{currency.lower()}_{time_frame} \nInsert with success. {cursor.rowcount}')
    print('Finished with success.')


# Insert the dataset in database.
def insert_data_commodities():
    params_dic = {
         'host': 'localhost',
         'database': '../data/commodities.db'
    }
    commodities = ['BZ', 'CL', 'GC', 'SI']
    for commodity in commodities:
        time_frames = ['1d', '1wk', '1mo', '3mo'] # Intervals: “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
        for time_frame in time_frames:
            ticket = yf.Ticker(f'{commodity}=F')
            dataset = ticket.history(period='6mo', interval=time_frame, auto_adjust=True).rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}) # periods: “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
            dataset['date'] = dataset.index
            dataset.reset_index(drop=True, inplace=True)
            for i in dataset.index:
                connection = sqlite3.connect(f"{params_dic['database']}")
                cursor = connection.cursor()
                cursor.execute("INSERT OR IGNORE INTO "+commodity.lower()+"_"+time_frame+" (date, open, high, low, close) VALUES(?, ?, ?, ?, ?);", (str(dataset['date'][i]), float(dataset['open'][i]), float(dataset['high'][i]), float(dataset['low'][i]), float(dataset['close'][i])))
                connection.commit()
                cursor.close()
                connection.close()
            print(f'{commodity.lower()}_{time_frame} \nInsert with success. {cursor.rowcount}')
    print('Finished with success.')


def delete_tables():
    # Parameters to database URL.
    params_dic = {
         'host': 'localhost',
         'database': '../data/forex.db'
    }
    try:
        currency_pair = ['XAUUSD', 'XAGUSD']
        for currency in currency_pair:
            time_frames = ['1d', '1wk', '1mo', '3mo'] # Intervals: “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
            for time_frame in time_frames:
                connection = sqlite3.connect(f"{params_dic['database']}")
                cursor = connection.cursor()
                cursor.execute("DROP TABLE "+currency.lower()+'_'+time_frame+";")
                cursor.close()
                connection.close()
                print(f'{currency.lower()}_{time_frame} \nDelete with success.')
    except (RuntimeError, TypeError, NameError, ValueError, KeyboardInterrupt) as err:
        print(err)
        pass


if __name__ == '__main__':
    #create_tables_forex()
    #create_tables_commodities()
    #delete_tables()
    insert_data_forex()
    insert_data_commodities()