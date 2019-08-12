#%%
import exchange
import asyncio
import data
import importlib
import pprint
#%%
def test(ex,C):
    try:
        ex.get_json(C)
        ex.get_last(C)
        print(ex.name + " OK")
        pprint.pprint(ex.to_json())
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