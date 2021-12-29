from ..Elements import label
from ...Core.DataTypes.UI import Interval,EventListener

class TimedContinueButton(label):

    def __init__(self, *args,countdown = 5,onfinish = lambda:0,text="Begin", ResizeCorrectionConst = 2.8,**kwargs):
        super().__init__(*args, **kwargs, text=text)
        self.Countdown = 5
        self._BeginningText = text
        self._BeginningResizeCorrectionConst = ResizeCorrectionConst
        self.__Counter = 0
        self.OnCountdownFinish = onfinish
        self.__CountdownInterval = Interval(1000, self.Callback)
        self.StartedCountdown = False
        self.EventListeners += EventListener("<Button-1>", lambda *args,**kwargs:self.StartCountdown())

    def StartCountdown(self):
        if self.StartedCountdown:return
        self.State += "Active"
        self.Window.Intervals += self.__CountdownInterval
        self.Text = str(self.Countdown)
        self.StartedCountdown = True
        self.ResizeCorrectionConst = 2

    def Callback(self):
        self.__Counter += 1

        self.Text = str(self.Countdown - self.__Counter)

        if self.__Counter >= self.Countdown:
            self.Window.Intervals -= self.__CountdownInterval
            self.State -= "Active"
            self.OnCountdownFinish()

    def Reset(self):
        self.__Counter = 0
        self.StartedCountdown = False
        self.Text = self._BeginningText
        self.ResizeCorrectionConst = self._BeginningResizeCorrectionConst

    