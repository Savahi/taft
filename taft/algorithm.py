from instrument import Instrument
import candle
import data

class Algorithm:
    """
    This class supposed to be base class (propably the only one) for an
    user algorithm.
    Conceptually, it should contain all the neccessary methods for
    code and testing an algorithm.
    
    Attributes:
    _instruments    list of instruments used by trader
    """
    def __init__(self):
        self._instruments = []
        self._takeProfit = 0
        self._stopLoss = 0
        
    @property
    def instruments(self):
        return self._instruments
        
    @instruments.setter
    def instruments(self, value):
        raise RuntimeError("Use addInstrument instead!")
        
    @instruments.deleter
    def instruments(self):
        raise RuntimeError("Use deleteInstrument insted!")
        
    @property
    def takeProfit(self):
        return self._takeProfit
        
    @takeProfit.setter
    def takeProfit(self, value):
        raise RuntimeError("Use setSLPTP insted!")
        
    @takeProfit.deleter
    def takeProfit(self):
        raise NotImplemetedError("Use ??? function instead!")
        
    @property
    def stopLoss(self):
        return self._stopLoss
        
    @stopLoss.setter
    def stopLoss(self, value):
        raise RuntimeError("Use setSLTP insted")
        
    @stopLoss.deleter
    def stopLoss(self):
        raise NotImplemetedError("Use ??? function instead!")

    def addInstrument(self, newInstrument):
        if isinstance(newInstrument, Instrument):
            newInstr = newInstrument
        elif isinstance(newInstrument, str):
            newInstr = Instrument(newInstrument)
        else:
            raise TypeError("Check argument! It's not of supported datatype!")
        self._instruments.append(newInstr)
        
    def deleteInstrument(self, delInstrument):
        _, found = self._findInstrument(delInstrument)
        if found:
            self._instruments.remove(instr)
        else:
            raise NameError("Wrong ticker!")
            
    def addTimeFrame(self, ticker, *timeFrame):
        ind, found = self._findInstrument(ticker)
        if found:
            self._instruments[ind].addTimeFrame(*timeFrame)
        else:
            raise NameError("Wrong ticker!")
            
    def deleteTimeFrame(self, ticker, *timeFrame):
        ind, found = self._findInstrument(ticker)
        if found:
            self._instruments[ind].deleteTimeFrame(*timeFrame)
        else:
            raise NameError("Wrong ticker!")
            
    def buy(self, ticker, lots):
        if lots <= 0:
            raise ValueError("You can't acquire nonnegative number of assets!")
        ind, found = self._findInstrument(ticker)
        if found:
            if self._instruments[ind].position >= 0:
                self._instruments[ind].position += lots
            else:
                self._instruments[ind].position = lots
        else:
            raise NameError("Wrong ticker!")
            
    def sell(self, ticker, lots):
        if lots <= 0:
            raise ValueError("You can't acquire nonnegative number of assets!")
        ind, found = self._findInstrument(ticker)
        if found:
            if self._instruments[ind].position <= 0:
                self._instruments[ind].position -= lots
            else:
                self._instruments[ind].position = -lots
        else:
            raise NameError("Wrong ticker!")
            
    def close(self, ticker, lots):
        if lots <= 0:
            raise ValueError("You can't acquire nonnegative number of assets!")
        ind, found = self._findInstrument(ticker)
        if found:
            currPosition = self._instruments[ind].position
            if currPosition == 0:
                raise ValueError("You are trying to close an empty position!")
            else:
                if currPosition > 0:
                    if currPosition >= lots:
                        self._instruments[ind].position -= lots
                    else:
                        self._instruments[ind].position = 0
                        Warning("You tried to close too much. Position is closed.")
                else:
                    if -currPosition >= lots:
                        self._instruments[ind].position += lots
                    else:
                        self._instruments[ind].position = 0
                        Warning("You tried to close too much. Position is closed.")
        else:
            raise NameError("Wrong ticker!")
            
    def closeAllByInstrument(self, ticker):
        ind, found = self._findInstrument(ticker)
        if found:
            self._instruments[ind].position = 0
        else:
            raise NameError("Wrong ticker!")
            
    def closeAll(self):
        for instr in self._instruments:
            instr.position = 0
            
    def setSLTP(self, stopLoss = 0, takeProfit = 0):
        """
        Setting stopLoss or takeProfit to zero means no stopLoss or takeProfit resp.
        """
        if stopLoss < 0:
            raise ValueError("Stop loss cannot be negative!")
        if takeProfit < 0:
            raise ValueError("Take profit cannot be negative!")
        self._stopLoss = stopLoss
        self._takeProfit = takeProfit
        
    def run(self, onBarFunction):
        rtsMinutes = data.loadFinam("RTS")
        print(rtsMinutes)
        for instr in self._instruments:
            print(instr.ticker)
            for timeFrame in instr.timeFrames:
                print(timeFrame)
        onBarFunction()
        #1. Load needed data
        #2. Prepare historic data (prices array) for each instrument
        #2. Iterate onBar(candle) through test period
        #3. Calculate performance
            
    def printAlgorithm(self):
        print("===========================================================")
        for instr in self._instruments:
            instr.printInstrument()
            print('-----------------------------------------------------------')
            print('\n Stop Loss = {:d} and Take Profit = {:d}'.format(
                self._stopLoss, self._takeProfit
            ))
        print("===========================================================")
        
    def _findInstrument(self, ticker):
        found = False
        if isinstance(ticker, Instrument):
            for ind, instr in enumerate(self._instruments):
                instrTicker = instr.ticker
                if ticker == instrTicker:
                    found = True
                    break
                else:
                    continue
        elif isinstance(ticker, str):
            for ind, instr in enumerate(self._instruments):
                if ticker == instr.ticker:
                    found = True
                    break
                else:
                    continue
        else:
            raise TypeError("Check the argument! It's not of supported datatype!")
        return ind, found