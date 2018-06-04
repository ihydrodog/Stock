import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order_target, record, symbol
from zipline.algorithm import TradingAlgorithm

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 3, 29)
data = web.DataReader("AAPL", "yahoo", start, end)

#plt.plot(data.index, data['Adj Close'])
#plt.show()

data = data[['Adj Close']]
data.columns = ['AAPL']
data = data.tz_localize('UTC')

print(data.head())

def initialize(context):
    context.i = 0
    context.sym = symbol('AAPL')

def handle_data(context, data):
    context.i += 1
    short,long = 20,100
    if context.i < long:
        return

    ma5 = data.history(context.sym, 'price', short, '1d').mean()
    ma20 = data.history(context.sym, 'price', long, '1d').mean()

    if ma5 > ma20:
        order_target(context.sym, 100)
    else:
        order_target(context.sym, -100)

    record(AAPL=data.current(context.sym, "price"), ma5=ma5, ma20=ma20)

algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(data)

print( result.info() )

figure = plt.figure()

ax1 = figure.add_subplot( 211 )
result[ 'portfolio_value'].plot( ax =ax1 )

ax2 = figure.add_subplot( 212 )
result[ 'AAPL'].plot( ax =ax2 )
result[ ['ma5','ma20'] ].plot( ax =ax2 )


perf_trans = result.ix[[t != [] for t in result.transactions]]
buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
sells = perf_trans.ix[
    [t[0]['amount'] < 0 for t in perf_trans.transactions]]
ax2.plot(buys.index, result.ma5.ix[buys.index],
         '^', markersize=10, color='m')
ax2.plot(sells.index, result.ma5.ix[sells.index],
         'v', markersize=10, color='k')

plt.show()

print( result['portfolio_value'].tail() )