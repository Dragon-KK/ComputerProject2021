from ...DataTypes.UI import Interval, EventListener

class InputManager:
    '''Scuffed'''
    def __init__(self, canvas,paddle, keyHoldDelay = 20, keybinds = {
        'w' : '+',
        's' : '-',
        'Up' : '+',
        'Down' : '-'    
    }):
        self.Window = canvas.Window
        self.Canvas = canvas
        self.KeyBinds = keybinds
        self.Paddle = paddle

        self.__PressedKeys = set()
        self.__KeyEventListener = EventListener("!Key", self.OnKey)
        self.__KeyCallbackInterval = Interval(keyHoldDelay, self.OnInterval)

    def OnKey(self, event):
        e = event.Args[0]
        t = str(e.type)
        if t == "KeyPress" or t=="2":
            if e.keysym in self.KeyBinds:
                self.__PressedKeys.add(e.keysym)
        elif t == "KeyRelease" or t=="3":
            if e.keysym in self.__PressedKeys:
                self.__PressedKeys.remove(e.keysym)

    def OnInterval(self):
        for i in self.__PressedKeys:
            if self.KeyBinds[i] == "+":
                self.Paddle.Position -= self.Paddle.PaddleVelocity
            elif self.KeyBinds[i] == "-":
                self.Paddle.Position += self.Paddle.PaddleVelocity

    def Pause(self):
        self.Canvas.EventListeners -= self.__KeyEventListener
        self.Window.Intervals -= self.__KeyCallbackInterval
        self.__PressedKeys.clear()

    def Continue(self):
        self.Canvas.EventListeners += self.__KeyEventListener
        self.Window.Intervals += self.__KeyCallbackInterval