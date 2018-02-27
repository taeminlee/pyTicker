import requests as req
import json
import re
import datetime
from collections import OrderedDict
import asyncio
import util
from data import BTCLast, USDTLast, KRWLast, BNBLast, ETHLast, PercentChanges
from network import JsonLoaderAsync, JsonLoaderRQ

class Exchange:
    name = ""
    msg = ""
    symbol = ""
    version = ""
    rst = False
    json_time = datetime.datetime.now()
    last_time = datetime.datetime.now()
    def get_json(self, currency_list): # 거래소 별 json 다운로드 로직
        pass
    def get_last(self, currency_list): # 거래소 별 last price parsing 로직
        pass
    def debug(self, error_msg):
        print(error_msg)
    def _run(self, currency_list):
        try:
            self.get_json(currency_list)
            self.json_time = datetime.datetime.now()
        except:
            self.debug("ERROR : %s get_json : %s" % (self.name, self.msg))
            return False
        try:
            self.get_last(currency_list)
            self.last_time = datetime.datetime.now()
            return True
        except:
            self.debug("ERROR : %s get_last : %s" % (self.name, self.msg))
            return False
    def run(self, currency_list):
        self._run(currency_list)
    async def async_run(self, currency_list):
        self._run(currency_list)

class Poloniex(Exchange, JsonLoaderRQ, BTCLast, USDTLast, PercentChanges):
    name = "Poloniex"
    symbol = "polo"
    version = "Poloniex 1.0 JsonLoaderRQ"
    def get_json(self, currency_list):
        self.json = self.load_single_json("https://poloniex.com/public?command=returnTicker")
    def get_last(self, currency_list):
        self.msg = "usdt_last btc"
        self.USDT_last['BTC'] = float(self.json["USDT_BTC"]['last'])
        for currency in currency_list:
            if "BTC_"+currency in self.json:
                self.msg = "percent_changes %s" % currency
                self.percent_changes[currency] = float(self.json["BTC_"+currency]['percentChange'])
                self.msg = "btc_last %s" % currency
                self.BTC_last[currency] = float(self.json["BTC_"+currency]['last'])
            if "USDT_"+currency in self.json:
                self.msg = "usdt_last %s" % currency
                self.USDT_last[currency] = float(self.json["USDT_"+currency]['last'])

class Binance(Exchange, JsonLoaderRQ, BTCLast, USDTLast, ETHLast, BNBLast):
    name = "Binance"
    symbol = "bin"
    version = "Binance 1.0 JsonLoaderRQ"
    def get_json(self, currency_list):
        self.json = {}
        self.rawJson = self.load_single_json("https://api.binance.com/api/v1/ticker/allPrices")
        self.json = dict(map(lambda dict:(dict['symbol'], dict['price']), self.rawJson))
    def get_last(self, currency_list):
        self.msg = "get_last"
        patch = {"BCH":"BCC"}
        for currency in currency_list:
            currency_str = currency
            if currency in patch:
                currency_str = patch[currency]
            self.msg = "get_last : %s" % currency_str
            for kv in {"BTC":self.BTC_last, "USDT":self.USDT_last, "ETH":self.ETH_last, "BNB":self.BNB_last}.items():
                self.msg = "get_last : %s %s " % (currency, kv[0])
                if "%s%s" % (currency_str, kv[0]) in self.json:
                    self.msg = "get_last parse : %s%s" % (currency, kv[0])
                    kv[1][currency] = float(self.json['%s%s' % (currency_str, kv[0])])

