from limits import maxPosition
from warnings import warn
global maxPosition


class Instrument:
    def __init__(self, ticker):
        self._ticker = ticker
        self._timeFrames = []
        self._position = 0
        
    @property
    def ticker(self):
        return self._ticker
        
    @ticker.setter
    def ticker(self, value):
        raise RuntimeError("Ticker cannot be changed!")
        
    @ticker.deleter
    def ticker(self):
        raise RuntimeError("Ticker cannot be deleted!")
        
    @property
    def timeFrames(self):
        return self._timeFrames
        
    @timeFrames.setter
    def timeFrames(self, value):
        raise RuntimeError("Use addTimeFrame instead!")
        
    @timeFrames.deleter
    def timeFrames(self):
        self._timeFrames = []
        
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        if value > maxPosition or value < -maxPosition:
            raise ValueError("You are trying to acquire too many assets")
        else:
            self._position = value
            
    @position.deleter
    def position(self):
        self._position = 0
        
    def __eq__(self, value):
        if isinstance(value, str):
            if self._ticker == value:
                return True
            else:
                return False
        else:
            warn("Comparing different types!")
            return None
        
    def addTimeFrame(self, *timeFrames):
        for timeFrame in timeFrames:
            if isinstance(timeFrame, int):
                self._timeFrames.append(timeFrame)
            else:
                raise TypeError("Time frame must be int!")
        self._timeFrames.sort()
    
    def deleteTimeFrame(self, *timeFrames):
        for timeFrame in timeFrames:
            if isinstance(timeFrame, int):
                if timeFrame in self._timeFrames:
                    self._timeFrames.remove(timeFrame)
                else:
                    raise ValueError("There is no such time frame!")
            else:
                raise TypeError("Time frame must be int!")
        
    def printInstrument(self):
        print("The ticker is {}".format(self._ticker))
        for ind, timeFrame in enumerate(self._timeFrames):
            print("TimeFrame # {} is {}".format(ind, timeFrame))
        print("Number of acquired lots is {}".format(self._position))
            
    def __del__(self):
        self._ticker = ''
        self._timeFrames = []