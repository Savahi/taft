import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import taft

rates = np.array([
	86.16,89.09,88.78,90.32,89.07,91.15,89.44,89.18,86.93,87.68,86.96,89.43,89.32,88.72,87.45,87.26,89.50,87.90,89.13,90.70,92.90,92.98,91.80,92.66,92.68,92.30,92.77,92.54,92.95,93.20,91.07,89.83,89.74,90.40,90.74,88.02,88.09,88.84,90.78,90.54,91.39,90.65
])

rates = rates[::-1]
ratesLen = len(rates)

bbands = []
for i in range( ratesLen ):
	bbands.append( taft.bollinger( shift=i, rates=rates ) )

for i in range( ratesLen-1,-1,-1 ):
	prefix = str(i) + ": " 
	if bbands[i] == None:
		print prefix + "N/A"
	else:
		print prefix + "rate=" + str(rates[i]) + ", middle=" + str(bbands[i]['middle']) + ", std=" + str(bbands[i]['std']) + ", upper=" + str(bbands[i]['upper'])  + ", lower=" + str(bbands[i]['lower'])

