import numpy as np
import taft

rates = np.array( [
	44.3389,44.0902,44.1497,43.6124,44.3278,44.8264,45.0955,45.4245,45.8433,46.0826,45.8931,46.0328,45.6140,46.2820,46.2820,46.0028,46.0328,46.4116,46.2222,45.6439,46.2122,46.2521,45.7137,46.4515,45.7835,45.3548,44.0288,44.1783,44.2181,44.5672,43.4205,42.6628,43.1314
] )

rates = rates[::-1]
ratesLen = len(rates)

ind = np.zeros( shape=ratesLen, dtype='float' )
ind2 = np.zeros( shape=ratesLen, dtype='float' )
ret = None
for i in range( ratesLen-1, -1, -1 ):
	ret = taft.rsi( shift=i, rates=rates, prev=ret )
	if ret is not None:
		ind[i] = ret['rsi']
		ind2[i] = ret['rs']

for i in range( ratesLen-1,-1,-1 ):
	prefix = str(i+1) + ". rate=" + str(rates[i]) + ": " 
	if ind[i] == 0.0:
		print prefix + "0"
	else:
		print prefix + "rs=" + str(ind2[i]) + ", " + str(ind[i])
