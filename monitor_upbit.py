# import python libs
import json
import time
from datetime import datetime
# import additional libs
from prettytable import PrettyTable
import pygame
from slacker import Slacker
# import pyTicker libs
import exchange
import util

print("init upbit monitor.. It takes several seconds..")

currencies = ["BTC", "BCC", "EMC2", "QTUM", "BTG", "ADA", "SNT", "REP", "ETC", "XLM", "ARK", "XMR", "KMD", "ETH", "XRP", "XEM", "STORJ", "NEO", "GRS", "DASH", "LTC", "STRAT", "SBD", "POWR", "TIX", "MER", "ARDR", "OMG", "ZEC", "WAVES", "LSK", "VTC", "PIVX", "MTL", "STEEM"]
duration = 1 #sec

pygame.mixer.init()
pygame.mixer.music.load("hangout.mp3")

token = 'xoxb-289205011008-GHBD95zHNsrXhxzV0JiCp39F'
slack = Slacker(token)

u = exchange.Upbit()

def run_ticker(): 
    while True:
        try:
            u.run(currencies)

            with open('upbit.json', 'w') as out:
                json.dump({'KRW_last' : u.KRW_last, 'BTC_last' : u.BTC_last, 'diff' : u.diff}, out)
            
            t = PrettyTable(["Index"] + currencies)
            t = PrettyTable(["currency", "KRW","BTC","positive","negative"])
            for (k,v) in u.KRW_last.items():
                r = [k, util.make_cell(k,u.KRW_last[k], 0)]
                if k in u.BTC_last:
                    r.append(util.make_cell(k,u.BTC_last[k], 12, False))
                else:
                    r.append("")
                if k in u.diff:
                    for threshold in range(102,111):
                        if u.diff[k] > threshold:
                            slack.chat.post_message('#+%s' % threshold, '%s %s %s %s' % (k, u.KRW_last[k], u.BTC_last[k], u.diff[k]))    
                    for threshold in range(90,99):
                        if u.diff[k] < threshold:
                            slack.chat.post_message('#-%s' % threshold, '%s %s %s %s' % (k, u.KRW_last[k], u.BTC_last[k], u.diff[k]))    
                    if u.diff[k] > 100:
                        r = r + [u.diff[k],""]
                    else:
                        r = r + ["",u.diff[k]]
                r = r + [""] * (5-len(r))
                t.add_row(r)
                
            if(len({k:v for (k,v) in u.diff.items() if v <= 97}) > 0):
                pygame.mixer.music.play()
            
            t.align = "l"
            
            util.clear()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(t)

        except Exception as e:
            #slack_bot.chat.post_message("#error", "failed with error code: {}".format(e))
            print("failed with error code: {}".format(e))

        time.sleep(1)

if __name__ == "__main__":
    run_ticker()