import os
import numpy as np
from datetime import datetime 
from datetime import timedelta
import cPickle as pickle
import __init__ as taft

'''
Allowed tickers so far: BTCUSD, LTCUSD, EURUSD
'''
def loadDaily( ticker, startYear=1980, endYear=2100, startMonth=1, endMonth=1, startDay=1, endDay=None ):
	readError = False
	fileOpened = False
	
	linesRead = 0
	linesSkipped = 0

	op = []
	hi = []
	lo = []
	cl = []
	vol = []
	dtm = []

	dataPath = os.path.join( os.path.dirname(__file__),'data' )
	fileName = os.path.join( dataPath, ticker + "_D.csv" )

	if endDay is None:
		endDay = getEndDayOfMonth( endMonth )

	startDate = datetime.strptime( str(startYear) + ":" + str(startMonth) + ":" + str(startDay), "%Y:%m:%d" )
	endDate = datetime.strptime( str(endYear) + ":" + str(endMonth) + ":" + str(endDay), "%Y:%m:%d" )

	try:
		fileHandle = open(fileName, "r")
		fileOpened = True

		firstLine = True
		for line in fileHandle:

			if firstLine:
				firstLine = False
				linesSkipped += 1
				continue

			lineSplitted = line.split( "," )
			if len(lineSplitted) < 6:
				linesSkipped += 1
				continue

			strDateTime = lineSplitted[0]
			try:
				if len(strDateTime) == 14:
					dateTime = datetime.strptime(strDateTime, '%Y%m%d%H%M%S')
				elif len(strDateTime) == 17:
					dateTime = datetime.strptime(strDateTime, '%Y%m%d%H%M%S%f')
				else:
					linesSkipped += 1
					continue									
			except Exception:
				linesSkipped += 1
				continue				
			if dateTime < startDate:
				continue
			if dateTime > endDate:
				continue
	
			dtm.append( dateTime )

			op.append( float( lineSplitted[1] ) )
			hi.append( float( lineSplitted[2] ) )
			lo.append( float( lineSplitted[3] ) )
			cl.append( float( lineSplitted[4] ) )
			vol.append( float( lineSplitted[5].rstrip() ) )

			linesRead += 1	
	except Exception:
		readError = True
	
	if fileOpened:
		fileHandle.close()

	if readError:
		return( None )

	op = np.array( op[::-1], dtype='float' )
	hi = np.array( hi[::-1], dtype='float' )
	lo = np.array( lo[::-1], dtype='float' )
	cl = np.array( cl[::-1], dtype='float' )
	vol = np.array( vol[::-1], dtype='float' )
	dtm = dtm[::-1]

	return { 'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'dtm':dtm, 'length':linesRead, 'skipped':linesSkipped }
# end of loadDaily


def loadMinutes( ticker, startYear=2017, endYear=2017, startMonth=1, endMonth=10, startDay=1, endDay=None ):
	readError = False
	fileOpened = False
	
	linesRead = 0
	linesSkipped = 0

	op = []
	hi = []
	lo = []
	cl = []
	vol = []
	dtm = []

	dataPath = os.path.join( os.path.dirname(__file__),'data' )
	fileName = os.path.join( dataPath, ticker + "_m.csv" )

	if endDay is None:
		endDay = getEndDayOfMonth( endMonth )

	startDate = datetime.strptime( str(startYear) + ":" + str(startMonth) + ":" + str(startDay), "%Y:%m:%d" )
	endDate = datetime.strptime( str(endYear) + ":" + str(endMonth) + ":" + str(endDay), "%Y:%m:%d" )

	try:
		fileHandle = open(fileName, "r")
		fileOpened = True

		firstLine = True
		for line in fileHandle:

			if firstLine:
				firstLine = False
				linesSkipped += 1
				continue

			lineSplitted = line.split( "," )
			if len(lineSplitted) < 5:
				linesSkipped += 1
				continue

			strDateTime = lineSplitted[0]
			dateTime = datetime.strptime(strDateTime, '%Y%m%d%H%M%S%f')
			if dateTime < startDate:
				continue
			if dateTime > endDate:
				continue

			dtm.append( dateTime )

			op.append( float( lineSplitted[1] ) )
			hi.append( float( lineSplitted[2] ) )
			lo.append( float( lineSplitted[3] ) )
			cl.append( float( lineSplitted[4] ) )
			vol.append( 0 )

			linesRead += 1	
	except Exception:
		readError = True
	
	if fileOpened:
		fileHandle.close()

	if readError:
		return( None )

	op = np.array( op[::-1], dtype='float' )
	hi = np.array( hi[::-1], dtype='float' )
	lo = np.array( lo[::-1], dtype='float' )
	cl = np.array( cl[::-1], dtype='float' )
	vol = np.array( vol[::-1], dtype='float' )
	dtm = dtm[::-1]

	return { 'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'dtm':dtm, 'length':linesRead, 'skipped':linesSkipped }
# end of readMinutes


def getEndDayOfMonth( month ):
	if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
		endDay = 31
	elif month == 2:
		endDay = 28
	else:
		endDay = 30
	return endDay
# end of def 	


def reframeRates( rates, timeFrame ):
	dtm = []
	op = []
	hi= []
	lo = []
	cl = []
	vol = []

	ratesDtm = rates['dtm']
	lenRates = len( ratesDtm )
	if lenRates == 0:
		return None

	startIndex = lenRates - 1
	while( True ):
		startIndex, candle = reframeCandle( rates, startIndex, timeFrame )
		if startIndex < 0:
			break
		dtm.append( candle['dtm'] )
		op.append( candle['op'] )
		hi.append( candle['hi'] )
		lo.append( candle['lo'] )
		cl.append( candle['cl'] )
		vol.append( candle['vol'] )

	dtm = dtm[::-1]
	op = np.array( op[::-1], dtype=np.float )
	hi = np.array( hi[::-1], dtype=np.float )
	lo = np.array( lo[::-1], dtype=np.float )
	cl = np.array( cl[::-1], dtype=np.float )
	vol = np.array( vol[::-1], dtype=np.float )

	return { 'dtm':dtm, 'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'length':len(dtm) }

# end of def reFrameRates


def reframeCandle( rates, startIndex, timeFrame ):

	def getBeginningOfTimeFrame( dtmOfCandle, timeFrame ):
		
		if timeFrame < 60:
			excess = dtmOfCandle.minute % timeFrame
		elif timeFrame < 1440:
			excess = dtmOfCandle.minute + (dtmOfCandle.hour % (timeFrame/60)) * 60
		else:
			excess = dtmOfCandle.minute + dtmOfCandle.hour * 60

		if excess > 0:
			dtmOfBeginningOfCandle = dtmOfCandle - timedelta(minutes=excess)
		else:
			dtmOfBeginningOfCandle = dtmOfCandle

		return excess, dtmOfBeginningOfCandle
	# end of def

	timeCounter = 1

	dtmOfCandle = rates['dtm'][startIndex]
	excess, beginningOfTimeFrame = getBeginningOfTimeFrame( dtmOfCandle, timeFrame )
	if excess > 0:
		dtmOfCandle = beginningOfTimeFrame
	opOfCandle = rates['op'][startIndex]
	hiOfCandle = rates['hi'][startIndex]
	loOfCandle = rates['lo'][startIndex]
	clOfCandle = rates['cl'][startIndex]
	volOfCandle = rates['vol'][startIndex]

	for i in range( startIndex-1, -1, -1 ):

		excess, beginningOfTimeFrame = getBeginningOfTimeFrame( rates['dtm'][i], timeFrame )
		if beginningOfTimeFrame > dtmOfCandle:
			break

		if rates['hi'][i] > hiOfCandle:
			hiOfCandle = rates['hi'][i]
		if rates['lo'][i] < loOfCandle:
			loOfCandle = rates['lo'][i]
		clOfCandle = rates['cl'][i]
		volOfCandle += rates['vol'][i]

		timeCounter += 1
		#if timeCounter == timeFrame:
		#	print "breaking on time Counter (" + str(timeCounter) + ")" + str(rates['dtm'][i])
		#	break

	return (startIndex - timeCounter), {'dtm':dtmOfCandle,'op':opOfCandle,'hi':hiOfCandle,'lo':loOfCandle,'cl':clOfCandle,'vol':volOfCandle}
# end of def reFrameCandle


logMessage = ""

# Calculates (inputs, label, profit) for each data index by index 
def prepareData( rates, calcInp, calcInpParams, calcOut, calcOutParams, normalize=False, detachTest=20, precalcData=None ):
	global logMessage
	logMessage = ""
	retErr = None, None

	op = rates['op']
	hi = rates['hi']
	lo = rates['lo']
	cl = rates['cl']
	length = len( rates['op'] )
	if not 'vol' in rates:
		vol = np.zeros( shape=(length,), dtype=np.float32 )
	else:
		vol = rates['vol']
	if not 'dtm' in rates:
		dtm = np.zeros( shape=(length,), dtype=np.float32 ) 
	else:
		dtm = rates['dtm']

	# If data precalculation is required
	if precalcData is not None:
		precalculated = precalcData( rates, calcOutParams )
		calcOutParams['precalculated'] = precalculated

	nnDTM = []
	nnInputs = []
	nnLabels = []
	nnProfit = []
	for i in range(1,length):
		# Inputs
		pastRates = { 'op': op[i:], 'hi':hi[i:], 'lo':lo[i:], 'cl':cl[i:], 'vol':vol[i:], 'dtm':dtm[i:] }
		futureRates = { 'op': op[i-1::-1], 'hi':hi[i-1::-1], 'lo':lo[i-1::-1], 'cl':cl[i-1::-1], 'vol':vol[i-1::-1], 'dtm':dtm[i-1::-1] }

		inputs = calcInp( pastRates, calcInpParams )
		if inputs is None:
			continue

		res = calcOut( futureRates, calcOutParams )
		if not isinstance( res, tuple ):
			continue
		label, profit = res

		nnInputs.append( inputs )
		nnLabels.append( label )
		nnProfit.append( profit )
		nnDTM.append( dtm[i-1] )

	if len(nnInputs) == 0:
		return retErr
	if len(nnLabels) == 0:
		return retErr

	nnInputs = np.array( nnInputs, dtype='float' )
	numSamples, numFeatures = np.shape( nnInputs )
	nnLabels = np.array( nnLabels, dtype='float' )
	shape = np.shape( nnLabels )
	if len( shape ) == 2: # One Hot
		numLabels = shape[1]
	else:
		numLabels = int( np.max( nnLabels ) + 1 )	   
	nnProfit = np.array( nnProfit, dtype='float' )	  
	nnMean = np.zeros( shape=[numFeatures], dtype='float' )
	nnStd = np.zeros( shape=[numFeatures], dtype='float' )

	if detachTest is not None:
		detachStart = int( float(numSamples) * detachTest / 100.0 )

	if normalize: # If normalization is required
		normIntervalStart = 0
		if detachTest is not None:
			normIntervalStart = detachStart

		for i in range(numFeatures):
			status, mean, std = taft.normalize( nnInputs[:,i], normInterval=[normIntervalStart,numSamples] )
			if status is None:
				logMessage += "Can't normalize %d column\n." % (i)
				return None
			nnMean[i] = mean
			nnStd[i] = std
	else:
		logMessage += "Normalization skipped.\n"
		nnMean = None
		nnStd = None

	if detachTest is None:
		retval1 = { 'inputs': nnInputs, 'labels': nnLabels, 'profit': nnProfit, 
			'numSamples':numSamples, 'numFeatures':numFeatures, 'numLabels':numLabels, 'mean':nnMean, 'std':nnStd, 'dtm':nnDTM }	
		retval2 = None
	else:
		retval1 = { 'inputs': nnInputs[detachStart:], 'labels': nnLabels[detachStart:], 'profit': nnProfit[detachStart:], 
			'numSamples':numSamples-detachStart, 'numFeatures':numFeatures, 'numLabels':numLabels, 
			'mean':nnMean, 'std':nnStd, 'dtm':nnDTM[detachStart:] }	
		retval2 = { 'inputs': nnInputs[:detachStart], 'labels': nnLabels[:detachStart], 'profit': nnProfit[:detachStart], 
			'numSamples':detachStart, 'numFeatures':numFeatures, 'numLabels':numLabels, 
			'mean':nnMean, 'std':nnStd, 'dtm':nnDTM[:detachStart] }	

	return( retval1, retval2 )
# end of def prepareData


def countLabels( labels ):
	shape = np.shape( labels )
	if len(shape) == 2: # One-hot
		rows, cols = shape
		labelsCounter = np.zeros( shape=[cols] )
		for i in range( rows ):
			for j in range( cols ):
				if labels[i][j] == 1:
					labelsCounter[j] += 1
		return labelsCounter
	else: # Not one-hot
		rows = shape[0]
		maxLabel = int( np.max( labels ) )
		labelsCounter = []
		for i in range(maxLabel+1):
			labelsCounter.append(0)
		for i in range(rows):
			labelsCounter[ int(labels[i]) ] += 1
		return labelsCounter
# end of def


def saveModel( fileName, model, calcInp, calcInpParams ):	
	global logMessage
	ok = True

	logMessage = ""
	logMessage += "Saving into \"%s\"...\n" % (fileName)

	try:	
		fileHandle = open(fileName, 'wb')
	except Exception:
		ok = False

	if ok:
		try:
			pickle.dump( { "model": model, "calcInp": calcInp, "calcInpParams":calcInpParams }, fileHandle, 2 )
		except Exception:
			ok = False
		finally:
			fileHandle.close()

	return ok
# end of saveModel()


def loadModel( fileName ):
	global logMessage
	ok = True

	logMessage = ""
	logMessage += "Reading data from \"%s\"...\n" % ( fileName )

	try:
		fileHandle = open( fileName, 'rb' )
	except Exception:
		ok = False
		logMessage += "Can't open file %s.\n" % ( fileName )

	if ok:
		try:
			loadObject = pickle.load( fileHandle )
		except Exception:
			ok = False
			logMessage += "Error reading the data.\n"
		finally:
			fileHandle.close()
	
	if not ok:
		return None
	return { 'model':loadObject['model'], 'calc':loadObject['calcInp'], 'params':loadObject['calcInpParams'] }
# end of loadModel()


def precalcFutureReturn( rates, params ):
	numLabels = params['numLabels']
	lookAhead = params['lookAhead']-1

	if lookAhead > 0:
		op = rates['op'][lookAhead:]
		cl = rates['cl'][:-lookAhead]
	else:
		op = rates['op']
		cl = rates['cl']

	diffs = cl-op
	lenDiffs = len(diffs)
	sortedDiffs = np.sort( diffs )
	
	ret = {}
	for i in range(numLabels-1):
		index = int( (i+1) * float(lenDiffs) / float(numLabels) + 0.5 )
		ret['splitter' + str(i)] = sortedDiffs[index]

	mean = np.mean( diffs )
	std = np.std( diffs )
	ret['mean'] = mean
	ret['std'] = std
	meanAbs = np.mean( np.abs(diffs) )
	stdAbs = np.std( np.abs(diffs) )
	ret['meanAbs'] = meanAbs
	ret['stdAbs'] = stdAbs

	return ret
# end of def


def calcFutureReturn( rates, params ):
	numLabels = params['numLabels']
	lookAhead = params['lookAhead']-1

	if lookAhead >= len( rates['cl'] ):
		return None

	profit = rates['cl'][lookAhead] - rates['op'][0]
	isLabel = False
	for i in range( numLabels-1 ):
		if profit < params['precalculated']['splitter'+str(i)]:
			label=i
			isLabel = True
			break
	if not isLabel:
		label = numLabels-1

	return label, profit
# end of def



def calcFutureNHNL( rates, params ):
	numLabels = params['numLabels']
	lookAhead = params['lookAhead']

	if lookAhead >= len( rates['cl'] ) or lookAhead < 2:
		return None

	# Calcualting NH/NL ratio
	hi = rates['hi'][:lookAhead]
	lo = rates['lo'][:lookAhead]
	v1 = taft.pNextHigher( lookAhead, hi[::-1] )
	v2 = taft.pNextLower( lookAhead, lo[::-1] )
	if v1 is None or v2 is None:
		return None

	vSum = v1 + v2
	if not( vSum > 0 ):
		ratio = 0.0
	else:
		ratio = (v1-v2) / vSum

	# Getting the scale to label the ratio value
	if not 'lookAheadScale' in params:
		scale = calcScale( numLabels )
		params['lookAheadScale'] = scale
	else:
		scale = params['lookAheadScale']

	# Labeling the ratio value 
	label = -1
	for l in range( numLabels-1 ):
		if ratio < scale[l]:
			label=l
			break
	if label == -1:
		label = numLabels-1

	profit = rates['cl'][lookAhead-1] - rates['op'][0]

	return label, profit
# end of def


def calcPastROCs( pastRates, params ):
	step0 = params['step0']
	stepSize = params['stepSize']
	stepMax = params['stepMax']
	if 'stepSizeInc' in params:
		stepSizeInc = params['stepSizeInc']
	else:
		stepSizeInc = 0

	inputs = []

	period = step0
	curStep = 0
	while( curStep < stepMax ):

		if period == step0:
			ind = taft.roc( period=period, rates=pastRates['cl'] )
			if ind == None:
				return None
			inputs.append(ind/100.0)

		ind = taft.roc( period=period, rates=pastRates['hi'] )
		if ind == None:
			return None
		inputs.append(ind/100.0)

		ind = taft.roc( period=period, rates=pastRates['lo'] )
		if ind == None:
			return None
		inputs.append(ind/100.0)

		period += stepSize + stepSizeInc*curStep
		curStep += 1

	return inputs
# end of def

def calcPastSTOs( pastRates, params ):
	step0 = params['step0']
	stepSize = params['stepSize']
	stepMax = params['stepMax']
	if 'stepSizeInc' in params:
		stepSizeInc = params['stepSizeInc']
	else:
		stepSizeInc = 0

	inputs = []

	period = step0
	curStep = 0
	while( curStep < stepMax ):
		ret = stochastic( periodK=period, hi=pastRates['hi'], lo=pastRates['lo'], cl=pastRates['cl'] )
		if ret is None:
			return None
		ind = ret['K']
		inputs.append(ind/100.0)

		period += stepSize + stepSizeInc*curStep
		curStep += 1

	return inputs
# end of def


def calcPastNHNLs( pastRates, params ):

	step0 = params['step0']
	stepSize = params['stepSize']
	stepMax = params['stepMax']
	if 'stepSizeInc' in params:
		stepSizeInc = params['stepSizeInc']
	else:
		stepSizeInc = 0

	inputs = []

	period = step0
	curStep = 0
	while( curStep < stepMax ):

		ind = taft.pNextHigher( period, pastRates['hi'] )
		if ind == None:
			return None
		inputs.append( ind )

		ind = taft.pNextLower( period, pastRates['lo'] )
		if ind == None:
			return None
		inputs.append( ind )

		period += stepSize + stepSizeInc*curStep
		curStep += 1

	return inputs
# end of def


def calcScale( numLabels ):
	scale = []
	splitter = 2.0 / float(numLabels)
	for i in range(1,numLabels):
		scale.append( -1.0 + splitter*float(i) )
	return scale
# end of def