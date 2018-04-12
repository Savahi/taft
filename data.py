"""
Basic data manipulation
"""

import os
import numpy as np
from datetime import datetime 
from datetime import timedelta
import dill
import i_indicators as taft

def LoadFinam(FileName, StartYear=None, EndYear=None,StartMonth=1, EndMonth=12, StartDay=1, EndDay=None):
    ReadError = False
    FileOpened = False
    LinesRead = 0
    LinesSkipped = 0

    if EndDay is None:
        EndDay = GetEndDayOfMonth(EndMonth, EndYear)
    if StartYear is None:
        StartYear = 1900
    if EndYear is None:
        EndYear = 2200
        
    StartDate = datetime.strptime(str(StartYear) + ":" + str(StartMonth) + ":" + str(StartDay), "%Y:%m:%d")
    EndDate = datetime.strptime(str(EndYear) + ":" + str(EndMonth) + ":" + str(EndDay), "%Y:%m:%d")

    op = []
    hi = []
    lo = []
    cl = []
    vol = []
    dtm = []

    try:
        FileHandle = open(FileName, "r")
        FileOpened = True
        FirstLine = True
        for line in FileHandle:
            if FirstLine:
                FirstLine = False
                LinesSkipped += 1
                continue

            LineSplitted = line.split(",")
            if len(LineSplitted) < 9:
                LinesSkipped += 1
                continue

            StrDate = LineSplitted[2]
            StrTime = LineSplitted[3]

            DateTime = datetime.strptime(StrDate + " " + StrTime, '%Y%m%d %H%M%S')

            if DateTime < StartDate:
                continue
            if DateTime > EndDate:
                continue

            dtm.append(DateTime)
            op.append(float(LineSplitted[4]))
            hi.append(float(LineSplitted[5]))
            lo.append(float(LineSplitted[6]))
            cl.append(float(LineSplitted[7]))
            vol.append(float(LineSplitted[8].rstrip()))

            LinesRead += 1    
    except IOError:
        ReadError = True

    if FileOpened:
        FileHandle.close()

    if ReadError:
        return(None)

    op = np.array(op[::-1], dtype='float')
    hi = np.array(hi[::-1], dtype='float')
    lo = np.array(lo[::-1], dtype='float')
    cl = np.array(cl[::-1], dtype='float')
    vol = np.array(vol[::-1], dtype='float')
    dtm = dtm[::-1]

    return {'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'dtm':dtm, 'length':LinesRead, 'skipped':LinesSkipped}
# end of readFinam


'''
Allowed tickers so far: BTCUSD, LTCUSD, EURUSD
'''
def LoadDaily(ticker, startYear=1980, endYear=2100, startMonth=1, endMonth=12, startDay=1, endDay=None):
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

    dataPath = os.path.join(os.path.dirname(__file__),'data')
    fileName = os.path.join(dataPath, ticker + "_D.csv")

    if endDay is None:
        endDay = GetEndDayOfMonth(endMonth)

    startDate = datetime.strptime(str(startYear) + ":" + str(startMonth) + ":" + str(startDay), "%Y:%m:%d")
    endDate = datetime.strptime(str(endYear) + ":" + str(endMonth) + ":" + str(endDay), "%Y:%m:%d")

    try:
        fileHandle = open(fileName, "r")
        fileOpened = True

        firstLine = True
        for line in fileHandle:

            if firstLine:
                firstLine = False
                linesSkipped += 1
                continue

            lineSplitted = line.split(",")
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
    
            dtm.append(dateTime)

            op.append(float(lineSplitted[1]))
            hi.append(float(lineSplitted[2]))
            lo.append(float(lineSplitted[3]))
            cl.append(float(lineSplitted[4]))
            vol.append(float(lineSplitted[5].rstrip()))

            linesRead += 1    
    except Exception:
        readError = True
    
    if fileOpened:
        fileHandle.close()

    if readError:
        return(None)

    op = np.array(op[::-1], dtype='float')
    hi = np.array(hi[::-1], dtype='float')
    lo = np.array(lo[::-1], dtype='float')
    cl = np.array(cl[::-1], dtype='float')
    vol = np.array(vol[::-1], dtype='float')
    dtm = dtm[::-1]

    return {'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'dtm':dtm, 'length':linesRead, 'skipped':linesSkipped}
# end of loadDaily


def LoadMinutes(ticker, startYear=2017, endYear=2017, startMonth=1, endMonth=10, startDay=1, endDay=None):
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
    
    dataPath = os.path.join(os.path.dirname(__file__),'data')
    fileName = os.path.join(dataPath, ticker + "_m.csv")
    print(fileName)
    
    if endDay is None:
        endDay = GetEndDayOfMonth(endMonth)
        
    startDate = datetime.strptime(str(startYear) + ":" + str(startMonth) + ":" + str(startDay), "%Y:%m:%d")
    endDate = datetime.strptime(str(endYear) + ":" + str(endMonth) + ":" + str(endDay), "%Y:%m:%d")
    
    try:
        fileHandle = open(fileName, "r")
        fileOpened = True
        
        firstLine = True
        for line in fileHandle:
            if firstLine:
                firstLine = False
                linesSkipped += 1
                continue
                
            lineSplitted = line.split(",")
            if len(lineSplitted) < 5:
                linesSkipped += 1
                continue
                
            strDateTime = lineSplitted[0]
            dateTime = datetime.strptime(strDateTime, '%Y%m%d%H%M%S%f')
            if dateTime < startDate:
                continue
            if dateTime > endDate:
                continue
                
            dtm.append(dateTime)
            
            op.append(float(lineSplitted[1]))
            hi.append(float(lineSplitted[2]))
            lo.append(float(lineSplitted[3]))
            cl.append(float(lineSplitted[4]))
            vol.append(0)
            
            linesRead += 1    
    except Exception:
        readError = True
    
    if fileOpened:
        fileHandle.close()

    if readError:
        return(None)

    op = np.array(op[::-1], dtype='float')
    hi = np.array(hi[::-1], dtype='float')
    lo = np.array(lo[::-1], dtype='float')
    cl = np.array(cl[::-1], dtype='float')
    vol = np.array(vol[::-1], dtype='float')
    dtm = dtm[::-1]
    
    return {'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'dtm':dtm, 'length':linesRead, 'skipped':linesSkipped}
# end of readMinutes


def GetEndDayOfMonth(month, year = None):
    LeapYear = 0
    if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
            endDay = 31
    elif month == 2:
            endDay = 28
    else:
            endDay = 30
    return endDay
# end of def     


def ReframeRates(rates, timeFrame):
    dtm = []
    op = []
    hi= []
    lo = []
    cl = []
    vol = []
    
    #ratesDtm = rates['dtm']
    #lenRates = len(ratesDtm)
    LengthOfRates = rates['length']
    if LengthOfRates == 0:
        return None

    startIndex = LengthOfRates - 1
    while(True):
        startIndex, candle = ReframeCandle(rates, startIndex, timeFrame)
        if startIndex < 0:
            break
        dtm.append(candle['dtm'])
        op.append(candle['op'])
        hi.append(candle['hi'])
        lo.append(candle['lo'])
        cl.append(candle['cl'])
        vol.append(candle['vol'])
        
    dtm = dtm[::-1]
    op = np.array(op[::-1], dtype=np.float)
    hi = np.array(hi[::-1], dtype=np.float)
    lo = np.array(lo[::-1], dtype=np.float)
    cl = np.array(cl[::-1], dtype=np.float)
    vol = np.array(vol[::-1], dtype=np.float)
    
    return {'dtm':dtm, 'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'length':len(dtm)}
    
# end of def reFrameRates


def ReframeCandle(rates, startIndex, timeFrame):

    def getBeginningOfTimeFrame(dtmOfCandle, timeFrame):
        if timeFrame < 60:
            excess = dtmOfCandle.minute % timeFrame
            print(excess)
        elif timeFrame < 1440:
            excess = dtmOfCandle.minute + (dtmOfCandle.hour % (timeFrame/60)) * 60
            print(excess)
        else:
            excess = dtmOfCandle.minute + dtmOfCandle.hour * 60
            print(excess)
        if excess > 0:
            dtmOfBeginningOfCandle = dtmOfCandle - timedelta(minutes=excess)
        else:
            dtmOfBeginningOfCandle = dtmOfCandle
        return excess, dtmOfBeginningOfCandle
    # end of def

    timeCounter = 1

    dtmOfCandle = rates['dtm'][startIndex]
    excess, beginningOfTimeFrame = getBeginningOfTimeFrame(dtmOfCandle, timeFrame)
    if excess > 0:
        dtmOfCandle = beginningOfTimeFrame
    opOfCandle = rates['op'][startIndex]
    hiOfCandle = rates['hi'][startIndex]
    loOfCandle = rates['lo'][startIndex]
    clOfCandle = rates['cl'][startIndex]
    volOfCandle = rates['vol'][startIndex]

    for i in range(startIndex-1, -1, -1):
        excess, beginningOfTimeFrame = getBeginningOfTimeFrame(rates['dtm'][i], timeFrame)
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
        #    print "breaking on time Counter (" + str(timeCounter) + ")" + str(rates['dtm'][i])
        #    break

    return (startIndex - timeCounter), {'dtm':dtmOfCandle,'op':opOfCandle,'hi':hiOfCandle,'lo':loOfCandle,'cl':clOfCandle,'vol':volOfCandle}
# end of def reFrameCandle


logMessage = ""

def getLogMessage():
    global logMessage
    return logMessage
    

# Calculates (inputs, label, profit) for each data index by index 
def prepareData(rates, calcInp, calcInpParams, calcOut, calcOutParams, normalize=False, detachTest=20, precalcData=None):
    global logMessage
    logMessage = ""
    retErr = None, None

    op = rates['op']
    hi = rates['hi']
    lo = rates['lo']
    cl = rates['cl']
    #length = len(rates['op'])
    length = rates['length']
    if not 'vol' in rates:
        vol = np.zeros(shape=(length,), dtype=np.float32)
    else:
        vol = rates['vol']
    if not 'dtm' in rates:
        dtm = np.zeros(shape=(length,), dtype=np.float32) 
    else:
        dtm = rates['dtm']
        
    print(precalcData)

    # If data precalculation is required
    if precalcData is not None:
        precalculated = precalcData(rates, calcOutParams)
    else:
        precalculated = precalcFutureReturn(rates, calcOutParams)
    calcOutParams['precalculated'] = precalculated
    
    if calcOut is None:
        calcOut = calcFutureReturn    
        
    nnOp = []
    nnDTM = []
    nnInputs = []
    nnLabels = []
    nnProfit = []
    nnRateIndexes = []
    nnCustomOut = []
    for i in range(1,length):
        # Inputs
        pastRates = {'op': op[i:], 'hi':hi[i:], 'lo':lo[i:], 'cl':cl[i:], 'vol':vol[i:], 'dtm':dtm[i:]}
        futureRates = {'op': op[i-1::-1], 'hi':hi[i-1::-1], 'lo':lo[i-1::-1], 'cl':cl[i-1::-1], 'vol':vol[i-1::-1], 'dtm':dtm[i-1::-1]}
        
        inputs = calcInp(pastRates, calcInpParams)
        if inputs is None:
            continue
            
        res = calcOut(futureRates, calcOutParams)
        if not isinstance(res, tuple):
            continue
        if len(res) == 2: # No custom output added
            label, profit = res
            customOut = None
        elif len(res) == 3: # Custom output added
            label, profit, customOut = res 
            
        nnInputs.append(inputs)
        nnLabels.append(label)
        nnProfit.append(profit)
        nnDTM.append(dtm[i-1])
        nnOp.append(op[i-1])
        nnRateIndexes.append(i-1)
        if customOut is not None:
            nnCustomOut.append(customOut)
    if len(nnInputs) == 0:
        return retErr
    if len(nnLabels) == 0:
        return retErr
        
    nnInputs = np.array(nnInputs, dtype='float')
    nnRateIndexes = np.array(nnRateIndexes, dtype='int')
    numSamples, numFeatures = np.shape(nnInputs)
    nnLabels = np.array(nnLabels, dtype='float')
    shape = np.shape(nnLabels)
    if len(shape) == 2: # One Hot
        numLabels = shape[1]
    else:
        numLabels = int(np.max(nnLabels) + 1)       
    nnProfit = np.array(nnProfit, dtype='float')      
    nnMean = np.zeros(shape=[numFeatures], dtype='float')
    nnStd = np.zeros(shape=[numFeatures], dtype='float')
    
    if detachTest is not None:
        detachStart = int(float(numSamples) * detachTest / 100.0)
        
    if normalize: # If normalization is required
        normIntervalStart = 0
        if detachTest is not None:
            normIntervalStart = detachStart
            
        for i in range(numFeatures):
            status, mean, std = taft.normalize(nnInputs[:,i], normInterval=[normIntervalStart,numSamples])
            if status is None:
                logMessage += "Can't normalize %d column\n." % (i)
                return retErr
            nnMean[i] = mean
            nnStd[i] = std
    else:
        logMessage += "Normalization skipped.\n"
        nnMean = None
        nnStd = None
        
    if detachTest is None:
        retval1 = {'inputs': nnInputs, 'labels': nnLabels, 'profit': nnProfit, 
        'dtm':nnDTM, 'op':nnOp, 'customOut':nnCustomOut, 'numSamples':numSamples, 
        'numFeatures':numFeatures, 'numLabels':numLabels, 'mean':nnMean, 
        'std':nnStd, 'rateIndexes':nnRateIndexes}    
        retval2 = None
    else:
        retval1 = {'inputs': nnInputs[detachStart:], 'labels': nnLabels[detachStart:], 
        'profit': nnProfit[detachStart:], 'customOut':nnCustomOut[detachStart:], 
        'rateIndexes':nnRateIndexes[detachStart:], 'numSamples':numSamples-detachStart, 
        'numFeatures':numFeatures, 'numLabels':numLabels, 'mean':nnMean, 
        'std':nnStd, 'dtm':nnDTM[detachStart:], 'op':nnOp[detachStart:]}    
        retval2 = {'inputs': nnInputs[:detachStart], 'labels': nnLabels[:detachStart], 
        'profit': nnProfit[:detachStart], 'customOut':nnCustomOut[:detachStart], 
        'rateIndexes':nnRateIndexes[:detachStart], 'numSamples':detachStart, 
        'numFeatures':numFeatures, 'numLabels':numLabels, 'mean':nnMean, 
        'std':nnStd, 'dtm':nnDTM[:detachStart], 'op':nnOp[:detachStart]}    

    return(retval1, retval2)
# end of def prepareData

#
def countLabels(labels):
    shape = np.shape(labels)
    if len(shape) == 2: # One-hot
        rows, cols = shape
        labelsCounter = np.zeros(shape=[cols])
        for i in range(rows):
            for j in range(cols):
                if labels[i][j] == 1:
                    labelsCounter[j] += 1
        return labelsCounter
    else: # Not one-hot
        rows = shape[0]
        maxLabel = int(np.max(labels))
        labelsCounter = []
        for i in range(maxLabel+1):
            labelsCounter.append(0)
        for i in range(rows):
            labelsCounter[ int(labels[i]) ] += 1
        return labelsCounter
# end of def

'''
def normalize(x, meanX=None, stdX=None, normInterval=[0,-1]):
    if meanX is None:
        if normInterval[1] == -1:
            meanX = np.mean(x)
        else:
            meanX = np.mean(x[ normInterval[0]:normInterval[1] ])            
    if stdX is None:
        if normInterval[1] == -1:
            stdX = np.std(x)
        else:
            stdX = np.std(x[ normInterval[0]:normInterval[1] ])            
    if not(stdX > 0.0):
        return None, None, None
    lenX = len(x) 
    for i in range(lenX):
        x[i] = (x[i] - meanX) / stdX
    return lenX, meanX, stdX
# end of normalize
'''

def normalize(x, meanX=None, stdX=None, normInterval=[0,-1]):
        lenX = len(x)
        if lenX == 0:
                return None, None, None
        if meanX is None:
                if normInterval[1] == -1:
                        meanX = np.mean(x)
                else:
                        meanX = np.mean(x[ normInterval[0]:normInterval[1] ])
        if stdX is None:
                if normInterval[1] == -1:
                        stdX = np.std(x)
                else:
                        stdX = np.std(x[ normInterval[0]:normInterval[1] ])
        if not(stdX > 0.0):
                return None, None, None
        else:
                for i in range(lenX):
                        x[i] = (x[i] - meanX) / stdX
        return lenX, meanX, stdX
# end of normalize


def SaveModel(FileName, model, calcInp, calcInpParams):    
    global logMessage
    ok = True

    logMessage = ""
    logMessage += "Saving into \"%s\"...\n" % (FileName)
    
    '''
    try:
        FileHandle = open(fileName, 'wb')
    except Exception:
        ok = False
    if ok:
        try:
            dill.dump({"model": model, "calcInp": calcInp, "calcInpParams":calcInpParams}, fileHandle, 2)
        except Exception:
            ok = False
        finally:
            fileHandle.close()
    '''
    
    data = {"model": model, "calcInp": calcInp, "calcInpParams": calcInpParams}
    with open(FileName, "wb") as FileHandler:
        dill.dump(data, FileHandler, 2)

    return ok
# end of SaveModel()


def LoadModel(FileName):
    global logMessage
    ok = True

    logMessage = ""
    logMessage += "Reading data from \"%s\"...\n" % (FileName)
    
    with open(FileName, "rb") as FileHandler:
        LoadObject = dill.load(FileHandler)

    """
    try:
        fileHandle = open(fileName, 'rb')
    except Exception:
        ok = False
        logMessage += "Can't open file %s.\n" % (fileName)

    if ok:
        try:
            loadObject = dill.load(fileHandle)
        except Exception:
            ok = False
            logMessage += "Error reading the data.\n"
        finally:
            fileHandle.close()
    
    if not ok:
        return None
    """
    return {'model':loadObject['model'], 'calc':loadObject['calcInp'], 
    'params':loadObject['calcInpParams']}
# end of LabelingoadModel()


def precalcFutureReturn(rates, params):
    if not 'numLabels' in params:
        params['numLabels'] = 3
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
    sortedDiffs = np.sort(diffs)

    ret = {}
    for i in range(numLabels-1):
        index = int((i+1) * float(lenDiffs) / float(numLabels) + 0.5)
        ret['splitter' + str(i)] = sortedDiffs[index]

    mean = np.mean(diffs)
    std = np.std(diffs)
    ret['mean'] = mean
    ret['std'] = std
    meanAbs = np.mean(np.abs(diffs))
    stdAbs = np.std(np.abs(diffs))
    ret['meanAbs'] = meanAbs
    ret['stdAbs'] = stdAbs

    return ret
# end of def


def calcFutureReturn(rates, params):
    numLabels = params['numLabels']
    lookAhead = params['lookAhead']-1

    if lookAhead >= len(rates['cl']):
        return None

    profit = rates['cl'][lookAhead] - rates['op'][0]
    isLabel = False
    for i in range(numLabels-1):
        if profit < params['precalculated']['splitter'+str(i)]:
            label=i
            isLabel = True
            break
    if not isLabel:
        label = numLabels-1

    return label, profit
# end of def



def calcFutureNHNL(rates, params):
    numLabels = params['numLabels']
    lookAhead = params['lookAhead']

    if lookAhead >= len(rates['cl']) or lookAhead < 2:
        return None

    # Calcualting NH/NL ratio
    hi = rates['hi'][:lookAhead]
    lo = rates['lo'][:lookAhead]
    v1 = taft.pNextHigher(lookAhead, hi[::-1])
    v2 = taft.pNextLower(lookAhead, lo[::-1])
    if v1 is None or v2 is None:
        return None

    vSum = v1 + v2
    if not(vSum > 0):
        ratio = 0.0
    else:
        ratio = (v1-v2) / vSum

    # Getting the scale to label the ratio value
    if not 'lookAheadScale' in params:
        scale = calcScale(numLabels)
        params['lookAheadScale'] = scale
    else:
        scale = params['lookAheadScale']

    # Labeling the ratio value 
    label = -1
    for l in range(numLabels-1):
        if ratio < scale[l]:
            label=l
            break
    if label == -1:
        label = numLabels-1

    profit = rates['cl'][lookAhead-1] - rates['op'][0]

    return label, profit
# end of def


def calcPastLogOfReturns(pastRates, params):
    inputs = []

    lenRates = len(pastRates['cl'])
    for l in range(len(params['lookBack'])):
        lookBack = params['lookBack'][l]
        if lookBack >= lenRates:
            return None

        bDone = False
        if 'lookBackLogOfReturns' in params: 
            if params['lookBackLogOfReturns'] == 'hl':
                ind = np.log(pastRates['cl'][0] / pastRates['hi'][lookBack]) 
                inputs.append(ind)

                ind = np.log(pastRates['cl'][0] / pastRates['lo'][lookBack]) 
                inputs.append(ind)
                bDone = True
        if not bDone:
            ind = np.log(pastRates['cl'][0] / pastRates['cl'][lookBack]) 
            inputs.append(ind)

    return inputs
# end of def


def calcPastSTOs(pastRates, params):
    inputs = []

    for p in range(len(params['lookBack'])):
        period = params['lookBack'][p] 

        ret = taft.stochastic(periodK=period, hi=pastRates['hi'], lo=pastRates['lo'], cl=pastRates['cl'])
        if ret is None:
            return None
        ind = ret['K']
        inputs.append(ind/100.0)

    return inputs
# end of def


def calcPastNHNLs(pastRates, params):
    inputs = []

    for p in range(len(params['lookBack'])):
        period = params['lookBack'][p] 

        ind = taft.pNextHigher(period, pastRates['hi'])
        if ind == None:
            return None
        inputs.append(ind)

        ind = taft.pNextLower(period, pastRates['lo'])
        if ind == None:
            return None
        inputs.append(ind)

    return inputs
# end of def


def calcPastROCs(pastRates, params):
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
    while(curStep < stepMax):

        if period == step0:
            ind = taft.roc(period=period, rates=pastRates['cl'])
            if ind == None:
                return None
            inputs.append(ind/100.0)

        ind = taft.roc(period=period, rates=pastRates['hi'])
        if ind == None:
            return None
        inputs.append(ind/100.0)

        ind = taft.roc(period=period, rates=pastRates['lo'])
        if ind == None:
            return None
        inputs.append(ind/100.0)

        period += stepSize + stepSizeInc*curStep
        curStep += 1

    return inputs
# end of def


def calcScale(numLabels):
    scale = []
    splitter = 2.0 / float(numLabels)
    for i in range(1,numLabels):
        scale.append(-1.0 + splitter*float(i))
    return scale
# end of def


# Simulates trade
def simulateTrade(shift=0, hi=None, lo=None, tp=None, sl=None, tpSlides=False, slSlides=False, side=1, price=None, type=0):
    profit = None
    closedAt = -1    
    
    (hi, lo) = _defineRates(hi=hi, lo=lo)
    if hi is None or lo is None:
        return None

    hiMax = np.max(hi)
    loMin = np.min(lo)
    if tp is None:
        tp = (hiMax - loMin)*100.0
    if sl is None:
        sl = (hiMax - loMin)*100.0

    if price is None:
        price = lo[shift] + (hi[shift] - lo[shift]) / 2.0

    hiLessLo = np.subtract(hi, lo)
    hiLessLoMean = np.mean(hiLessLo)

    closePrice = None

    if side == 1:
        tpPrice = price + tp
        slPrice = price - sl
    else:
        tpPrice = price - tp 
        slPrice = price + sl

    for i in range(shift, -1, -1):
        if side == 1:
            if hi[i] >= tpPrice:
                profit = tpPrice - price
                closedAt = i
                closePrice = tpPrice
                break
            if lo[i] <= slPrice:
                profit = slPrice - price
                closedAt = i
                closePrice = slPrice
                break
            if tpSlides == True:
                if lo[i] + tp < tpPrice:
                    tpPrice = lo[i] + tp
            if slSlides:
                if hi[i] - sl > slPrice:
                    slPrice = hi[i] - sl
        else:
            if hi[i] >= slPrice:
                profit = price - slPrice
                closedAt = i
                closePrice = slPrice                
                break
            if lo[i] <= tpPrice:
                profit = price - tpPrice
                closedAt = i
                closePrice = tpPrice                
                break
            if tpSlides:
                if hi[i] - tp > tpPrice:
                    tpPrice = hi[i] - tp
            if slSlides:
                if lo[i] + sl < slPrice:
                    slPrice = lo[i] + sl
                    
    return {'profit': profit, 'closedAt':closedAt, 'closePrice':closePrice}
# end of simulateTrade



'''
def readFile(fileName):
    return readFinam(fileName)


def readFinam(fileName):
    readError = False
    fileOpened = False
    
    linesRead = 0
    linesSkipped = 0

    from datetime import datetime 

    op = []
    hi = []
    lo = []
    cl = []
    vol = []
    dtm = []

    try:
        fileHandle = open(fileName, "r")
        fileOpened = True

        firstLine = True
        for line in fileHandle:

            if firstLine:
                firstLine = False
                linesSkipped += 1
                continue

            lineSplitted = line.split(",")
            if len(lineSplitted) < 9:
                linesSkipped += 1
                continue

            strDate = lineSplitted[2]
            strTime = lineSplitted[3]
            dtm.append(datetime.strptime(strDate + " " + strTime, '%Y%m%d %H%M%S'))

            op.append(float(lineSplitted[4]))
            hi.append(float(lineSplitted[5]))
            lo.append(float(lineSplitted[6]))
            cl.append(float(lineSplitted[7]))
            vol.append(float(lineSplitted[8].rstrip()))

            linesRead += 1    
    except IOError:
                readError = True
    
    if fileOpened:
        fileHandle.close()

    if readError:
        return(None)

    op = np.array(op[::-1], dtype='float')
    hi = np.array(hi[::-1], dtype='float')
    lo = np.array(lo[::-1], dtype='float')
    cl = np.array(cl[::-1], dtype='float')
    vol = np.array(vol[::-1], dtype='float')
    dtm = dtm[::-1]

    return {'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'dtm':dtm, 'length':linesRead, 'skipped':linesSkipped}
# end of readFinam
'''

# 
def _defineRates( op=[], hi=[], lo=[], cl=[], vo=[] ):
    global _open
    global _high
    global _low
    global _close
    global _volumes

    ret = ()
    if op is None:
        op = _open
        ret = ret + (op,)
    elif len(op) > 0:
        ret = ret + (op,)
    if hi is None:
        hi = _high
        ret = ret + (hi,)
    elif len(hi):
        ret = ret + (hi,)
    if lo is None:
        lo = _low
        ret = ret + (lo,)
    elif len(lo) > 0:
        ret = ret + (lo,)
    if cl is None:
        cl = _close
        ret = ret + (cl,)
    elif len(cl) > 0:
        ret = ret + (cl,)
    if vo is None:
        vo = _volumes
        ret = ret + (vo,)
    elif len(vo) > 0:
        ret = ret + (vo,)
    return ret
# end of _defineRates

_open = None
_close = None
_high = None
_low = None
_volumes = None