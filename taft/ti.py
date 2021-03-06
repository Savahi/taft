import numpy as np

from data import _defineRates

# AD-indicator
def ad( period=1, shift=0, hi=None, lo=None, cl=None, vol=None, prev=None ):
	(hi, lo, cl, vol) = _defineRates( hi=hi, lo=lo, cl=cl, vol=vol )
	if hi is None or lo is None or cl is None or vol is None:
		return None

	adValue = None
	if prev is not None:
		if shift < len(cl):
			adValue = prev + ad1( hi[shift], lo[shift], cl[shift], vol[shift] ) 
	else:
		startIndex = shift + period - 1
		if startIndex < len(cl):
			prevAdValue = 0.0
			for i in range( startIndex, shift-1, -1 ):
				adValue = prevAdValue + ad1( hi[i], lo[i], cl[i], vol[i] ) 
				prevAdValue = adValue
	
	return adValue
# end of AD

def ad1( hi,lo,cl,vol ):
	highLessLow = hi - lo
	if highLessLow > 0.0:
		closeLessLow = cl - lo
		highLessClose = hi - cl
		return ( ( vol * ( closeLessLow - highLessClose ) ) / highLessLow )
	return 0
# end of ad1

# ADX-indicator
def adx( period=14, shift=0, hi=None, lo=None, cl=None, prev=None ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	if prev is not None:
		if shift+1 >= len(cl):
			return None

		smoothedTr = prev['trsm']
		smoothedPlusDM = prev['pdmsm']
		smoothedMinusDM = prev['pdmsm']	
		tr = max( hi[shift] - lo[shift], abs( hi[shift] - cl[shift+1]), abs(lo[shift]-cl[shift+1]) )
		plusDM = 0.0
		minusDM = 0.0
		upMove = hi[shift] - hi[shift+1]
		downMove = lo[shift+1] - lo[shift]
		if upMove > downMove and upMove > 0.0:
			plusDM = upMove
		if downMove > upMove and downMove > 0.0:
			minusDM = downMove
		
		smoothedTr = smoothedTr - smoothedTr / period + tr
		if not( smoothedTr > 0.0 ):
			return None 
		smoothedPlusDM = smoothedPlusDM - smoothedPlusDM / period + plusDM
		smoothedMinusDM = smoothedMinusDM - smoothedMinusDM / period + minusDM

		plusDI = 100.0 * (smoothedPlusDM / smoothedTr)
		minusDI = 100.0 * (smoothedMinusDM / smoothedTr)
		sumDI = plusDI + minusDI
		if not( sumDI > 0.0 ):
			return None
		dx0 = 100.0 * ( abs( plusDI - minusDI ) / sumDI )
		adx = ( prev['adx'] * (period-1.0) + dx0 ) / period

	else:
		st = shift + period * 2 - 2
		if st+1 >= len(cl):
			return None

		plusDM = np.zeros( shape=period*2, dtype="float" )
		minusDM = np.zeros( shape=period*2, dtype="float" )
		tr = np.empty( shape=period*2, dtype='float')

		for i in range( st, shift-1, -1 ):
			upMove = hi[i] - hi[i+1]
			downMove = lo[i+1] - lo[i]

			index = i-shift
			if upMove > downMove and upMove > 0.0:
				plusDM[index] = upMove

			if downMove > upMove and downMove > 0.0:
				minusDM[index] = downMove
		
			tr[index] = max( hi[i] - lo[i], abs( hi[i] - cl[i+1]), abs(lo[i]-cl[i+1]) )

		# for i in range(st, shift-1,-1):
		# 	print str(i) + ": tr =" + str( tr[i-shift] ) + ", plusDM=" + str( plusDM[i-shift] ) + ", minusDM=" + str( minusDM[i-shift] )
		
		dx = np.empty( shape = period, dtype='float' )
		smoothedTr = None
		smoothedPlusDM = None
		smoothedMinusDM = None	
		for i in range( shift + period-1, shift-1, -1 ):
			index = i - shift
			if smoothedTr is None:
				smoothedTr = np.sum( tr[index:index+period] )
			else:
				smoothedTr = smoothedTr - smoothedTr / period + tr[index]
			if smoothedPlusDM is None:
				smoothedPlusDM = np.sum( plusDM[index:index+period] )
			else:
				smoothedPlusDM = smoothedPlusDM - smoothedPlusDM / period + plusDM[index]
			if smoothedMinusDM is None:
				smoothedMinusDM = np.sum( minusDM[index:index+period] )
			else:
				smoothedMinusDM = smoothedMinusDM - smoothedMinusDM / period + minusDM[index]

			if not( smoothedTr > 0.0 ):
				return None 
			plusDI = 100.0 * (smoothedPlusDM / smoothedTr)
			minusDI = 100.0 * (smoothedMinusDM / smoothedTr)
			sumDI = plusDI + minusDI
			if not( sumDI > 0.0 ):
				return None
			dx[index] = 100.0 * ( abs( plusDI - minusDI ) / ( plusDI + minusDI ) )

		adx = np.mean( dx )
		dx0 = dx[0]

	return( { 'adx': adx, 'dx': dx0, "pdi": plusDI, "mdi": minusDI, "pdmsm": smoothedPlusDM, "pdmsm": smoothedMinusDM, "trsm": smoothedTr } )
# end of ADX	

def aroon( period=14, shift=0, rates=None ):
	global _close
	if rates is None:
		rates = _close
	if rates is None:
		return None

	notAssigned = True
	highest = -1.0 # Highest high to be stored here
	highestIndex = -1.0 # The highest high index to be stored here
	lowest = -1.0 # Lowest low to be stored here
	lowestIndex = -1.0 # The lowest low index to be stored here

	endIndex = shift + period + 1
	if endIndex > len(rates):
		return None

	for i in range( shift, endIndex ):
		priceValue = rates[i]
		if notAssigned: 
			highest = priceValue;
			highestIndex = i;
			lowest = priceValue;
			lowestIndex = i;
			notAssigned = False;
		else:
			if highest < priceValue:
				highest = priceValue;
				highestIndex = i;
			elif lowest > priceValue:
				lowest = priceValue;
				lowestIndex = i;

	if notAssigned:
		return None

	up = (period - (highestIndex-shift)) * 100.0 / period;
	down = (period - (lowestIndex-shift)) * 100.0 / period;

	return ( { 'up': up, 'down':down } )
# end of aroon	


# ATR - Average True Range
def atr( period=14, shift=0, hi=None, lo=None, cl=None, prev=None ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	trValue = None
	atrValue = None
	if prev is not None:
		if prev['atr'] is not None:
			if shift < len(cl):
				trValue = tr( hi, lo, cl, shift )
				atrValue = (prev['atr'] * (period-1) + trValue) / period	
	if atrValue is None:
		if shift + period - 1 < len(cl):
			trValues = np.empty( shape=period, dtype='float' )
			for i in range( shift+period-1, shift-1, -1 ):
				trValues[i-shift] = tr( hi, lo, cl, i )
			trValue = trValues[0]
			atrValue = np.mean( trValues )

	return { 'atr':atrValue, 'tr':trValue }
# end of atr


def tr( hi, lo, cl, shift ):
	trValue = None
	lenCl = len(cl)
	if shift + 1 < lenCl:
		trValue = max( hi[shift] - lo[shift], abs(hi[shift] - cl[shift+1]), abs(lo[shift] - cl[shift+1]) )
	elif shift < lenCl:
		trValue = hi[shift] - lo[shift]
	return trValue
#end of tr


# Bollinger Bands
def bollinger( period=20, shift=0, nStds=2.0, rates=None ):
	(rates,) = _defineRates( cl=rates )
	if rates is None:
		return None

	en = shift + period
	if en > len(rates):
		return None

	bandMiddle = np.mean( rates[shift:en] )
	bandStd = np.std( rates[shift:en] )

	#print "bandMiddle=%s , nStds=%s ,bandStd = %s" % (str(bandMiddle),str(nStds),str(bandStd))
	top = (bandMiddle + nStds * bandStd)
	bottom = (bandMiddle - nStds * bandStd)
	return( { 'ma':bandMiddle, 'std': bandStd, 'top': top, 'bottom': bottom  } )
# end of bollinger


# CCI indicator
def cci( period=20, shift=0, hi=None, lo=None, cl=None, cciConst=0.015 ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	if shift + period - 1 >= len(cl):
		return None
		
	typicalPrices = np.empty( shape = period, dtype='float')
	for i in range( shift+period-1, shift-1, -1 ):
		typicalPrices[shift-i] = (hi[i] + lo[i] + cl[i]) / 3.0
	
	meanTypicalPrice = np.mean( typicalPrices )	

	sumDeviation = 0.0
	for i in range( shift+period-1, shift-1, -1 ):
		sumDeviation = sumDeviation + abs( meanTypicalPrice - typicalPrices[shift-i] )
	if not( sumDeviation > 0.0 ):
		return None
	meanDeviation = sumDeviation / period

	cciValue = (typicalPrices[0] - meanTypicalPrice) / (cciConst * meanDeviation)

	return { 'cci': cciValue, 'meanTypicalPrice': meanTypicalPrice, 'meanDeviation': meanDeviation }
# end of CCI


# EMA - Exponential Moving Average
def ema( period=10, shift=0, alpha=None, rates=None, prev=None, history=0 ):			
	global _close
	if rates is None:
		rates = _close
	if rates is None:
		return None

	if alpha is None:
		alpha = 2.0 / (period + 1.0)

	emaValue = None
	lenRates = len(rates)

	# Previously calculated ema is given 
	if prev is not None:
		if shift < lenRates:
			emaValue = (rates[shift] - prev) * alpha + prev
	else:
		if history == 0:
			end = shift + period
			if shift < lenRates:
				if end > lenRates:
					end = lenRates
				emaValue = np.mean( rates[shift:end] )
		else:
			end = shift + period + history - 1
			if end < len(rates):
				emaValue = np.mean( rates[ shift+history: end+1 ] )
				for i in range( shift+history-1, shift-1,-1 ):
					emaValue = (rates[i] - emaValue) * alpha + emaValue
	return emaValue
# end of ema


# MACD - Moving Average Convergence/Divergence Oscillator
def macd( periodFast=12, periodSlow=26, periodSignal=9, shift=0, rates=None, prev=None ):
	global _close
	if rates is None:
		rates = _close
	if rates is None:
		return None

	#st = shift + periodSlow + periodSignal - 1
	#if st >= len(rates):
	#	return None

	if prev is not None:
		emaFast = ema( period=periodFast, rates=rates, shift=shift, prev = prev['fast'] )
		emaSlow = ema( period=periodSlow, rates=rates, shift=shift, prev = prev['slow'] )
		if emaFast is None or emaSlow is None:
			macd = None
			emaSignal = None
		else:
			macd = emaFast - emaSlow
			emaSignal = ema( period=periodSignal, rates=[macd], shift=shift, prev=prev['signal'] )
	else:
		emaFast = ema( period=periodFast, shift=shift, rates=rates )
		emaSlow = ema( period=periodSlow, shift=shift, rates=rates )
		if emaFast is None or emaSlow is None:
			macd = None
			emaSignal = None
		else:
			macd = emaFast - emaSlow
			emaSignal = ema( period=periodSignal, shift=shift, rates=[macd] )
	if macd is not None and emaSignal is not None:
		histogram = (macd - emaSignal)
	else:
		histogram = None

	if macd is None or emaSignal is None or histogram is None:
		return None 
	return( {'slow': emaSlow, 'fast': emaFast, 'macd': macd, 'signal': emaSignal, 'histogram': histogram } )
# end of macd


# SMMA - Smooothed Moving Average
def smma( period, shift=0, rates=None ):
	return ema( period=period, shift=shift, alpha = 1.0 / period, rates=rates )
# end of smma
	
# ROC - Rate Of Change indicator
def roc( period=12, shift=0, rates=None ):
	(rates,) = _defineRates(cl=rates)
	if rates is None:
		return None

	nPeriodsAgoIndex = shift + period 
	if nPeriodsAgoIndex >= len(rates):
		return None
	if not( rates[nPeriodsAgoIndex] > 0 ):
		return None

	return ( rates[shift] - rates[nPeriodsAgoIndex] ) * 100.0 / rates[nPeriodsAgoIndex]
# end of roc


# RSI - Relative Strength Index
def rsi( period=14, shift=0, rates=None, prev = None ):
	(rates,) = _defineRates( cl=rates )
	if rates is None:
		return None

	averageGainPrev = None
	averageLossPrev = None
	if prev is not None:
		averageGainPrev = prev['averageGain']
		averageLossPrev = prev['averageLoss']

	if (averageGainPrev is not None) and (averageLossPrev is not None):
		if shift + 1 >= len(rates):
			return None
		difference = rates[shift] - rates[shift+1]
		currentGain = 0.0
		currentLoss = 0.0
		if difference > 0.0: 
			currentGain = difference
		if difference < 0.0:
			currentLoss = -difference
		averageGain = (averageGainPrev * (period - 1.0) + currentGain) / period 
		averageLoss = (averageLossPrev * (period - 1.0) + currentLoss) / period 
	else:
		st = shift + period
		if st >= len(rates):
			return None 
		upSum = 0.0
		downSum = 0.0
		for i in range( st, shift, -1 ):
			difference = rates[i-1] - rates[i]
			if difference > 0:
				upSum += difference
			elif difference < 0:
				downSum += -difference
		averageGain = upSum / period
		averageLoss = downSum / period

	if not( averageLoss > 0.0 ):
		rsiValue = 100.0
		rs = "HUGE!"
	else:
		rs = averageGain / averageLoss
		rsiValue = 100.0 - 100.0 / ( 1.0 + rs )

	return( { 'rsi':rsiValue, 'rs':rs, 'averageGain': averageGain, 'averageLoss': averageLoss } )
# end of rsi


# SMA - Simple Moving Average
def sma( period=10, shift=0, rates=None ):
	(rates,) = _defineRates( cl=rates )
	if rates is None:
		return None
	
	lenRates = len(rates)
	endIndex = shift + period
	if endIndex > lenRates:
		return None

	return np.mean( rates[shift:endIndex] )	
# end of sma


# Stochastic (FSI) - Stochastic Oscillator
def stochastic( period=14, periodD=3, smoothing=1, shift=0, hi=None, lo=None, cl=None ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	ratesLen = len(cl)
	if shift + period + periodD - 1 >= ratesLen:
		if shift + period - 1 >= ratesLen: # The 'K' value is also impossible to calculate?
			return None
		valueK = stochasticK( hi, lo, cl, shift, shift + period - 1 ) # Calculating the 'K' value only
		if valueK is None:
			return None
		return( { 'k':valueK, 'd':None } )

	valuesK = np.empty( shape=periodD, dtype='float' )
	for i in range( periodD ):
		valueK = stochasticK( hi, lo, cl, shift+i, shift + i + period - 1 )
		if valueK is None:
			return None
		valuesK[i] = valueK

	return( { 'k': valuesK[0], 'd': np.mean( valuesK ) } )
# end of stochastic

def stochasticK( hi, lo, cl, st, en ):
	minLow = lo[st]
	maxHigh = hi[st]
	for i in range( st+1, en+1 ):
		if lo[i] < minLow:
			minLow = lo[i]
		if hi[i] > maxHigh:
			maxHigh = hi[i]
	difference = maxHigh - minLow
	if not ( difference > 0 ):
		return None

	return (cl[st] - minLow) * 100.0 / difference
# end of stochasticK


def williams( period=14, shift=0, hi=None, lo=None, cl=None ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	endIndex = shift + period
	if endIndex > len(cl):
		return None

	lowestLow = np.min( lo[shift:endIndex] )
	highestHigh = np.max( hi[shift:endIndex] )
	diff = highestHigh - lowestLow
	if not (diff > 0):
		return None

	return (highestHigh-cl[shift]) / diff * (-100.0)
# end of williams


def awesome( period1=5, period2=34, shift=0, hi=None, lo=None ):
	(hi, lo) = _defineRates( hi=hi, lo=lo )
	if hi is None or lo is None:
		return None

	endIndex = shift + period1
	if endIndex > len(hi):
		return None
	v1 = (hi[shift:endIndex] + lo[shift:endIndex])/2.0
	
	endIndex = shift + period2
	if endIndex > len(hi):
		return None
	v2 = (hi[shift:endIndex] + lo[shift:endIndex])/2.0

	return (v1-v2)
# end of awesome

def pNextHigher( period, rates ):
	(rates,) = _defineRates(cl=rates)
	if rates is None:
		return None

	if len(rates) < period or period < 2:
		return None

	numH = 0.0
	for i in range(1,period):
		if rates[i-i] > rates[i]:
			numH += 1.0

	return numH / (period-1.0)
# end of def 


def pNextLower( period, rates ):
	(rates,) = _defineRates(cl=rates)
	if rates is None:
		return None

	if len(rates) < period or period < 2:
		return None

	numL = 0.0
	for i in range(1,period):
		if rates[i-1] < rates[i]:
			numL += 1.0

	return numL / (period-1.0)
# end of def 

