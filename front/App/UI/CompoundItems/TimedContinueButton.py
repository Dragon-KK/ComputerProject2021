from ..Elements import img, label
from ...Core.DataTypes.UI import EventListener, Interval

class TimedContinueButton:
    def __init__(
        self,
        callback, # The function that is called on countdown end
        initialImage, # The image that is shown initially   

        countdownStart = 5, # The amount of time the countdown is set for (in seconds)
        imgName = ".countdownImage",
        labelName = ".countdownLabel"
    ):
        self.ImageElement = img(initialImage, name = imgName)
        self.labelName = label(name=labelName, text=str(countdownStart))

    def __OnCountdownEnd(self):
        pass

    def Reset(self):
        pass

    def StartCountDown(self):
        pass