from ...UI.Base import Document
from ...UI.Elements import div,img,label
from ...Core.DataTypes.UI import EventListener
from ...UI.CustomElements import AspectRatioPreservedContainer,Counter
from ...UI.Items import TimedContinueButton
from ...Core.Engine.Pong import ArcadePong
from ...Core.DataTypes.Game import GameSettings

class PlayGame(Document):
    Name = "Pong/Arcade/PlayGame"
    StyleSheet = "Styles/Arcade/PlayGame.json"
    ResourceKey = "Arcade"
    def Destroy(self):
        super().Destroy()
        self.Pong.PauseRound()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = GameSettings.FromJson(self.Window.Resources.Storage.Arcade['GameSettings'])
        self.Window.Title = f"{self.Name} ({self.Window.Resources.Storage.Arcade['Difficulty']})"
        # Container (since we want our page to preserve aspect ratio)
        container = AspectRatioPreservedContainer(classes=".container")        
        self.Children += container
       
        # region Toolbar
        Toolbar = div(classes=".toolbar")
        container.Children += Toolbar

        GoBackButton = img(self.Window.Resources.Images.Home, classes = ".imgButton .goHome")
        GoBackButton.EventListeners += EventListener("<Button-1>", lambda e:self.NavigateTo("MainMenu"))
        Toolbar.Children += GoBackButton

        PauseButton = img(self.Window.Resources.Images.Pause,classes = '.imgButton .pause')
        PauseButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:Pause())
        Toolbar.Children += PauseButton

        Timer = Counter(classes=".counter",text="0")
        Toolbar.Children += Timer
        # endregion

        WorldContainer = div(classes=".worldContainer")
        container.Children += WorldContainer

        self.Pong = ArcadePong(WorldContainer,settings, onGoal=lambda :OnGoal())
        
        tcb = TimedContinueButton(WorldContainer,lambda : OnCountdownFinish(), self.Window.Resources.Images.Play, 3)
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
        # endregion       


    def NavigateTo(self, dest):
        if dest == "MainMenu":
            from ..MainMenu import MainMenu
            self.Window.ChangeDocumentTo(MainMenu)