# import python libs
import sys
import re
import argparse
import time
import json
import io
import asyncio
from datetime import datetime
# import additional libs
from prettytable import PrettyTable
import pygame
# import pyTicker libs
import exchange
import util
import data
from slacker import Slacker

parser = argparse.ArgumentParser(description="cryptocurrency ticker comparer suite")
parser.add_argument('input', nargs='?', help="disable getting ticker from poloniex")
args = parser.parse_args()

args.input = 'upbit2.json'

token = 'xoxb-289205011008-vbRidHwCaVXy17szQpuq1UG7'
slack = Slacker(token)

def load_config(file):
    default = {
        'refresh':1,
        'slack_alarm':80,
    }
    with io.open(file, 'r') as fp:
        j = json.load(fp)
        default.update(j)
        return default

def load_exchange(name):
    return {'coinone':exchange.Coinone(),
            'binance':exchange.Binance(),
            'gate.io':exchange.GateIO(),
            'upbit':exchange.Upbit(),
            'cpdax':exchange.Cpdax(),
            'kucoin':exchange.Kucoin(),
            'gopax':exchange.Gopax(),
            'coinrail':exchange.Coinrail(),
            'coinnest':exchange.Coinnest()}[name]

def parse_config(cfg):
    EX = dict(map(lambda name:(name,load_exchange(name)),cfg['exchanges']))
    C = cfg['currencies']
    nu = cfg['norm_unit']
    TU = cfg['target_units']
    SU = cfg['show_units']
    RP = list(map(lambda pair:(EX[pair[0]], EX[pair[1]]), cfg['RNPR_pairs']))
    SA = cfg['slack_alarm']
    return EX, C, nu, TU, SU, RP, SA

def async_run(EX, C):
    loop = asyncio.get_event_loop()
    tasks = list(map(lambda ex:asyncio.ensure_future(ex[1].async_run(C)), list(EX.items())))
    loop.run_until_complete(asyncio.wait(tasks))

def run(EX, C):
    for kv in EX.items():
        kv[1].run(C)

def make_header(C):
    return ["Index"] + C

def get_type_u(u):
    return {"KRW":data.KRWLast,"BTC":data.BTCLast,"ETH":data.ETHLast,"USDT":data.USDTLast}[u]

def get_u_last(ex,u):
    if u == "KRW":
        return ex.KRW_last
    elif u == "BTC":
        return ex.BTC_last
    elif u == "ETH":
        return ex.ETH_last
    elif u == "USDT":
        return ex.USDT_last

def make_exchange_body(name,ex,C,SU,TU,nu):
    rows = []
    U = ["KRW","BTC","ETH","USDT"]
    for u in U:
        if u in SU:
            currencyOpt = u == "KRW" or u == "USDT"
            if(issubclass(type(ex), get_type_u(u))):
                rows.append(["%s (%s)"%(name,u)] + util.make_row(C,get_u_last(ex,u), currencyOpt=currencyOpt))
            if(u != nu and issubclass(type(ex), get_type_u(u))):
                currencyOpt = nu == "KRW" or nu == "USDT"
                if u in TU:
                    NP = make_NP(ex=ex, tu=u, nu=nu)
                    rows.append(["%s (%s->%s)"%(name, u, nu)] + util.make_row(C,NP,roundOpt=8,currencyOpt=currencyOpt))
    return rows

def make_NP(ex, tu, nu):
    if issubclass(type(ex), get_type_u(tu)):
        u_last = get_u_last(ex,tu)
        nu_last = 1
        if(tu != nu):
            nu_last = u_last[nu]
        return util.get_normalized_price(u_last,nu_last)
    else:
        return None

def make_NRPR_body(EX, RP, C, TU, nu, SA): # EX:Exchange, RP : RNPR pairs, C : Currencies, TU : Target Unit, nu : norm unit, SA : slack alarm
    rows = []
    for tu in TU:
        for rp in RP:
            if(rp[0] == rp[1] and tu == nu):
                continue
            NP_0 = make_NP(ex=rp[0],tu=tu,nu=nu)
            NP_1 = make_NP(ex=rp[1],tu=nu,nu=nu)
            if NP_0 is None or NP_1 is None:
                continue
            elif issubclass(type(rp[0]), get_type_u(tu)) == False:
                continue
            diff = util.get_diff_last(NP_0, NP_1)
            if(len({k:v for (k,v) in diff.items() if v < SA}) > 0):
                for kv in {k:v for (k,v) in diff.items() if v < SA}.items():
                    slack.chat.post_message('#pyticker2', '%s/%s - %s : %s' % (list(EX.items())[0][0], list(EX.items())[1][0], kv[0], kv[1]))
            rows.append(["%s(%s)/%s(%s) (+)"%(rp[0].symbol, tu, rp[1].symbol, nu)] + util.make_row(C, {k:v for (k,v) in diff.items() if v > 100}, 4))
            rows.append(["%s(%s)/%s(%s) (-)"%(rp[0].symbol, tu, rp[1].symbol, nu)] + util.make_row(C, {k:v for (k,v) in diff.items() if v <= 100}, 4))
    return rows

def print_table(EX,C,SU,TU,nu,RP, SA):
    t = PrettyTable(make_header(C))
    for kv in EX.items():
        for row in make_exchange_body(name=kv[0],ex=kv[1],C=C,SU=SU,nu=nu,TU=TU):
            t.add_row(row)
    for row in make_NRPR_body(EX=EX,RP=RP,C=C,TU=TU,nu=nu, SA=SA):
        t.add_row(row)        
    t.align = "l"
    util.clear()
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(t)

if __name__ == "__main__": 
    if(args.input == None):
        print("Please provide config json file.\n\re.g.) python pyTicker2.py default.json")
    else:
        cfg = load_config(args.input)
        EX, C, nu, TU, SU, RP, SA = parse_config(cfg)

        while(True):
            try:
                #async_run(EX, C)
                run(EX,C)
                print_table(EX=EX,C=C,SU=SU,TU=TU,nu=nu,RP=RP, SA = SA)
            except Exception as e:
                print("failed with error code: {}".format(e))
            time.sleep(cfg['refresh'])
            