TAFT Data Handling: the "data.py" Module
============================
version 1.0.*		

Related documents: [TAFT readme](README.md), [ti.py](ti.md) module, [data.py](data.md) module, [test.py](test.md) module, [rates](rates.md) data structure.		

> **Important notice**:
> Nothing important yet... :)   

** Contents **		
[loadDaily](#loaddaily)	
[prepareData](#preparedata)	
[countLabels](#countlabels)	
[normalize](#normalize)	
[saveModel](#savemodel)	
[loadModel](#loadmodel)	

<a name="ratesloadingfunctions"></a>
Rates loading
-------------

<a name="loaddaily"></a>
### loadDaily ###
```python
def loadDaily( ticker, startYear=None, endYear=None, 
	startMonth=None, endMonth=None, startDay=None, endDay=None )
```
Loads sample rate data (say, to pass it later into the [prepareData](#preparedata) function and then use for training and testing an ML model).
>**tickerName** (string) - the name of the ticker. Can be one of the following: AUDUSD, Brent, BTCUSD, ETHUSD, EURUSD, GBPUSD, LTCUSD, NaturalGas, NZDUSD, SINUSOID, WTI.    
>**startYear**, **endYear**, **startMonth**, **endMonth**, **startDay**, **endDay** (integers) - specify a time window for quotes loaded. 

Returns None if fails or data presented in the form of a [rates](rates.md) data structure if succeeds.


<a name="preparedata"></a>
### prepareData ###
```python
def prepareData( rates, calcInp, calcInpParams, calcOut, calcOutParams, 
	normalize=False, detachTest=20, precalcData=None )
```
Prepares "raw" for feeding into an ML model, e.g. calculates inputs and outputs, performs normalization etc.	 
> **rates** (dictionary) - "raw" rates presented in the from of a [rates](rates.md) data structure. Usually rates are loaded by one of the [rates loading functions](#ratesloadingfunctions).    
> **calcInp** (function, optional) - A user defined function used to calculate inputs for each sample. If "None" the default one is used.    
> **calcInpParams** (dictionary, optional) - A set of user-defined parameters presented as a python dictionary used to pass additional parameters into the **calcInp** function.    
> **calcOut** (function, optional) - A user defined function used to calculate **output** for each **input**.     
**calcOutParams** (dictionary, optional) - A set of user-defined parameters presented as a python dictionary used to pass additional parameters into the **calcOut** function.    
> **normalize** (boolean, optional) - **True** value makes the function normalize inputs before feeding into the model.    
> **detachTest** (integer, optional) - Specifies how many samples (in %) must be used as test ones.    
> **precalcData** (function, optional) - A user-defined function used to make preliminary calculations before calculating inputs and outputs.    				

Returns two dictionary variables, the first one stores train data while the other one stores test data. If **detachTest** is **None** the second returned variable is **None** too. Each of the dictionary variables has the following structure:			
>**'numSamples'** (integer) - the number of samples to train or test the model with (equals to the size of the 'inputs' array alogn the '0' axis).	
>**'numFeatures'** (integer) - the number of features (equals the size of the 'inputs' array along the '1' axis).		
>**'numLabels'** (integer) - the number of classes the model can recognize. **Important notice!** Short trades must be encoded with '0' which is the smallest allowed value of an item in the array, while long ones must be encoded with the biggest allowed value of the array which is determined by the number of classes.		  
>**'inputs'** (numpy array, np.float) - inputs to train or test the model. The size of the array is 'numSamples'X'NumFeatures'.
>**'labels'** (numpy array, np.float) - outputs or class identifiers. i.e. the correct answers of the model to train or test with. The size of the array is 'numSamples'.		
>**'profit'** (numpy array, np.float, size='numSampl') - gains or losses in points of trades simulated. For short trades gains must be negative while loss must be positive. The size of the array is 'numSamples'.		
>**'mean'** (numpy array, np.float) - for each feature stores the mean value (used to normalize the values of the feature). The size of the array is 'numFeatures'.		 
>**'std'** (numpy array, np.float) - for each feature stores the standard deviation (used to normalize the values of the feature). The size of the array is 'numFeatures'.		


<a name="countlabels"></a>
### countLabels ###
```python
def countLabels( labels ):
```
Counts number of samples for each class.		 
>**labels** (np.array) - an array that stores class indetifier for each sample. The array is returned by the [prepareData](#preparedata) function (the 'labels' element of the dictionary returned).		

Returns an array where each item stores the number of samples for the corresponding class. 


<a name="normalize"></a>
### normalize ###
```python
def normalize( x, meanX=None, stdX=None, normInterval=[0,-1] ):
```
Performs normalization of a specified data array.
>**x** (np.array) - source data to be normalized.    
>**meanX** (float) - the mean used to normalize data. If **None** is passed, the function calculates it.    
>**stdX** (float) - the standard deviation used to normalize data. If **None** is passed, the function calculates it.    
>**normInterval** (array, integer) - a 2-item array specifies which part (sub-array) of the **x** array should be used to calculate **meanX** and **stdX**. The first item stands for the beginning of the sub-array and the second one stands for it's end. If "None" is passed the whole array is used.    


<a name="savemodel"></a>
### saveModel ###
```python
def saveModel( fileName, model, calcInp, calcInpParams ):	
```
Saves a trained ML model for future use.    	
>**fileName** (string) - destination file.    
>**model** (object) - the model to be saved.    
>**calcInp** (function) - the function earlier used with the [prepareData](#preparedata) function to calculate "inputs".    
>**calcInpParams** (function) - a set of parameters for the **calcInp** function.


<a name="loadmodel"></a>
### loadModel ###
```python
def loadModel( fileName ):
```
Loads a model previously saved with the [saveModel](savemodel) function.    
>**fileName** (string) - source file.    

Returns a dictionary of the following structure:    
>**'model'** - the model.    
>**'calcInp'** - the function to calculate "inputs".
>**'calcInpParams'** - a set of parameters for the **calcInp** function.
