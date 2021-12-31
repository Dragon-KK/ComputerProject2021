from ....Core.DataTypes.UI import EventListener, Interval
from ....Core.Engine.Pong import LocalMultiplayerPong
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.Components import *
from ....UI.Elements import *
from ....UI import Styles
from ....Core.DataTypes.Game import GameSettings

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/LocalMultiplayer/Game"
    StyleSheet = "Styles/LocalMultiplayer/Game.json"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO
        # Add a way to get settings from settings screen
        settings = GameSettings(20, 1, 1, False, 5)

        self.config(bg="black") # Let the background be black

        # Container (since we want our page to preserve aspect ratio)
        Container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)        
        self.Children += Container
       
       # region Toolbar
        Toolbar = div(name=".toolbar")
        Container.Children += Toolbar

        PauseButton = div(name = '.pause')
        Toolbar.Children += PauseButton
        # endregion

        WorldContainer = div(name=".worldContainer")
        Container.Children += WorldContainer

        self.Pong = LocalMultiplayerPong(WorldContainer,settings, onGoal=lambda *args,**kwargs:OnGoal(*args,**kwargs))



        # region Callbacks
        # TODO
        # In the future change this to an image
        tcb = TimedContinueButton(name=".startCountdown",text=" Start?",countdown=3, onfinish=lambda:OnCountdownFinish())
        def OnCountdownFinish():
            tcb.Remove()
            self.Pong.StartRound()
        def ShowCountDown():
            tcb.Reset()
            WorldContainer.Children += tcb
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
        # endregion       

        PauseButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.Pong.TogglePause())

        ShowCountDown()

    def Render(self):
        super().Render()

        


        

        
