from ....Core.DataTypes.UI import EventListener, Interval
from ....Core.Engine.Pong import ArcadePong
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.CompoundItems import TimedContinueButton
from ....UI.Components import AspectRatioPreservedContainer,Counter
from ....UI.Elements import *
from ....Core.DataTypes.Game import GameSettings

'''
Arcade is basically going to be how long you can survive
There will be a timer on the top where you can see how good you are doing
'''

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/Arcade/Game"
    StyleSheet = "Styles/Arcade/Game.json"
    ResourceKey = "Arcade"

    def Destroy(self):
        super().Destroy()
        self.Pong.PauseRound()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = GameSettings.FromJson(self.Window.Resources.Storage.Arcade['GameSettings'])

        self.config(bg="black") # Let the background be black

        # Container (since we want our page to preserve aspect ratio)
        Container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)        
        self.Children += Container
       
        # region Toolbar
        Toolbar = div(name=".toolbar")
        Container.Children += Toolbar

        GoBackButton = img(self.Window.Resources.Images.Arcade.Home, name = ".goHome")
        GoBackButton.EventListeners += EventListener("<Button-1>", lambda *args,**kwargs:GoHome())
        Toolbar.Children += GoBackButton

        PauseButton = img(self.Window.Resources.Images.Arcade.Pause,name = '.pause')
        Toolbar.Children += PauseButton

        Timer = Counter(name=".counter",text="0")
        Toolbar.Children += Timer
        # endregion

        WorldContainer = div(name=".worldContainer")
        Container.Children += WorldContainer

        self.Pong = ArcadePong(WorldContainer,settings, onGoal=lambda :OnGoal())
        
        tcb = TimedContinueButton(WorldContainer,lambda : OnCountdownFinish(), self.Window.Resources.Images.Arcade.Play, 3)
        def OnCountdownFinish():
            self.Pong.StartRound()
            Timer.Reset()
            Timer.Continue()
        def ShowCountDown():
            tcb.Reset()
        def OnGoal():
            Timer.Pause()
            ShowCountDown()
        def Pause():
            self.Pong.TogglePause()
            if self.Pong.IsPaused:Timer.Pause()
            else:Timer.Continue()

        def GoHome():
            from ...MainMenu import Document as MainMenu
            self.Window.Document = MainMenu
        # endregion       

        PauseButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:Pause())


    def Render(self):
        super().Render()

        


        

        
