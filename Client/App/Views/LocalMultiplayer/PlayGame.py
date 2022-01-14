from ...UI.Base import Document
from ...UI.Elements import div,img,label
from ...Core.DataTypes.UI import EventListener
from ...UI.CustomElements import AspectRatioPreservedContainer
from ...UI.Items import TimedContinueButton
from ...UI.CustomElements.Sprites import Line
from ...Core.DataTypes.Standard import Vector
from ...Core.Engine.Pong import LocalMultiplayerPong
from ...Core.DataTypes.Game import GameSettings

class PlayGame(Document):
    Name = "Pong/LocalMultiplayer/PlayGame"
    StyleSheet = "Styles/LocalMultiplayer/PlayGame.json"
    ResourceKey = "LocalMultiplayer"
    def Destroy(self):
        super().Destroy()
        self.Pong.PauseRound()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = GameSettings.FromJson(self.Window.Resources.Storage.LocalMultiplayer['GameSettings'])
        self.Window.Title = f"{self.Name} ({self.Window.Resources.Storage.LocalMultiplayer['Difficulty']})"
        # Container (since we want our page to preserve aspect ratio)
        container = AspectRatioPreservedContainer(classes=".container")        
        self.Children += container
       
        # region Toolbar
        Toolbar = div(classes=".toolbar")
        container.Children += Toolbar

        p1Score = label(text = '0',classes = ".scoreCounter .p1score")
        p2Score = label(text = '0',classes = ".scoreCounter .p2score")

        Toolbar.Children += p1Score
        Toolbar.Children += p2Score

        GoBackButton = img(self.Window.Resources.Images.Home, classes = ".imgButton .goHome")
        GoBackButton.EventListeners += EventListener("<Button-1>", lambda e:self.NavigateTo("MainMenu"))
        Toolbar.Children += GoBackButton

        PauseButton = img(self.Window.Resources.Images.Pause,classes = '.imgButton .pause')
        PauseButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:Pause())
        Toolbar.Children += PauseButton
        # endregion

        WorldContainer = div(classes=".worldContainer")
        container.Children += WorldContainer

        

        self.Pong = LocalMultiplayerPong(WorldContainer,settings, onGoal=lambda **kwargs:OnGoal(**kwargs))
        
        tcb = TimedContinueButton(WorldContainer,lambda : OnCountdownFinish(), self.Window.Resources.Images.Play, 3)
        def OnCountdownFinish():
            self.Pong.StartRound()
        def ShowCountDown():
            tcb.Reset()
        def UpdateScore():
            p1Score.Text= self.Pong.Score[0]
            p2Score.Text= self.Pong.Score[1]
        def Pause():
            self.Pong.TogglePause()
        def OnGoal(winner = ""):
            UpdateScore()
            
            if not winner:
                ShowCountDown()
            else:
                t = ""
                if self.Pong.Score[0] > self.Pong.Score[1]:
                    p1Score.State += "Won"
                    p2Score.State += "Lost"
                    t = "Player 1 Wins"
                else:
                    p1Score.State += "Lost"
                    p2Score.State += "Won"
                    t = "Player 2 Wins"
                container.Children += label(classes = '.gameoverMessage',text = t)
        # endregion       


    def NavigateTo(self, dest):
        if dest == "MainMenu":
            from ..MainMenu import MainMenu
            self.Window.ChangeDocumentTo(MainMenu)