import numpy as np

values = []
with open("tsf.txt") as f:
	for line in f:
		splitted = line.strip().split(',')
		values.append( splitted[4] )

y = np.array( values, dtype=float )
x = np.arange( 1, 11, 1 )

print "x=" + str(x)

from scipy.stats import linregress

result = linregress( x, y[-10:] )
print "Variative: %s\n" % ( str(result) )

result = linregress(x, y[-11:-1])
print "Calculate: %s\n" % ( str(result) )

result = linregress(x, y[-12:-2])
print "Precalculate: %s\n" % ( str(result) )

'''
print "VALUES READ: %s" % ( str(values[-10:]) )

print "Last 10: mean = %f, std = %f" % ( np.mean( values[-10:] ), np.std( values[-10:] ) * (10**0.5/9**0.5) ) 

print "VALUES READ: %s" % ( str(values[-11:-1]) )

print "Last 10, not counting the latest: mean = %f, std = %f" % ( np.mean( values[-11:-1] ), np.std( values[-11:-1] ) * (10**0.5/9**0.5) ) 

print "VALUES READ: %s" % ( str(values[-12:-2]) )

print "Last 10, not counting the 2 latest: mean = %f, std = %f" % ( np.mean( values[-12:-2] ), np.std( values[-12:-2] ) * (10**0.5/9**0.5) ) 
'''
