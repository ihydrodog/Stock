import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_selected(df, columns, start_index, end_index):
    plot_data( df.ix[start_index:end_index,columns])


def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv( symbol_to_path(symbol), parse_dates=True, index_col='Date', usecols=['Date','Adj Close'], na_values=['NaN'] )
        df_temp = df_temp.rename( columns={'Adj Close': symbol})
        df = df.join( df_temp )
        if symbol == 'SPY':
            df = df.dropna( subset=['SPY'])

    return df


def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def test_run():

    start_date = '2010-01-22'
    end_date = '2010-04-10'
    dates = pd.date_range( start_date, end_date )

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']

    # Get stock data
    df = get_data(symbols, dates)
    print( df )

    # Slice and plot
    plot_selected(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')

    print( df['SPY'].shift(1))


    # for symbol in ['AAPL', 'IBM']:
    #     plt.plot( get_dataframe( symbol )[['Volume','High']])
    #     plt.show()

if __name__ == "__main__":
    test_run()
