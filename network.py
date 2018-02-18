import requests as req
import json
import asyncio
from aiohttp import ClientSession

class JsonLoaderRQ:
    json_loader_msg = ""
    def debug(self):
        print("json_loader failed : %s" % self.json_loader_msg)
    def load_single_json(self, url):
        #print(url)
        res = req.get(url)
        if res.ok:
            #print(res.text)
            try:
                return json.loads(res.text)
            except:
                self.json_loader_msg = "json loads failed : %s" % url
                return False
        else:
            self.json_loader_msg = "request failed : %s" % url
            return False
    def load_multiple_json(self, url_dict):
        # url_dict = { currency : url }
        try :
            list(map(lambda kv : (kv[0], self.load_single_json(kv[1])), list(url_dict.items())))
        except :
            return False

class JsonLoaderAsync:
    json_loader_msg = ""
    def debug(self):
        print("json_loader failed : %s" % self.json_loader_msg)
    async def load_single_json(self, url, currency = None, option=None):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                try:
                    json = await response.json()
                    #print(json)
                    if option == 'CRIX':
                        if(len(json) > 0):
                            json[0]['currency'] = currency
                            return json[0]
                        else:
                            return json
                    if(currency != None):
                        json['currency'] = currency
                    return json
                except:
                    self.json_loader_msg = "json loads failed : %s" % url
                    print(self.json_loader_msg)
    def load_multiple_json(self, url_dict, option=None):
        # url_dict = { currency : url }
        try :
            loop = asyncio.get_event_loop()
            tasks = list(map(lambda kv:asyncio.ensure_future(self.load_single_json(currency = kv[0], url = kv[1], option=option)), list(url_dict.items())))
            loop.run_until_complete(asyncio.wait(tasks))
            return list(map(lambda t: t.result(), tasks))
        except Exception as e:
            return False