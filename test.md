TAFT Tests: the "test.py" Module
============================
version 1.0.*		
  
Related documents: [TAFT readme](README.md), [ti.py](ti.md) module, [data.py](data.md) module, [test.py](test.md) module, [rates](rates.md) data structure.		

> **Important notice**:
> Nothing important yet... :)   

** Contents **		
[regressionModelProfit](#regressionModelProfit)	
[regressionModelTest](#regressionModelTest)	
[displayPlots](#displayPlots)	
[simulateTrade](#simulateTrade)	

<a name="regressionModelProfit"></a>
### regressionModelProfit ###
~~~
def regressionModelProfit( model, data, title="", entryFunction=None, 
	entryFunctionParams=None, flipOver=False,
	verbose=False, plot=False, plotsCombined=False, useTPSL=False, rates=None )
~~~
Tests trained regression model for performance and profit.	
>	 
**model** (object) - a regression model tested (e.g. MLPRegression, SVR etc);	
**data** (dictionary) -  used to feed the model with train and test data; such a dictionary can be obtained with the [prepareData](data.md) function; 	
**entryFunction** (function) - during simulation this function is used to make a decision whether a trade should be made or not. Returns a tuple that consists of three values: 1) an integer that denotes the side of a trade to perform ('-1' - short, '0' - no trade, '1' - long), 2) the take profit, 3) the stop loss. Alternatively the function may return a single integer value that stands for the side of a trade to perform. The take profit and stop loss would be assigned with the value of the profit predicted by the model (data['profit'][i]).		
**entryFunctionParams** (dictionary) - a set of parameters you may pass into your **entryFunction**.	
**flipOver** (boolean) - True value simulates a so-called "flip-over trading" when any trade is closed only when the opposite signal is received, at that the signal not only closes the trade but also opens another one in the opposite side.			
**verbose** (boolean) - If **true** the function outputs log messages into the terminal screen.	
**plot** (boolean) - If **true** the function value plots cumulative profit curve (PnL).	  
**plotsCombined** (boolean) - If **true** the function creates cumulative profit curve (PnL) but doesn't show it waiting for more models to be tested and the plots displayed simultaneously. You must call the [displayPlots()](#displayPlots) function later to show all the plots created.		
**useTPSL** (boolean) - if **true** the function simulates each trade usign take profit and stop loss, if **false** the function uses data['profit'] array to determine profit for each trade.		
**rates** (dictionary) - a [rates](rates.md) dictionary. It must be specified only if **useTPSL** is **true**.

Returns a dictionary of the following structure:		
>				
'numTrades' (integer) - the number of trades made.		
'meanZ' (double) - the mean of model predictions (the data['profit'] array).	
'stdZ' (double) - the standard deviation of the model predictions (the data['profit'] array).	
'cumulativeProfit' - an array that stores cumulative profit after each trade (the PnL curve).	
'overallProfit' (double) - the profit gained during simulation.	

<a name="regressionModelTest"></a>
### regressionModelTest ###

def regressionModelTest( model, data, trainHistory=100, repeatTrainAfter=10, title="", 
	entryFunction=None, entryFunctionParams=None, normalize=False, flipOver=False, verbose=False, plot=False, plotsCombined=False, 
	useTPSL=False, rates=None )
>				
**model** (object) - a regression model tested (e.g. MLPRegression, SVR etc);	
**data** (dictionary) -  used to feed the model with train and test data; such a dictionary can be obtained with the [prepareData](data.md) function; 	
**entryFunction** (function) - during simulation this function is used to make a decision whether a trade should be made or not. Returns a tuple that consists of three values: 1) an integer that denotes the side of a trade to perform ('-1' - short, '0' - no trade, '1' - long), 2) the take profit, 3) the stop loss. Alternatively the function may return a single integer value that stands for the side of a trade to perform. The take profit and stop loss would be assigned with the value of the profit predicted by the model (data['profit'][i]).		
**entryFunctionParams** (dictionary) - a set of parameters you may pass into your **entryFunction**.	
**normalize** (boolean) - True value makes the function normalize inputs before feeding into the model.
**flipOver** (boolean) - True value simulates a so-called "flip-over trading" when any trade is closed only when the opposite signal is received, at that the signal not only closes the trade but also opens another one in the opposite side.			
**verbose** (boolean) - If **true** the function outputs log messages into the terminal screen.	
**plot** (boolean) - If **true** the function value plots cumulative profit curve (PnL).	  
**plotsCombined** (boolean) - If **true** the function creates cumulative profit curve (PnL) but doesn't show it waiting for more models to be tested and the plots displayed simultaneously. You must call the [displayPlots()](#displayPlots) function later to show all the plots created.		
**useTPSL** (boolean) - if **true** the function simulates each trade usign take profit and stop loss, if **false** the function uses data['profit'] array to determine profit for each trade. 		
**rates** (dictionary) - a [rates](rates.md) dictionary. It must be specified only if **useTPSL** is **true**.

<a name="displayPlots"></a>
### displayPlots ###
~~~
def displayPlots( title = None )
~~~
Displays plots created by the [regressionModelProfit()](#regressionModelProfit) or [regressionModelTest()](#regressionModelTest) functions.		
> **title** (string, optional) - A title for the plot displayed.  		

<a name="simulateTrade"></a>
### simulateTrade ###
 simulateTrade( rateIndex, rates, takeProfit, stopLoss, dir )
