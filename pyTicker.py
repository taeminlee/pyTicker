# import python libs
import sys
import re
import argparse
import sched
import time
import json
from datetime import datetime
from collections import OrderedDict
# import additional libs
import requests as req
from prettytable import PrettyTable
import pygame
# import pyTicker libs
import exchange
import util

parser = argparse.ArgumentParser(description="cryptocurrency ticker comparer suite")
parser.add_argument('-polo', action="store_false", default=True, help="disable getting ticker from poloniex")
parser.add_argument('-btx', action="store_true", default=False, help="enable getting ticker from bittrex")
parser.add_argument('-bfx', action="store_true", default=False, help="enable getting ticker from bitfinex")
parser.add_argument('-hitbtc', action="store_true", default=False, help="enable getting ticker from hitbtc")
parser.add_argument('-liqui', action='store_true', default=False, help='enable getting ticker from liqui.io')
parser.add_argument('-binance', action="store_true", default=False, help="enable getting ticker from binance")
parser.add_argument('-gopax', action="store_true", default=False, help="enable getting ticker from gopax")
parser.add_argument('-gate', action="store_true", default=False, help="enable getting ticker from gate.io")
parser.add_argument('-bt', action="store_false", default=True, help="disable getting ticker from bithumb")
parser.add_argument('-co', action="store_false", default=True, help="disable getting ticker from coinone")
parser.add_argument('-ci', action="store_false", default=True, help="disable getting ticker from coinis")
parser.add_argument('-cr', action="store_false", default=True, help="disable getting ticker from coinrail")
parser.add_argument('-alarm', action='store_false', default=True, help='disable alarm')
parser.add_argument('-eth', action='store_true', default=False, help='disable ETH ticker')
parser.add_argument('-dash', action='store_true', default=False, help='disable DASH ticker')
parser.add_argument('-ltc', action='store_true', default=False, help='disable LTC ticker')
parser.add_argument('-etc', action='store_true', default=False, help='disable ETC ticker')
parser.add_argument('-zec', action='store_true', default=False, help='disable ZEC ticker')
parser.add_argument('-xmr', action='store_true', default=False, help='disable XMR ticker')
parser.add_argument('-bch', action='store_true', default=False, help='disable BCH ticker')
parser.add_argument('-xrp', action='store_true', default=False, help='enable XRP(ripple) ticker')
parser.add_argument('-qtum', action='store_true', default=False, help='enable QTUM ticker')
parser.add_argument('-steem', action='store_true', default=False, help='enable STEEM ticker')
parser.add_argument('-sbd', action='store_true', default=False, help='enable SBD ticker')
parser.add_argument('-eos', action='store_true', default=False, help='enable EOS ticker')
parser.add_argument('-btg', action='store_true', default=False, help='enable BTG ticker')
parser.add_argument('-iota', action='store_true', default=False, help='enable IOTA ticker')
parser.add_argument('-xlm', action='store_true', default=False, help='enable XLM ticker')
args = parser.parse_args()

#currencies = ["ETH", "DASH", "LTC", "ETC", "ZEC", "XRP", "BCH"]
#cols = ["ETH","DASH","LTC","ETC","ZEC", "XRP","BCH", "BTC"]
currencies = ["ETH", "DASH", "LTC", "ETC", "ZEC", "XMR", "BCH"]
cols = ["ETH","DASH","LTC","ETC","ZEC", "XMR", "BCH", "BTC"]
duration = 1 #sec

s = sched.scheduler(time.time, time.sleep)

if args.alarm:
    pygame.mixer.init()
    pygame.mixer.music.load("hangout.mp3")

def add_currency(currency):
    currencies.insert(len(currencies)-2, currency)
    cols.insert(len(cols)-3, currency)
def remove_currency(currency):
    currencies.remove(currency)
    cols.remove(currency)

if args.eth:
    remove_currency('ETH')
if args.dash:
    remove_currency('DASH')
if args.ltc:
    remove_currency('LTC')
if args.etc:
    remove_currency('ETC')
if args.zec:
    remove_currency('ZEC')
if args.xmr:
    remove_currency('XMR')
if args.bch:
    remove_currency('BCH')
if args.xrp:
    add_currency('XRP')
if args.qtum:
    add_currency('QTUM')
if args.steem:
    add_currency('STEEM')
if args.sbd:
    add_currency('SBD')
if args.eos:
    add_currency('EOS')
if args.iota:
    add_currency('IOTA')
