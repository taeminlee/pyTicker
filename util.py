import util, os,subprocess
from collections import OrderedDict
from babel.numbers import format_decimal

def get_diff_last(x, y):
    diff_last = OrderedDict()
    for currency in x.keys():
        if currency in y:
            diff_last[currency] = (x[currency] / y[currency]) * 100
    return diff_last

def get_normalized_price(prices, unit_price):
    NP = OrderedDict()
    for kv in prices.items():
        NP[kv[0]] = kv[1] / unit_price
    return NP

def get_diff_history(balance, last):
    diff_history = OrderedDict()
    for currency in balance.keys():
        if currency in last:
            diff_history[currency] = (last[currency] - balance[currency]['price']) * balance[currency]['amount']
    return diff_history

def orderby(d, reverseOpt=True):
    o = OrderedDict()
    for (k,v) in sorted(d.items(), key=lambda x: x[1], reverse=reverseOpt):
        o[k]=v
    return o.items()

def make_cell(currency, val, roundOpt=-1,currencyOpt=False):
    if (roundOpt > 0 and val >= 0.0001):
        val = round(val, roundOpt)
    if roundOpt == 0:
        val = int(val)
    if currencyOpt == True:
        val = format_decimal(val, locale="en_US")
    return val

def make_row(cols,vals,roundOpt=-1,currencyOpt=False):
    o = []
    for col in cols:
        if col in vals:
            o.append(make_cell(col, vals[col], roundOpt, currencyOpt))
        else:
            o.append("")
    return o

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def import_test(pack_string):
    try:
        if __import__(pack_string.lower()):
            print(pack_string + " loaded successfully")
            return True
    except Exception as e:
        print(pack_string + " failed with error code: {}".format(e))

def clear():
    if os.name in ('nt','dos'):
        os.system("cls")
    elif os.name in ('linux','osx','posix'):
        subprocess.call("clear")
    else:
        print ("\n"*120)