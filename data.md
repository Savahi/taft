TAFT Data Handling: the "data.py" Module
============================
version 1.0.*		

Related documents: [TAFT readme](README.md), [ti.py](ti.md) module, [data.py](data.md) module, [test.py](test.md) module, [rates](rates.md) data structure.		

> **Important notice**:
> Nothing important yet... :)   

<a name="prepareData"></a>
### prepareData ###
def prepareData( rates, calcInp, calcInpParams, calcOut, calcOutParams, normalize=False, detachTest=20, precalcData=None )
>		
**rates** 
**calcInp**
**calcInpParams**
**calcOut**
**calcOutParams**
**normalize**
**detachTest** 
**precalcData** 


Rates loading
-------------

### loadDaily ###
~~~
loadDaily( ticker, 
	startYear=None, endYear=None, 
	startMonth=None, endMonth=None, 
	startDay=None, endDay=None )
~~~
	tickerName (string) - the name of the ticker.   
		Can be one of the following: BTCUSD, LTCUSD, EURUSD
	startYear, endYear, startMonth, endMonth, startDay, endDay (int) - specify the time window 
		for the quotes to be loaded. 
	Returns None if fails and a 'rates' data structure if succeeds.

See the description of the ['rates'](rates.md) data structure [here](rates.md).  
