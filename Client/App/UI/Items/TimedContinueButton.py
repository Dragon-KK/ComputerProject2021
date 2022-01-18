from ..Elements import img, label
from ...Core.DataTypes.UI import EventListener, Interval

class TimedContinueButton:
    def __init__(
        self,
        parent, # The element that containsthe component
        callback, # The function that is called on countdown end
        initialImage, # The image that is shown initially   

        countdownStart = 5, # The amount of time the countdown is set for (in seconds)
        imgName = ".countdownImage", # The name of the img element
        labelName = ".countdownLabel", # The name of the label
        customCountdownStart = False
    ):
        self.ImageElement = img(initialImage, classes = imgName)
        self.__labelName = labelName

        self.ParentElement = parent

        self.OnCountdownEnd = callback

        self.__Counter = 0
        self.Countdown = countdownStart

        self.__CountdownInterval = Interval(1000, self.__OnCountDownTick)

        if not customCountdownStart:self.ImageElement.EventListeners += EventListener("<Button-1>", lambda e : self.StartCountDown())
        
        self.ParentElement.Children += self.ImageElement

    def __OnCountdownEnd(self):
        self.ParentElement.Window.Intervals -= self.__CountdownInterval
        self.LabelElement.Remove()
        self.OnCountdownEnd()

    def __OnCountDownTick(self):
        self.__Counter += 1
        if self.__Counter >= self.Countdown:
            self.__OnCountdownEnd()
            return
        self.LabelElement.Text = str(self.Countdown - self.__Counter)

    def Reset(self):
        self.__Counter = 0
        self.ImageElement.State += 'Visible'


    def StartCountDown(self):
        self.ImageElement.State -= 'Visible'
        self.LabelElement = label(classes = self.__labelName, text=str(self.Countdown))
        self.ParentElement.Children += self.LabelElement

        self.ParentElement.Window.Intervals += self.__CountdownInterval

