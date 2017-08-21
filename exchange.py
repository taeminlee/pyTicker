import json
import requests as req
import re
from collections import OrderedDict

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
    btc_krw = ticker["data"]['ClosePrice']
    KRW_last["BTC"] = float(btc_krw)
    for currency in currency_list:
        res = req.get("http://coinis.co.kr/api/sise/ticker?itemcode="+currency+"KRW")
        if(res.ok):
            ticker = json.loads(res.text)
            if(len(ticker['data']) > 0):
                BTC_last[currency] = float(ticker['data']['ClosePrice']) / float(btc_krw)
                KRW_last[currency] = float(ticker['data']['ClosePrice'])
    return BTC_last, KRW_last

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
            BTC_last[currency] = float(ticker['last_price'])
            USDT_last[currency] = float(ticker['last_price']) * btc_USDT
    return BTC_last, USDT_last

def get_liqui_last(currency_list):
    BTC_last = OrderedDict()
    for currency in currency_list:
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