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
parser.add_argument('-bfx', action="store_true", default=False, help="enable getting ticker from poloniex")
parser.add_argument('-bt', action="store_false", default=True, help="disable getting ticker from bithumb")
parser.add_argument('-co', action="store_false", default=True, help="disable getting ticker from coinone")
parser.add_argument('-ci', action="store_false", default=True, help="disable getting ticker from coinis")
parser.add_argument('-liqui', action='store_false', default=True, help='disable getting ticker from liqui.io')
parser.add_argument('-alarm', action='store_false', default=True, help='disable alarm')
args = parser.parse_args()

currencies = ["ETH", "DASH", "LTC", "ETC", "ZEC", "XRP", "BCH"]
cols = ["ETH","DASH","LTC","ETC","ZEC", "XRP","BCH", "BTC"]
duration = 1 #sec

s = sched.scheduler(time.time, time.sleep)

if args.alarm:
    pygame.mixer.init()
    pygame.mixer.music.load("hangout.mp3")

def run_ticker(sc): 
    try:
        if args.polo:
            polo_last, polo_USDT_last, polo_percent_changes, polo_json = exchange.get_polo_last(currencies)
        if args.bfx:
            bitfinex_last, bitfinex_USDT_last = exchange.get_bitfinex_last(currencies)
        if args.bt:
            bithumb_last, bithumb_KRW_last = exchange.get_bithumb_last(currencies)
        if args.co:
            coinone_last, coinone_KRW_last = exchange.get_coinone_last(currencies)
        if args.ci:
            coinis_last, coinis_KRW_last = exchange.get_coinis_last(currencies)
        if args.liqui:
            liqui_last = exchange.get_liqui_last(currencies)
        if args.polo and args.bt:
            BP_diff_last = util.get_diff_last(bithumb_last, polo_last)
        if args.bfx and args.bt:
            BB_diff_last = util.get_diff_last(bithumb_last, bitfinex_last)
        if args.polo and args.co:
            CP_diff_last = util.get_diff_last(coinone_last, polo_last)
        if args.polo and args.ci:
            CIP_diff_last = util.get_diff_last(coinis_last, polo_last)
        if args.polo and args.liqui:
            LP_diff_last = util.get_diff_last(liqui_last, polo_last)

        t = PrettyTable(["Index"] + cols)
        if args.polo:
            t.add_row(['polo (BTC)'] + util.make_row(cols, {k:v for (k,v) in polo_last.items()}, 6))
            t.add_row(['polo (USDT)'] + util.make_row(cols, {k:v for (k,v) in polo_USDT_last.items()}, 2, True))
            t.add_row(['polo (+)'] + util.make_row(cols, {k:v for(k,v) in polo_percent_changes.items() if v > 0}, 6, True))
            t.add_row(['polo (-)'] + util.make_row(cols, {k:v for(k,v) in polo_percent_changes.items() if v <= 0}, 6, True))
        if args.bfx:
            t.add_row(['bitfinex (BTC)'] + util.make_row(cols, {k:v for (k,v) in bitfinex_last.items()}, 6))
            t.add_row(['bitfinex (USDT)'] + util.make_row(cols, {k:v for (k,v) in bitfinex_USDT_last.items()}, 2, True))
        if args.bt:
            t.add_row(['bithumb (BTC)'] + util.make_row(cols, {k:v for (k,v) in bithumb_last.items()}, 6))
            t.add_row(['bithumb (KRW)'] + util.make_row(cols, {k:v for (k,v) in bithumb_KRW_last.items()}, 0, True))
        if args.polo and args.bt:
            t.add_row(['positive Bt-Po'] + util.make_row(cols, {k:v for (k,v) in BB_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Bt-Po'] + util.make_row(cols, {k:v for (k,v) in BB_diff_last.items() if v <= 100}, 4))
            if(args.alarm):
                if(len({k:v for (k,v) in BB_diff_last.items() if v <= 98}) > 0):
                    pygame.mixer.music.play()
        if args.bfx and args.bt:
            t.add_row(['positive Bt-Bfx'] + util.make_row(cols, {k:v for (k,v) in BP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Bt-Bfx'] + util.make_row(cols, {k:v for (k,v) in BP_diff_last.items() if v <= 100}, 4))
            if(args.alarm):
                if(len({k:v for (k,v) in BP_diff_last.items() if v <= 98 and polo_percent_changes[k] > 0}) > 0):
                    pygame.mixer.music.play()
        if args.polo and args.bt:
            t.add_row(['bt100 (KRW)'] + util.make_row(cols, {k:v*100/BP_diff_last[k] for (k,v) in util.removekey(bithumb_KRW_last, 'BTC').items()}, 0, True))
        if args.co:
            t.add_row(['coinone (BTC)'] + util.make_row(cols, {k:v for (k,v) in coinone_last.items()}, 6))
            t.add_row(['coinone (KRW)'] + util.make_row(cols, {k:v for (k,v) in coinone_KRW_last.items()}, 0, True))
            if(args.alarm):
                if(len({k:v for (k,v) in CP_diff_last.items() if v <= 98 and polo_percent_changes[k] > 0}) > 0):
                    pygame.mixer.music.play()
        if args.co and args.polo:
            t.add_row(['co100 (KRW)'] + util.make_row(cols, {k:v*100/CP_diff_last[k] for (k,v) in util.removekey(coinone_KRW_last, 'BTC').items()}, 0, True))
        if args.co and args.polo:
            t.add_row(['positive Co-Po'] + util.make_row(cols, {k:v for (k,v) in CP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Co-Po'] + util.make_row(cols, {k:v for (k,v) in CP_diff_last.items() if v <= 100}, 4))
        if args.ci: 
            t.add_row(['coinis (BTC)'] + util.make_row(cols, {k:v for (k,v) in coinis_last.items()}, 6))
            t.add_row(['coinis (KRW)'] + util.make_row(cols, {k:v for (k,v) in coinis_KRW_last.items()}, 0, True))
        if args.ci and args.polo:
            t.add_row(['positive Ci-Po'] + util.make_row(cols, {k:v for (k,v) in CIP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Ci-Po'] + util.make_row(cols, {k:v for (k,v) in CIP_diff_last.items() if v <= 100}, 4))    
        if args.liqui:
            t.add_row(['liqui (BTC)'] + util.make_row(cols, {k:v for (k,v) in liqui_last.items()}, 6))
        if args.liqui and args.polo:
            t.add_row(['positive Li-Po'] + util.make_row(cols, {k:v for (k,v) in LP_diff_last.items() if v > 100}, 4))
            t.add_row(['negative Li-Po'] + util.make_row(cols, {k:v for (k,v) in LP_diff_last.items() if v <= 100}, 4))

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