import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import taft

rates = np.array( [
	44.34,44.09,44.15,43.61,44.33,44.83,45.10,45.42,45.84,46.08,45.89,46.03,45.61,46.28,46.28,46.00,46.03,46.41,46.22,45.64,46.21,46.25,45.71,46.45,45.78,45.35,44.03,44.18,44.22,44.57,43.42,42.66,43.13
] )

rates = rates[::-1]
ratesLen = len(rates)

ind = np.zeros( shape=ratesLen, dtype='float' )
ind2 = np.zeros( shape=ratesLen, dtype='float' )
averageGainPrev = None
averageLossPrev = None 
for i in range( ratesLen-1, -1, -1 ):
	ret = taft.rsi( shift=i, rates=rates, averageGainPrev=averageGainPrev, averageLossPrev=averageLossPrev )
	if ret != None:
		ind[i] = ret['rsi']
		ind2[i] = ret['rs']
		averageGainPrev = ret['averageGain']
		averageLossPrev = ret['averageLoss']

for i in range( ratesLen ):
	prefix = str(i+1) + ". rate=" + str(rates[i]) + ": " 
	if ind[i] == 0.0:
		print prefix + "0"
	else:
		print prefix + "rs=" + str(ind2[i]) + ", " + str(ind[i])
