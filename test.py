#%%
import exchange
import asyncio
import data
import importlib
#%%
def test(ex,C):
    try:
        ex.get_json(C)
        ex.get_last(C)
        print(ex.name + " OK")
        if(issubclass(type(ex), data.KRWLast)):
            print("    ", ex.name, 'KRW', ex.KRW_last)
        if(issubclass(type(ex), data.BTCLast)):
            print("    ", ex.name, 'BTC', ex.BTC_last)
        if(issubclass(type(ex), data.USDTLast)):
            print("    ", ex.name, 'USDT', ex.USDT_last)
        if(issubclass(type(ex), data.ETHLast)):
            print("    ", ex.name, 'ETH', ex.ETH_last)
    except Exception as e:
        print(ex.name + " FAILED")
        print("    failed " +ex.name+ " with error code: {}".format(e))
#%%
importlib.reload(exchange)
E = [
    exchange.Binance(),
    exchange.Coinnest(),
    exchange.Coinone(),
    exchange.Coinrail(),
    exchange.Cpdax(),
    exchange.GateIO(),
    exchange.Gopax(),
    exchange.Kucoin(),
    exchange.Poloniex(),
    exchange.Bittrex(),
    exchange.Bithumb(),
    exchange.Upbit(),
    exchange.Bitfinex(),
    exchange.Liqui(),
    exchange.Hitbtc(),
    exchange.CexIO()
]
C = ["BTC","OMG","BCH","ETC","ETH","STEEM","EOS","XRP","NoneCin"]
for e in E:
    test(e,C)