TAFT Sample Data Load Module
============================
version 1.0.7
  
Related documents: [TAFT library](README.md), ['rates' data structure]   

> **Important notice**:
> Nothing important yet... :)   

Loading data
------------

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
