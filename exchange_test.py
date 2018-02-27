#%%
import exchange
from pprint import pprint

print("IMPORT COMPLETE")

#%% kucoin
k = exchange.Kucoin()
k.run(['BTC','ETH','XRP','LTC','NONE'])
print(k.BTC_last)
print(k.USDT_last)
print(k.ETH_last)