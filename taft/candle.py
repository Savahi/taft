"""
This module contains realization of rates class.
Rates class is used for contain and handle bars.
"""

class candle(dict):
    def __init__(self, rawData = None):
        self._instrument
        self._timeFrame
        self._openPrice
        self._highPrice
        self._lowPrice
        self._closePrice
        self._volume
        self._dtm
        
    @property
    def ratesDict(self):
        return self._ratesDict
        
    @ratesDict.setter
    def ratesDict(self, newRates):
        self._ratesDict = newRates
        
    @ratesDict.deleter
    def ratesDict(self):
        del self._ratesDict
        
    def __getitem__(self, k):
        openPrice = self._ratesDict['op'][k]
        highPrice = self._ratesDict['hi'][k]
        lowPrice = self._ratesDict['lo'][k]
        closePrice = self._ratesDict['cl'][k]
        vol = self._ratesDict['vol'][k]
        dtm = self._ratesDict['dtm'][k]
        if isinstance(k, slice):
            start = k.start
            stop = k.stop
            fullLength = self._ratesDict['length']
            if stop == 0 and start != 0:
                raise IndexError
            if stop > fullLength - 1 or stop < -fullLength + 1:
                raise IndexError
            if start > fullLength -1 or start < -fullLength + 1:
                raise IndexError
            start = start % fullLength
            stop = stop % fullLength
            if start > stop:
                raise IndexError
            length = stop - start + 1
        elif isinstance(k, int):
            length = 1
        else:
            raise TypeError 
        candle = {'op': openPrice, 'hi': highPrice, 'lo': lowPrice,
                    'cl': closePrice, 'vol': vol, 'dtm': dtm,
                    'length': length}
        return candle
        
    def __setitem__(self, k, value):
        if not isinstance(value, rates):
            raise TypeError
        fullLength = self._ratesDict['length']
        if k > fullLength - 1 or k < 0:
            raise IndexError
        self._ratesDict['op'][k] = value['op']
        self._ratesDict['hi'][k] = value['hi']
        self._ratesDict['lo'][k] = value['lo']
        self._ratesDict['cl'][k] = value['cl']
        self._ratesDict['vol'][k] = value['vol']
        self._ratesDict['dtm'][k] = value['dtm']
        return None