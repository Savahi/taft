# -*- coding: utf-8 -*- 

import numpy as np
import matplotlib.pyplot as plt
import taft # Importing 'taft' library

# An array to serve as 'high' rates
ratesHigh = np.array([
	1550,1560,1570,1550,1520,1530,1550,1570,1540,1560,1540,1550,1560,1570,1550,1520,1530,1550,1570,1540,1560,1540,1550,1570
])

# An array to serve as 'low' rates
ratesLow = np.array([
	1500,1520,1500,1500,1460,1480,1510,1510,1500,1510,1480,1500,1520,1500,1500,1460,1480,1510,1510,1500,1510,1480,1510,1510
])

# An array to serve as 'close' rates
ratesClose = np.array([
	1530,1540,1530,1510,1490,1500,1540,1560,1530,1520,1490,1530,1540,1530,1510,1490,1500,1540,1560,1530,1520,1490,1540,1560
])
ratesNumber = len(ratesClose)

# Time strings
ratesTimeStr = [
	'2015-02-09 10:00:00','2015-02-06 10:00:00','2015-02-05 10:00:00','2015-02-04 10:00:00','2015-02-03 10:00:00','2015-02-02 10:00:00',
	'2015-01-30 10:00:00','2015-01-29 10:00:00','2015-01-28 10:00:00','2015-01-27 10:00:00','2015-01-26 10:00:00','2015-01-23 10:00:00',
	'2015-01-22 10:00:00','2015-01-21 10:00:00','2015-01-20 10:00:00','2015-01-19 10:00:00','2015-01-18 10:00:00','2015-01-16 10:00:00',
	'2015-01-15 10:00:00','2015-01-14 10:00:00','2015-01-13 10:00:00','2015-01-12 10:00:00','2015-01-09 10:00:00','2015-01-08 10:00:00'
]

# Converting time strings to datetime objects (it is necessary for data visualization)
import datetime
ratesTime = [ datetime.datetime.strptime(timeStr, "%Y-%m-%d %H:%M:%S") for timeStr in ratesTimeStr ]

xOpen = [] # moments of time when trades are opened = ratesTime[i] 
xClose = [] # moments of time when trades are closed = ratesTime[i]

yOpen = [] # Rate values of opening trades 
yClose = [] # Rate values of closing rades

xProfit=[] # moments of time when profit is changed
yProfit=[] # profit change

# Cumulative (overall) profit 
profit = 0

xProfit.append(ratesTime[ratesNumber-1]) # In the beginning the profit is 0
yProfit.append(0) 
tp = 35 # Choosing the take profit value 
sl = 35 # Choosing the stop loss value
i = ratesNumber-1
while i >= 0:

	if( i % 2 == 0 ):	# Very simple 'strategy': opening trade if 'i' is not even.
		i = i-1			# If not - go to the beginning of the cycle
		continue		# 
	
	# Simulating trade
	# side: '1' for simulationg LONG trade and '-1' for SHORT trade
	# price: the rate value the trade is opened at   
	ret = taft.simulateTrade( shift=i-1, hi=ratesHigh, lo=ratesLow, tp=tp, sl=sl, side=1, price=ratesClose[i] )
	if ret == None: # Returns 'None' if an error occurs  
		break
	if ret['closedAt'] == -1: # ret['closedAt'] receives '-1' when the latest rate is reached  
		break

	xOpen.append( ratesTime[i] ) # time of opening the trade

	closedAt = ret['closedAt'] # index (inside the rates arrays) of closing trade 
	xClose.append( ratesTime[closedAt] ) # time of closing trade

	yOpen.append( ratesClose[i] ) # the rate value the trade is opened at 
	yClose.append( ret['closePrice'] ) # the rate value the trade is closed at

	xProfit.append( ratesTime[closedAt] ) # time the cumultive profit is changed
	profit = profit + ret['profit'] # Increasing or decreasing the cumulative profit
	yProfit.append( profit )  # current cumulative profit

	i = closedAt # going to the index where the trade was closed

ax211 = plt.subplot( 211 ) # Starting to draw the 'HI-LOW-TRADES' plot

plt.title( u"HI-LOW-TRADES" ) # The title of the plot

plt.xlabel( u'TIME' ) # 'X' axis label

plt.ylabel( u'HI-LOW-TRADES' ) # 'Y' axis label

plt.plot( ratesTime, ratesHigh, color="#cfcfcf" ) # High rates
plt.plot( ratesTime, ratesLow, color="#cfcfcf" ) # Low rates

plt.scatter( xOpen, yOpen, marker='o', color='g') # Drawing green 'o'-s (circles) to mark where trades were opened
plt.scatter( xClose, yClose, marker='x', color='r') # Drawing red 'x'-s to mark where trades were closed

# Displaying trades & cumulative profit change across time
for i in range( len(xOpen) ):
	plt.plot( [ xOpen[i], xClose[i] ], [ yOpen[i], yClose[i] ], color="#afafaf" )
	plt.text( xClose[i], yClose[i], "%+.0f$" % (yProfit[i+1]), horizontalalignment='right', verticalalignment='top', fontsize=10 )

plt.grid() # Drawing grid

plt.subplot( 212, sharex = ax211 ) # The 'PROFIT' plot, using the x-axis of the upper one ('sharex = ax211')

plt.title( u"PROFIT" ) # The title of the plot

plt.xlabel( u'TIME' ) # 'X' axis label

plt.ylabel( u'PROFIT' ) # 'Y' axis label

plt.plot( xProfit, yProfit ) # Profit plot 

plt.grid( True ) # Drawing grid

plt.show() # Displaying the plots

