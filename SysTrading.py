import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order_target, order, order_percent, record, symbol
from zipline.algorithm import TradingAlgorithm

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 3, 29)
# end = datetime.datetime(2011, 1, 1)
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

    sma = data.history(context.sym, 'price', short, '1d').mean()
    lma = data.history(context.sym, 'price', long, '1d').mean()

    if sma > lma:
        order_percent(context.sym, 1)
    else:
    # elif sma < lma:
    #     order_percent(context.sym, 0)
        pass

    record(AAPL=data.current(context.sym, "price"), sma=sma, lma=lma)

algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data )
result = algo.run(data)

print( result.info() )

figure = plt.figure()

ax1 = figure.add_subplot( 211 )
result[ 'portfolio_value'].plot( ax =ax1 )

ax2 = figure.add_subplot( 212 )
result[ 'AAPL'].plot( ax =ax2 )
result[ ['sma','lma'] ].plot( ax =ax2 )


perf_trans = result.ix[[t != [] for t in result.transactions]]
buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
sells = perf_trans.ix[
    [t[0]['amount'] < 0 for t in perf_trans.transactions]]
ax2.plot(buys.index, result.sma.ix[buys.index],
         '^', markersize=5, color='m')
ax2.plot(sells.index, result.sma.ix[sells.index],
         'v', markersize=5, color='k')
print( result['portfolio_value'].head() )
print( result['portfolio_value'].tail() )

print( result['portfolio_value'] )
plt.show()

