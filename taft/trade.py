from limits import singlePositionLimit
global singlePositionLimit

class Trade:
    def __init__(self, price, volume, side):
        self._price = price
        self._volume = volume
        self._side = side
        
    @property
    def price(self, price):
        return self._price
        
    @price.setter
    def price(self, value):
        raise RuntimeError("Open price cannot be changed!")
        
    @price.deleter
    def price(self):
        raise RuntimeError("Open price cannot be deleted! Close position\
        properly")
    
    @property
    def volume(self):
        return self._volume
        
    @volume.setter
    def volume(self, value):
        if value > singlePositionValue or value < -singlePositionValue:
            raise ValueError("Cannot open position with {:d} lots!\
            Maximum number of lots for a single position is {:d}".format(
                value, singlePositionLimit))
        else:
            self._value = value
            
    @volume.deleter
    def volume(self):
        raise RuntimeError("Close position properly!")
        
    @property
    def side(self):
        return self._side
        
    @side.setter
    def side(self, value):
        raise RuntimeError("Side cannot be changed!")
        
    @side.deleter
    def side(self):
        raise RuntimeError("Side cannot be deleted!")