import numpy as np

values = []
with open("stddev.txt") as f:
	for line in f:
		splitted = line.strip().split(',')
		values.append( splitted[4] )

values = np.array( values, dtype=float )

print "VALUES READ: %s" % ( str(values[-10:]) )

print "Last 10: mean = %f, std = %f" % ( np.mean( values[-10:] ), np.std( values[-10:] ) * (10**0.5/9**0.5) ) 

print "VALUES READ: %s" % ( str(values[-11:-1]) )

print "Last 10, not counting the latest: mean = %f, std = %f" % ( np.mean( values[-11:-1] ), np.std( values[-11:-1] ) * (10**0.5/9**0.5) ) 

print "VALUES READ: %s" % ( str(values[-12:-2]) )

print "Last 10, not counting the 2 latest: mean = %f, std = %f" % ( np.mean( values[-12:-2] ), np.std( values[-12:-2] ) * (10**0.5/9**0.5) ) 