class Gopax(Exchange, JsonLoaderAsync, KRWLast):
    name = "Gopax"
    symbol = "go"
    version = "Gopax 1.0 JsonLoaderAsync"
    supported_currencies = []
    #def __init__(self):
        #https://api.gopax.co.kr/trading-pairs
        #loop = asyncio.get_event_loop()
        #task = asyncio.ensure_future(self.load_single_json(url = "https://api.gopax.co.kr/trading-pairs"))
        #loop.run_until_complete(task)
        #loop.close()
        #for record in task.result():
        #   self.supported_currencies.append(record["baseAsset"])
    def get_json(self, currency_list):
        #https://api.gopax.co.kr/trading-pairs/BTC-KRW/ticker
        #C = set(self.supported_currencies).intersection(set(currency_list))
        C = ['BTC'] + currency_list
        self.krw_urls = dict(map(lambda currency:(currency, "https://api.gopax.co.kr/trading-pairs/%s-KRW/ticker" % currency), C))
        temp_jsons = self.load_multiple_json(self.krw_urls)
        self.json = dict(map(lambda json:(json['currency'], json), temp_jsons))
    def get_last(self, currency_list):
        C = ['BTC'] + currency_list
        for currency in C:
           self.msg = "get_last : %s" % currency
           #print(self.json)
           if currency in self.json:
               if 'price' in self.json[currency]:
                   self.KRW_last[currency] = self.json[currency]['price']

class Coinone(Exchange, JsonLoaderRQ, KRWLast):
    name = "Coinone"
    symbol = "co"
    version = "Coinone 1.0 JsonLoaderRQ"
    def get_json(self, currency_list):
        self.json = self.load_single_json("https://api.coinone.co.kr/ticker/?format=json&currency=btn")
    def get_last(self, currency_list):
        for currency in currency_list:
            self.msg = "krw_last %s" % currency
            if currency.lower() in self.json:
                if 'last' in self.json[currency.lower()]:
                    self.KRW_last[currency] = float(self.json[currency.lower()]['last'])
            
class Upbit(Exchange, JsonLoaderAsync, KRWLast, BTCLast, USDTLast):
    name = "Upbit"
    symbol = "up"
    version = "Upbit 1.0 JsonLoaderAsync"
    def get_json(self, currency_list):
        # https://crix-api-endpoint.upbit.com/v1/crix/trades/ticks?code=CRIX.UPBIT.KRW-BTC&count=1
        # https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-BTC&count=1
        self.krw_urls = dict(map(lambda currency:(currency, "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/60?code=CRIX.UPBIT.KRW-%s&count=1" % currency), currency_list))
        self.usdt_urls = dict(map(lambda currency:(currency, "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/60?code=CRIX.UPBIT.USDT-%s&count=1" % currency), currency_list))
        self.btc_urls = dict(map(lambda currency:(currency, "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/60?code=CRIX.UPBIT.BTC-%s&count=1" % currency), currency_list))
        self.krw_jsons = self.load_multiple_json(self.krw_urls)
        self.usdt_jsons = self.load_multiple_json(self.usdt_urls)
        self.btc_jsons = self.load_multiple_json(self.btc_urls)
    def get_last(self, currency_list):
        extype_dict = {'usdt_last' : (self.usdt_jsons, self.USDT_last), 'krw_last' : (self.krw_jsons, self.KRW_last), 'btc_last' : (self.btc_jsons, self.BTC_last)}
        for currency in currency_list:
            for extype in list(extype_dict.items()):
                #print(extype)
                for json in filter(lambda json:json['currency'] == currency, extype[1][0]):
                    self.msg = "%s %s" % (extype[0], currency)
                    extype[1][1][currency] = json['tradePrice']

class GateIO(Exchange, JsonLoaderRQ, BTCLast, USDTLast, ETHLast):
    name = "Gate.IO"
    symbol = "gate"
    version = "Gate.IO 1.0 JsonLoaderRQ"
    def get_json(self, currency_list):
        self.json = {}
        self.rawJson = self.load_single_json("http://data.gate.io/api2/1/tickers")
        self.json = dict(map(lambda dict:(dict[0], dict[1]['last']), self.rawJson.items()))
    def get_last(self, currency_list):
        self.msg = "get_last"
        for currency in currency_list:
            self.msg = "get_last : %s" % currency
            for kv in {"btc":self.BTC_last, "usdt":self.USDT_last, "ETH":self.ETH_last}.items():
                self.msg = "get_last : %s %s " % (currency, kv[0])
                if "%s_%s" % (currency.lower(), kv[0]) in self.json:
                    self.msg = "get_last parse : %s %s" % (currency, kv[0])
                    kv[1][currency] = float(self.json['%s_%s' % (currency.lower(), kv[0])])

