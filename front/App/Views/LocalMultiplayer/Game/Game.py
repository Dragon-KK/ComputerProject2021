from ....Core.DataTypes.UI import EventListener, Interval
from ....Core.Engine.Pong import LocalMultiplayerPong
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.Components import *
from ....UI.Elements import *
from ....UI import Styles


class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/LocalMultiplayer/Game"
    StyleSheet = "Styles/LocalMultiplayer/Game.json"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

        self.Pong = LocalMultiplayerPong(WorldContainer,None)


        # region Callbacks
        def TogglePause(e):
            self.Pong.TogglePause()
        # endregion

        

        PauseButton.EventListeners += EventListener("<Button-1>", TogglePause)

    def Render(self):
        super().Render()
        def Test():
            self.Pong.World.Entities[0].Position += Vector(5, 0)
        self.Pong.ContinueRound()
        self.Window.Intervals += Interval(10, Test)
        


        

        
