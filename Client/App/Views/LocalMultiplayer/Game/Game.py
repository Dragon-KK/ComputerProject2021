from ....Core.DataTypes.UI import EventListener, Interval
from ....Core.Engine.Pong import LocalMultiplayerPong
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.CompoundItems import TimedContinueButton
from ....UI.Components import AspectRatioPreservedContainer
from ....UI.Elements import *
from ....Core.DataTypes.Game import GameSettings

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/LocalMultiplayer/Game"
    StyleSheet = "Styles/LocalMultiplayer/Game.json"
    ResourceKey = "LocalMultiplayer"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = GameSettings.FromJson(self.Window.Resources.Storage.LocalMultiplayer['GameSettings'])

        self.config(bg="black") # Let the background be black

        # Container (since we want our page to preserve aspect ratio)
        Container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)        
        self.Children += Container
       
       # region Toolbar
        Toolbar = div(name=".toolbar")
        Container.Children += Toolbar
        GoBackButton = img(self.Window.Resources.Images.LocalMultiplayer.Home, name = ".goHome")
        GoBackButton.EventListeners += EventListener("<Button-1>", lambda *args,**kwargs:GoHome())
        Toolbar.Children += GoBackButton

        PauseButton = img(self.Window.Resources.Images.LocalMultiplayer.Pause,name = '.pause')
        Toolbar.Children += PauseButton
        # endregion

        WorldContainer = div(name=".worldContainer")
        Container.Children += WorldContainer

        self.Pong = LocalMultiplayerPong(WorldContainer,settings, onGoal=lambda *args,**kwargs:OnGoal(*args,**kwargs))


        tcb = TimedContinueButton(WorldContainer,lambda : OnCountdownFinish(), self.Window.Resources.Images.LocalMultiplayer.Play, 3)
        def OnCountdownFinish():
            self.Pong.StartRound()
        def ShowCountDown():
            tcb.Reset()
        def UpdateScore():
            print(self.Pong.Score)
        def OnGoal(winner = ""):
            UpdateScore()
            
            if not winner:
                ShowCountDown()
            else:
                # Show end screen
                print("Winner has won",winner)
                pass
        def GoHome():
            from ...MainMenu import Document as MainMenu
            self.Window.Document = MainMenu
        # endregion       

        PauseButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.Pong.TogglePause())


    def Render(self):
        super().Render()

        


        

        
