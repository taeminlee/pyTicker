from collections import OrderedDict

class USDTLast:
    @property
    def USDT_last(self):
        if('_USDT_last' not in dir(self)):
            self._USDT_last = OrderedDict()
        return self._USDT_last

    @USDT_last.setter
    def USDT_last(self, value):
        self._USDT_last = value

class BTCLast:
    @property
    def BTC_last(self):
        if('_BTC_last' not in dir(self)):
            self._BTC_last = OrderedDict()
        return self._BTC_last

    @BTC_last.setter
    def BTC_last(self, value):
        self._BTC_last = value

class KRWLast:
    @property
    def KRW_last(self):
        if('_KRW_last' not in dir(self)):
            self._KRW_last = OrderedDict()
        return self._KRW_last

    @KRW_last.setter
    def KRW_last(self, value):
        self._KRW_last = value

class ETHLast:
    @property
    def ETH_last(self):
        if('_ETH_last' not in dir(self)):
            self._ETH_last = OrderedDict()
        return self._ETH_last

    @ETH_last.setter
    def ETH_last(self, value):
        self._ETH_last = value

class BNBLast:
    @property
    def BNB_last(self):
        if('_BNB_last' not in dir(self)):
            self._BNB_last = OrderedDict()
        return self._BNB_last

    @BNB_last.setter
    def BNB_last(self, value):
        self._BNB_last = value

class PercentChanges:
    @property
    def percent_changes(self):
        if('_percent_changes' not in dir(self)):
            self._percent_changes = OrderedDict()
        return self._percent_changes

    @percent_changes.setter
    def percent_changes(self, value):
        self._percent_changes = value