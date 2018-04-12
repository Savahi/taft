import taft.ti
import taft.data

# AD
rates = taft.data.load( "data/ad.txt" )
lenRates = len( rates['cl'] )

output = "**** AD\n"
v = None
for i in range( lenRates-1, -1, -1 ):
	v = taft.ti.ad( period=1, hi=rates['hi'][i:], lo=rates['lo'][i:], cl=rates['cl'][i:], vol=rates['vol'][i:], prev=v )
	output += str(v) + "  "
print output

# ADX
rates = taft.data.load( "data/adx2.txt" )
lenRates = len( rates['cl'] )

output = "**** ADX:\n"
v = None
for i in range( lenRates-1, -1, -1 ):
	v = taft.ti.adx( period=14, hi=rates['hi'][i:], lo=rates['lo'][i:], cl=rates['cl'][i:], prev=v )
	if v is None:
		continue
	output += str(v) + "\n"
print output

# Aroon
rates = taft.data.load( "data/aroon.txt" )
lenRates = len( rates['cl'] )

output = "**** Aroon:\n"
v = None
for i in range( lenRates-1, -1, -1 ):
	v = taft.ti.aroon( period=5, rates=rates['cl'][i:] )
	if v is None:
		continue
	output += str(v) + "\n"
print output

# ATR
rates = taft.data.load( "data/atr.txt" )
lenRates = len( rates['cl'] )

output = "**** atr:\n"
v = None
for i in range( lenRates-1, -1, -1 ):
	v = taft.ti.atr( period=3, hi=rates['hi'][i:], lo=rates['lo'][i:], cl=rates['cl'][i:] )
	if v is None:
		continue
	output += str(v) + "\n"
print output

# Bollinger
rates = taft.data.load( "data/bollinger.txt" )
lenRates = len( rates['cl'] )

output = "**** bollinger:\n"
v = None
for i in range( lenRates-1, -1, -1 ):
	v = taft.ti.bollinger( period=8, rates=rates['cl'][i:] )
	if v is None:
		continue
	output += str(v) + "\n"
print output

# EMA
rates = taft.data.load( "data/ema2.txt" )
lenRates = len( rates['cl'] )

output = "**** ema:\n"
v = None
for i in range( lenRates-1, -1, -1 ):
	v = taft.ti.ema( period=3, rates=rates['cl'][i:], prev=v )
	if v is None:
		continue
	output += str(v) + "\n"
print output

# MACD
rates = taft.data.load( "data/macd.txt" )
lenRates = len( rates['cl'] )

output = "**** macd:\n"
v = None
for i in range( lenRates-1, -1, -1 ):
	v = taft.ti.macd( periodFast=2, periodSlow=3, periodSignal=3, rates=rates['cl'][i:], prev=v )
	if v is None:
		continue
	output += str(v) + "\n"
print output


# Stochastic
rates = taft.data.load( "data/stochastic.txt" )
lenRates = len( rates['cl'] )

output = "**** stochastic:\n"
v = None
for i in range( lenRates-1, -1, -1 ):
	v = taft.ti.stochastic( period=7, periodD=3, hi=rates['hi'][i:], lo=rates['lo'][i:], cl=rates['cl'][i:] )
	if v is None:
		continue
	output += str(v) + "\n"
print output

