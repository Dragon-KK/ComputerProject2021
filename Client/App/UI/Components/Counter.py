from ..Elements import label
from ...Core.DataTypes.UI import Interval

class Counter(label):
    '''
    AspectRatioPreservedDiv will try to fill its parent as much as it can while preserving aspect ratio
    Aspect ratio = width/height
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.Counter = 0
        self.__CounterInterval = Interval(1000, self.__OnInterval)

    def __OnInterval(self):
        self.Counter += 1
        self.Text = str(self.Counter)

    def Continue(self):
        self.Window.Intervals += self.__CounterInterval

    def Pause(self):
        self.Window.Intervals -= self.__CounterInterval

    def Reset(self):
        self.Counter = 0
        self.Text = str(0)


        


