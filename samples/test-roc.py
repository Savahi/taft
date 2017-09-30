import numpy as np
import taft

cl = np.array([
	11045.2700, 11167.3200, 11008.6100, 11151.8300, 10926.7700, 10868.1200, 10520.3200, 
	10380.4300, 10785.1400, 10748.2600, 10896.9100, 10782.9500, 10620.1600, 10625.8300, 
	10510.9500, 10444.3700, 10068.0100, 10193.3900, 10066.5700, 10043.7500
])

cl = cl[::-1]
ratesLen = len(cl)

for i in range( ratesLen-1, -1, -1 ):
	roc = taft.roc( shift=i, rates=cl )
	prefix = str(i+1) + ". rate=" + str(cl[i]) + ": " 
	if roc is None:
		print prefix + "N/A"
	else:
		print prefix + "roc=" + str(roc)
