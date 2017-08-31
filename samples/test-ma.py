
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import taft

rates=np.array([
	22.27340000,22.19400000,22.08470000,22.17410000,22.18400000,22.13440000,22.23370000,22.43230000,22.24360000,22.29330000,22.15420000,22.39260000,22.38160000,22.61090000,23.35580000,24.05190000,23.75300000,23.83240000,23.95160000,23.63380000,23.82250000,23.87220000,23.65370000,23.18700000,23.09760000,23.32600000,22.68050000,23.09760000,22.40250000,22.17250000
])

rates = rates[::-1]

ratesLen = len(rates)

sma = []
ema = []
for i in range( ratesLen ):
	sma.append( 0 )
	ema.append( 0 )

prev = None
for i in range( ratesLen-1, -1, -1 ):
	sma[i] = taft.sma( shift=i, period=10, rates=rates )
	ema[i] = taft.ema( shift=i, period=10, rates=rates, prev=prev )
	prev = ema[i]

for i in range( ratesLen-1,-1,-1 ):
	prefix = str(i) + ": " 
	print prefix + "close=" + str(rates[i]) + ", SMA=" + str(sma[i])  + ", EMA=" + str(ema[i])