def get_polo_last(currency_list):
    BTC_last = OrderedDict()
    percent_changes = OrderedDict()
    USDT_last = OrderedDict()
    res = req.get("https://poloniex.com/public?command=returnTicker")
    polo = json.loads(res.text)
    USDT_last['BTC'] = float(polo["USDT_BTC"]['last'])
    for currency in currency_list:
        if "BTC_"+currency in polo:
            percent_changes[currency] = float(polo["BTC_"+currency]['percentChange'])
            BTC_last[currency] = float(polo["BTC_"+currency]['last'])
        if "USDT_"+currency in polo:
            USDT_last[currency] = float(polo["USDT_"+currency]['last'])
    return BTC_last, USDT_last, percent_changes, polo

def get_bithumb_json(str):
    m = re.search('{.*}', str)
    return m.group(0)

def get_bithumb_last(currency_list):
    BTC_last = OrderedDict()
    KRW_last = OrderedDict()
    btc_res = req.get("https://api.bithumb.com/public/ticker")
    btc_ticker = json.loads(get_bithumb_json(btc_res.text))
    if btc_ticker['status'] == 5600:
        return BTC_last, KRW_last;
    btc_krw = btc_ticker['data']['closing_price']
    KRW_last["BTC"] = float(btc_krw)
    for currency in currency_list:
        res = req.get("https://api.bithumb.com/public/ticker/"+currency)
        if(res.ok):
            ticker = json.loads(get_bithumb_json(res.text))
            BTC_last[currency] = float(ticker['data']['closing_price']) / float(btc_krw)
            KRW_last[currency] = float(ticker['data']['closing_price'])
    return BTC_last, KRW_last

def get_coinone_last(currency_list):
    BTC_last = OrderedDict()
    KRW_last = OrderedDict()
    res = req.get("https://api.coinone.co.kr/ticker/?format=json&currency=btn")
    ticker = json.loads(res.text)
    btc_krw = ticker["btc"]['last']
    KRW_last["BTC"] = float(btc_krw)
    for currency in currency_list:
        if currency.lower() in ticker:
            BTC_last[currency] = float(ticker[currency.lower()]['last']) / float(btc_krw)
            KRW_last[currency] = float(ticker[currency.lower()]['last'])
    return BTC_last, KRW_last

def get_coinis_last(currency_list):
    BTC_last = OrderedDict()
    KRW_last = OrderedDict()
    res = req.get("http://coinis.co.kr/api/sise/ticker?itemcode=BTCKRW")
    ticker = json.loads(res.text)
    if ticker['result'] == -1 :
        return BTC_last, KRW_last;
    btc_krw = ticker["data"]['ClosePrice']
    KRW_last["BTC"] = float(btc_krw)
    for currency in currency_list:
        if currency == "ETH" or currency == "ETC":
            continue
        if currency == "BCH":
            res = req.get("http://coinis.co.kr/api/sise/ticker?itemcode=BCCKRW")
        else:
            res = req.get("http://coinis.co.kr/api/sise/ticker?itemcode="+currency+"KRW")
        if(res.ok):
            ticker = json.loads(res.text)
            if(len(ticker['data']) > 0):
                BTC_last[currency] = float(ticker['data']['ClosePrice']) / float(btc_krw)
                KRW_last[currency] = float(ticker['data']['ClosePrice'])
    return BTC_last, KRW_last

def get_coinrail_last(currency_list):
    BTC_last = OrderedDict()
    KRW_last = OrderedDict()
    btc_res = req.get("https://api.coinrail.co.kr/public/last/order?currency=btc-krw")
    btc_ticker = json.loads(btc_res.text)
    if btc_ticker['error_code'] != 0:
        return BTC_last, KRW_last
    btc_krw = btc_ticker['last_price']
    KRW_last["BTC"] = float(btc_krw)
    for currency in currency_list:
        res = req.get("https://api.coinrail.co.kr/public/last/order?currency=%s-krw" % currency.lower())
        if(res.ok):
            ticker = json.loads(res.text)
            if ticker['error_code'] == 0:
                BTC_last[currency] = float(ticker['last_price']) / float(btc_krw)
                KRW_last[currency] = float(ticker['last_price'])
    return BTC_last, KRW_last

