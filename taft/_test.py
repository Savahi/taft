from algorithm import Algorithm
#from instrument import Instrument

alg = Algorithm()
ticker1 = "RTS"
#ticker2 = "Si"
alg.addInstrument(ticker1)
#alg.addInstrument(ticker2)
alg.addTimeFrame(ticker1, 5, 10)
#alg.addInstrument(ticker2)
#alg.addTimeFrame(ticker2, 10, 20)

def onBar(startDate = None, endDate = None):
    pass

alg.run(onBar)