if args.xlm:
    add_currency('XLM')

print("init pyTicker.. It takes several seconds..")

if args.binance:
    binance = exchange.Binance()
if args.gate:
    gate = exchange.GateIO()
if args.gopax:
    gopax = exchange.Gopax()

def run_ticker(sc): 
    try:
        if args.polo:
            polo_last, polo_USDT_last, polo_percent_changes, polo_json = exchange.get_polo_last(currencies)
        if args.btx:
            bittrex_last, bittrex_USDT_last = exchange.get_bittrex_last(currencies)
        if args.bfx:
            bitfinex_last, bitfinex_USDT_last = exchange.get_bitfinex_last(currencies)
        if args.hitbtc:
            hitbtc_last = exchange.get_hitbtc_last(currencies)
        if args.binance:
            binance.run(currencies)
            binance_last = binance.BTC_last
        if args.gopax:
            gopax.run(currencies)
            gopax_KRW_last = gopax.KRW_last
            gopax_last = dict(map(lambda kv: (kv[0], kv[1] / gopax_KRW_last['BTC']), gopax_KRW_last.items()))
        if args.gate:
            gate.run(currencies)
            gate_last = gate.BTC_last
        if args.bt:
            bithumb_last, bithumb_KRW_last = exchange.get_bithumb_last(currencies)
        if args.co:
            coinone_last, coinone_KRW_last = exchange.get_coinone_last(currencies)
        if args.ci:
            coinis_last, coinis_KRW_last = exchange.get_coinis_last(currencies)
        if args.cr:
            coinrail_last, coinrail_KRW_last = exchange.get_coinrail_last(currencies)
        if args.liqui:
            liqui_last = exchange.get_liqui_last(currencies)
        if args.polo and args.bt:
            BP_diff_last = util.get_diff_last(bithumb_last, polo_last)
        if args.btx and args.bt:
            BBT_diff_last = util.get_diff_last(bithumb_last, bittrex_last)
        if args.bfx and args.bt:
            BB_diff_last = util.get_diff_last(bithumb_last, bitfinex_last)
        if args.polo and args.co:
            CP_diff_last = util.get_diff_last(coinone_last, polo_last)
        if args.btx and args.co:
            CBT_diff_last = util.get_diff_last(coinone_last, bittrex_last)
        if args.binance and args.co:
            CBI_diff_last = util.get_diff_last(coinone_last, binance_last)
        if args.gate and args.co:
            CGA_diff_last = util.get_diff_last(coinone_last, gate_last)
        if args.liqui and args.co:
            CL_diff_last = util.get_diff_last(coinone_last, liqui_last)
        if args.btx and args.gopax:
            GBT_diff_last = util.get_diff_last(gopax_last, bittrex_last)
        if args.binance and args.gopax:
            GBI_diff_last = util.get_diff_last(gopax_last, binance_last)
        if args.polo and args.ci:
            CIP_diff_last = util.get_diff_last(coinis_last, polo_last)
        if args.polo and args.cr:
            CRP_diff_last = util.get_diff_last(coinrail_last, polo_last)
        if args.polo and args.liqui:
            LP_diff_last = util.get_diff_last(liqui_last, polo_last)
        if args.polo and args.hitbtc:
            HP_diff_last = util.get_diff_last(hitbtc_last, polo_last)

        t = PrettyTable(["Index"] + cols)
        if args.polo:
            t.add_row(['polo (BTC)'] + util.make_row(cols, {k:v for (k,v) in polo_last.items()}, 6))
            t.add_row(['polo (USDT)'] + util.make_row(cols, {k:v for (k,v) in polo_USDT_last.items()}, 2, True))
            t.add_row(['polo (+)'] + util.make_row(cols, {k:v for(k,v) in polo_percent_changes.items() if v > 0}, 6, True))
            t.add_row(['polo (-)'] + util.make_row(cols, {k:v for(k,v) in polo_percent_changes.items() if v <= 0}, 6, True))
        if args.bfx:
            t.add_row(['bitfinex (BTC)'] + util.make_row(cols, {k:v for (k,v) in bitfinex_last.items()}, 6))
            t.add_row(['bitfinex (USDT)'] + util.make_row(cols, {k:v for (k,v) in bitfinex_USDT_last.items()}, 2, True))
        if args.binance:
            t.add_row(['binance (BTC)'] + util.make_row(cols, {k:v for (k,v) in binance_last.items()}, 6))
        if args.gate:
            t.add_row(['gate.IO (BTC)'] + util.make_row(cols, {k:v for (k,v) in gate_last.items()}, 6))
        if args.btx:
            t.add_row(['bittrex (BTC)'] + util.make_row(cols, {k:v for (k,v) in bittrex_last.items()}, 6))
            t.add_row(['bittrex (USDT)'] + util.make_row(cols, {k:v for (k,v) in bittrex_USDT_last.items()}, 2, True))
        if args.bt:
            t.add_row(['bithumb (BTC)'] + util.make_row(cols, {k:v for (k,v) in bithumb_last.items()}, 6))
            t.add_row(['bithumb (KRW)'] + util.make_row(cols, {k:v for (k,v) in bithumb_KRW_last.items()}, 0, True))
        if args.polo and args.bt:
            t.add_row(['positive Bt-Po'] + util.make_row(cols, {k:v for (k,v) in BP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Bt-Po'] + util.make_row(cols, {k:v for (k,v) in BP_diff_last.items() if v <= 100}, 4))
            t.add_row(['bt100 (KRW)'] + util.make_row(cols, {k:bithumb_KRW_last[k]*100/v for (k,v) in BP_diff_last.items()}, 0, True))
            if(args.alarm):
                if(len({k:v for (k,v) in BP_diff_last.items() if v <= 97}) > 0):
                    pygame.mixer.music.play()
        if args.bfx and args.bt:
            t.add_row(['positive Bt-Bfx'] + util.make_row(cols, {k:v for (k,v) in BB_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Bt-Bfx'] + util.make_row(cols, {k:v for (k,v) in BB_diff_last.items() if v <= 100}, 4))
            if(args.alarm):
                if(len({k:v for (k,v) in BB_diff_last.items() if v <= 98 and polo_percent_changes[k] > 0}) > 0):
                    pygame.mixer.music.play()
        if args.btx and args.bt:
            t.add_row(['positive Bt-Btx'] + util.make_row(cols, {k:v for (k,v) in BBT_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Bt-Btx'] + util.make_row(cols, {k:v for (k,v) in BBT_diff_last.items() if v <= 100}, 4))
            if(args.alarm):
                if(len({k:v for (k,v) in BBT_diff_last.items() if v <= 98 and polo_percent_changes[k] > 0}) > 0):
                    pygame.mixer.music.play()
        if args.co:
            t.add_row(['coinone (BTC)'] + util.make_row(cols, {k:v for (k,v) in coinone_last.items()}, 6))
            t.add_row(['coinone (KRW)'] + util.make_row(cols, {k:v for (k,v) in coinone_KRW_last.items()}, 0, True))
        if args.co and args.polo:
            t.add_row(['positive Co-Po'] + util.make_row(cols, {k:v for (k,v) in CP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Co-Po'] + util.make_row(cols, {k:v for (k,v) in CP_diff_last.items() if v <= 100}, 4))
            t.add_row(['co100 (KRW)'] + util.make_row(cols, {k:coinone_KRW_last[k]*100/v for (k,v) in CP_diff_last.items()}, 0, True))
        if args.btx and args.co:
            t.add_row(['positive Co-Btx'] + util.make_row(cols, {k:v for (k,v) in CBT_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Co-Btx'] + util.make_row(cols, {k:v for (k,v) in CBT_diff_last.items() if v <= 100}, 4))
            t.add_row(['co100 (KRW)'] + util.make_row(cols, {k:coinone_KRW_last[k]*100/v for (k,v) in CBT_diff_last.items()}, 0, True))
            if(args.alarm):
                if(len({k:v for (k,v) in CBT_diff_last.items() if v <= 98 and polo_percent_changes[k] > 0}) > 0):
                    pygame.mixer.music.play()
        if args.binance and args.co:
            t.add_row(['positive Co-Bin'] + util.make_row(cols, {k:v for (k,v) in CBI_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Co-Bin'] + util.make_row(cols, {k:v for (k,v) in CBI_diff_last.items() if v <= 100}, 4))
            t.add_row(['co100 (KRW)'] + util.make_row(cols, {k:coinone_KRW_last[k]*100/v for (k,v) in CBI_diff_last.items()}, 0, True))
            if(args.alarm):
                if(len({k:v for (k,v) in CBI_diff_last.items() if v <= 98 and polo_percent_changes[k] > 0}) > 0):
                    pygame.mixer.music.play()
        if args.gate and args.co:
            t.add_row(['positive Co-Gate'] + util.make_row(cols, {k:v for (k,v) in CGA_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Co-Gate'] + util.make_row(cols, {k:v for (k,v) in CGA_diff_last.items() if v <= 100}, 4))
            t.add_row(['co100 (KRW)'] + util.make_row(cols, {k:coinone_KRW_last[k]*100/v for (k,v) in CGA_diff_last.items()}, 0, True))
        if args.liqui and args.co:
            t.add_row(['positive Co-Liqui'] + util.make_row(cols, {k:v for (k,v) in CL_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Co-Liqui'] + util.make_row(cols, {k:v for (k,v) in CL_diff_last.items() if v <= 100}, 4))
            t.add_row(['co100 (KRW)'] + util.make_row(cols, {k:coinone_KRW_last[k]*100/v for (k,v) in CL_diff_last.items()}, 0, True))
        if args.gopax:
            t.add_row(['gopax (BTC)'] + util.make_row(cols, {k:v for (k,v) in gopax_last.items()}, 6))
            t.add_row(['gopax (KRW)'] + util.make_row(cols, {k:v for (k,v) in gopax_KRW_last.items()}, 0, True))
        if args.btx and args.gopax:
            t.add_row(['positive Go-Btx'] + util.make_row(cols, {k:v for (k,v) in GBT_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Go-Btx'] + util.make_row(cols, {k:v for (k,v) in GBT_diff_last.items() if v <= 100}, 4))
            t.add_row(['go100 (KRW)'] + util.make_row(cols, {k:gopax_last[k]*100/v for (k,v) in GBT_diff_last.items()}, 0, True))
        if args.binance and args.gopax:
            t.add_row(['positive Go-Bin'] + util.make_row(cols, {k:v for (k,v) in GBI_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Go-Bin'] + util.make_row(cols, {k:v for (k,v) in GBI_diff_last.items() if v <= 100}, 4))
            t.add_row(['go100 (KRW)'] + util.make_row(cols, {k:gopax_last[k]*100/v for (k,v) in GBI_diff_last.items()}, 0, True))
        if args.ci: 
            t.add_row(['coinis (BTC)'] + util.make_row(cols, {k:v for (k,v) in coinis_last.items()}, 6))
            t.add_row(['coinis (KRW)'] + util.make_row(cols, {k:v for (k,v) in coinis_KRW_last.items()}, 0, True))
        if args.ci and args.polo:
            t.add_row(['positive Ci-Po'] + util.make_row(cols, {k:v for (k,v) in CIP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Ci-Po'] + util.make_row(cols, {k:v for (k,v) in CIP_diff_last.items() if v <= 100}, 4))    
        if args.cr:
            t.add_row(['coinrail (BTC)'] + util.make_row(cols, {k:v for (k,v) in coinrail_last.items()}, 6))
            t.add_row(['coinrail (KRW)'] + util.make_row(cols, {k:v for (k,v) in coinrail_KRW_last.items()}, 0, True))
        if args.cr and args.polo:
            t.add_row(['positive Cr-Po'] + util.make_row(cols, {k:v for (k,v) in CRP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Cr-Po'] + util.make_row(cols, {k:v for (k,v) in CRP_diff_last.items() if v <= 100}, 4))    
        if args.liqui:
            t.add_row(['liqui (BTC)'] + util.make_row(cols, {k:v for (k,v) in liqui_last.items()}, 6))
        if args.liqui and args.polo:
            t.add_row(['positive Li-Po'] + util.make_row(cols, {k:v for (k,v) in LP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Li-Po'] + util.make_row(cols, {k:v for (k,v) in LP_diff_last.items() if v <= 100}, 4))
        if args.hitbtc:
            t.add_row(['hitbtc (BTC)'] + util.make_row(cols, {k:v for (k,v) in hitbtc_last.items()}, 6))
        if args.hitbtc and args.polo:
            t.add_row(['positive HB-Po'] + util.make_row(cols, {k:v for (k,v) in HP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative HB-Po'] + util.make_row(cols, {k:v for (k,v) in HP_diff_last.items() if v <= 100}, 4))

        t.align = "l"
        
        util.clear()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(t)

    except Exception as e:
        #slack_bot.chat.post_message("#error", "failed with error code: {}".format(e))
        print("failed with error code: {}".format(e))

    s.enter(duration, 1, run_ticker, (sc,))

if __name__ == "__main__":    
    s.enter(duration, 1, run_ticker, (s,))
    s.run()