def get_bittrex_last(currency_list):
    #https://bittrex.com/api/v1.1/public/getmarketsummaries   
    BTC_last = OrderedDict()
    USDT_last = OrderedDict()
    res = req.get("https://bittrex.com/api/v1.1/public/getmarketsummaries")
    if res.ok != True :
        return BTC_last, USDT_last
    bittrex = json.loads(res.text)
    if bittrex['success'] != True:
        return BTC_last, USDT_last
    USDT_last['BTC'] = float(get_bittrex_currency('USDT-BTC', bittrex)['Last'])
    for currency in currency_list:
        if currency == 'BCH':
            x = get_bittrex_currency("BTC-BCC", bittrex)
        else:
            x = get_bittrex_currency("BTC-"+currency, bittrex)
        if x != None:
            BTC_last[currency] = float(x['Last'])
    return BTC_last, USDT_last

def get_bittrex_currency(currency, json):
    x = list(filter(lambda x: x['MarketName'] == currency, json['result']))
    if len(x) == 0:
        return None
    return x[0]

def get_bitfinex_last(currency_list):
    BTC_last = OrderedDict()
    USDT_last = OrderedDict()
    btc_res = req.get("https://api.bitfinex.com/v1/pubticker/BTCUSD")
    btc_ticker = json.loads(btc_res.text)
    btc_USDT = float(btc_ticker['last_price'])
    for currency in currency_list:
        if currency == "DASH":
            res = req.get("https://api.bitfinex.com/v1/pubticker/DSHBTC")
        else:
            res = req.get("https://api.bitfinex.com/v1/pubticker/"+currency+"BTC")
        if res.ok:
            ticker = json.loads(res.text)
            if 'last_price' in ticker:
                BTC_last[currency] = float(ticker['last_price'])
                USDT_last[currency] = float(ticker['last_price']) * btc_USDT
    return BTC_last, USDT_last

def get_liqui_last(currency_list):
    BTC_last = OrderedDict()
    for currency in currency_list:
        if currency == "STEEM" or currency == "SBD":
            continue
        if currency == "BCH":
            res = req.get("https://api.liqui.io/api/3/ticker/bcc_btc")
        else:
            res = req.get("https://api.liqui.io/api/3/ticker/"+currency.lower()+"_btc")
        if res.ok:
            ticker = json.loads(res.text)
            if currency == "BCH":
                BTC_last[currency] = float(ticker['bcc_btc']['last'])
            if currency.lower()+'_btc' in ticker:
                BTC_last[currency] = float(ticker[currency.lower()+'_btc']['last'])
    return BTC_last

def get_hitbtc_last(currency_list):
    BTC_last = OrderedDict()
    res = req.get("https://api.hitbtc.com/api/1/public/ticker")
    hitbtc = json.loads(res.text)
    for currency in currency_list:
        if currency+"BTC" in hitbtc:
            BTC_last[currency] = float(hitbtc[currency+"BTC"]['last'])
    return BTC_last

def get_cex_io_last():
    USDT_last = OrderedDict()
    btc_res = req.get("https://cex.io/api/last_price/BTC/USD")
    if btc_res.ok:
        btc_ticker = json.loads(btc_res.text)
        USDT_last["BTC"] = float(btc_ticker["lprice"])
        USDT_last["buy"] = USDT_last["BTC"] * 1.07
        USDT_last["visa"] = USDT_last["buy"] * 1.035
        USDT_last["fee"] = USDT_last["visa"] * 1.02
    return USDT_last

def get_exchange_rate():
    res = req.get("http://api.fixer.io/latest?base=USD&symbols=KRW")
    USD2KRW = json.loads(res.text)["rates"]["KRW"]
    return USD2KRW