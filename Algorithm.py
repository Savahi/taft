class Algorithm:
    """
    This class supposed to be base class (propably the only one) for an
    user algorithm.
    Conceptually, it should contain all the neccessary methods for
    code and testing an algorithm.
    
    Attributes:
    _instruments    list of instruments used by trader
    _timeFrames     dictionary of lists of timeFrames used by trader.
                    Key is instrument.
    """
    def __init__(self):
        self._instruments = []
        self._timeFrames = {}
        
    @property
    def instruments(self):
        return self._instruments
        
    @instruments.setter
    def instruments(self, value):
        raise NotImplementedError("Use addInstrument instead!")
        
    @instruments.deleter
    def instruments(self):
        raise NotImplementedError("Use deleteInstrument insted!")
        
    @property
    def timeFrames(self):
        return self._timeFrames
        
    @timeFrames.setter
    def timeFrames(self, value):
        raise NotImplementedError("Use addTimeFrame instead!")
        
    @timeFrames.deleter
    def timeFrames(self):
        raise NotImplementedError("Use deleteTimeFrame insted!")
        
    def addInstrument(self, instrument):
        self._instruments.append(instrument)
        self._timeFrames[instrument] = []
        
    def deleteInstrument(self, instrument):
        if instrument in self._instruments:
            self._instruments.remove(instrument)
        else:
            raise NameError
            
    def addTimeFrame(self, instrument, timeFrame):
        if instrument in self._instruments:
            self._timeFrames[instrument].append(timeFrame)
        else:
            raise NameError
        
    def deleteTimeFrame(self, instrument, timeFrame):
        if instrument in self._instruments:
            if timeFrame in self._timeFrames[instruments]:
                self._timeFrames[instruments].remove(timeFrame)
            else:
                raise ValueError
        else:
            raise NameError