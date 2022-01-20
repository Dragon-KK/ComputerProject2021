from ...UI.Base import Document
from ...UI.Elements import div,img,label
from ...Core.DataTypes.UI import EventListener
from ...UI.CustomElements import AspectRatioPreservedContainer,Counter
from ...UI.Items import TimedContinueButton
from ...Core.Engine.Pong import OnlineMultiplayerPong
from ...Core.DataTypes.Game import GameSettings
from ...Core.Connection import PeerToPeer
from ...Core.Connection.Commands import Commands

class PlayGame(Document):
    Name = "Pong/OnlineMultiplayer/PlayGame"
    StyleSheet = "Styles/OnlineMultiplayer/PlayGame.json"
    ResourceKey = "OnlineMultiplayer"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = GameSettings.FromJson(self.Window.Resources.Storage.OnlineMultiplayer['game']['gameSettings'])
        self.Window.Title = f"{self.Name} {self.Window.Resources.Storage.OnlineMultiplayer['game']['name']} ({self.Window.Resources.Storage.OnlineMultiplayer['game']['gameDifficulty']})"
        # Container (since we want our page to preserve aspect ratio)
        container = AspectRatioPreservedContainer(classes=".container")        
        self.Children += container
       
        # region Toolbar
        Toolbar = div(classes=".toolbar")
        container.Children += Toolbar

        GoBackButton = img(self.Window.Resources.Images.Home, classes = ".imgButton .goHome")
        GoBackButton.EventListeners += EventListener("<Button-1>", lambda e:self.NavigateTo("MainMenu"))
        self.p1Score = label(text = '0',classes = ".scoreCounter .p1score")
        self.p2Score = label(text = '0',classes = ".scoreCounter .p2score")

        Toolbar.Children += self.p1Score
        Toolbar.Children += self.p2Score
        Toolbar.Children += GoBackButton
        # endregion

        self.P2P = PeerToPeer(self.Window.Resources.Networking.peerListener)
        self.P2P.Listen(self.Window.Resources.Storage.OnlineMultiplayer['listeningAddr'], self.OnMessage)
        self.WorldContainer = div(classes=".worldContainer")
        container.Children += self.WorldContainer
        self.MsgBox = label(classes = ".gameoverMessage",text = "Connecting to opponent...")

        self.IsMain = (tuple(self.Window.Resources.Storage.OnlineMultiplayer['peerAddr']) != tuple(self.Window.Resources.Storage.OnlineMultiplayer['game']['addr']))
        self.Pong = OnlineMultiplayerPong(self.WorldContainer,settings, onGoal=lambda **kwargs:OnGoal(**kwargs),isLeft = self.IsMain)
        self.WorldContainer.Children += self.MsgBox
        
        self.P2P.Connect(self.Window.Resources.Storage.OnlineMultiplayer['peerAddr'], onConnection=self.OnConnection,onError = self.OnConnectionError,wait = 10)

    def OnConnectionError(self):
        if self.MsgBox:
            self.MsgBox.Remove()
            self.MsgBox = None
        self.MsgBox = label(classes = ".gameoverMessage .redText",text = "Could not connect :(")
        self.WorldContainer.Children += self.MsgBox

    def OnConnection(self):
        
        if self.MsgBox:
            self.MsgBox.Remove()
            self.MsgBox = None
        self.Pong.OnGoalCallback = lambda **kwargs:OnGoal(**kwargs)

        self.RoundStartHasBeenRequested = False
        self.OtherScore = None

        self.tcb = TimedContinueButton(self.WorldContainer,lambda : OnCountdownFinish(), self.Window.Resources.Images.Play, 3,customCountdownStart=True)
        self.tcb.ImageElement.EventListeners += EventListener("<Button-1>", lambda e:RequestCountdownStart())
        def OnCountdownFinish():
            self.OtherScore = None
            self.RoundStartHasBeenRequested = False
            self.Pong.StartRound()
            self.P2P.SendImages(cancel=lambda : self.Pong.RoundHasEnded,data=lambda:self.Pong.GetImage(),delay = 0.01)
        def RequestCountdownStart():
            if not self.P2P.TalkerIsConnected:return self.OnConnectionError()
            if ".greenBack" in self.tcb.ImageElement.ClassList:return
            if self.RoundStartHasBeenRequested:
                self.P2P.StartRound()
                self.Pong.Reset()
                if self.IsMain:
                    self.P2P.UpdateImage(self.Pong.GetInitialImage())
                self.tcb.StartCountDown()
            else:
                self.tcb.ImageElement.ClassList += ".greenBack"
                self.P2P.RequestRoundStart()

        def ShowCountDown():
            self.tcb.Reset()
            self.tcb.ImageElement.ClassList -= ".greenBack"
            if not self.P2P.TalkerIsConnected:self.OnConnectionError()
        def UpdateScore():
            self.p1Score.Text= self.Pong.Score[0]
            self.p2Score.Text= self.Pong.Score[1]
        def OnGoal(winner = ""):
            
            UpdateScore()
            if self.OtherScore:
                if self.OtherScore != self.Pong.Score:
                    self.RaiseInconsistency()
                    return
            else:
                self.P2P.ValidateResult(self.Pong.Score)
                        
            if not winner:
                ShowCountDown()
            else:
                t = ""
                if self.Pong.Score[0] > self.Pong.Score[1]:
                    self.p1Score.State += "Won"
                    self.p2Score.State += "Lost"
                    t = "Player 1 Wins"
                else:
                    self.p1Score.State += "Lost"
                    self.p2Score.State += "Won"
                    t = "Player 2 Wins"
                self.WorldContainer.Children += label(classes = '.gameoverMessage',text = t)
                self.P2P.Close()
        # endregion        
        

    def OnMessage(self, msg):
        if msg == Commands.DISCONNECT:
            return True
        elif msg['command'] == Commands.UpdateImage:
            self.Pong.UpdateFromImage(msg['data'])
        elif msg['command'] == Commands.RequestRoundStart:
            self.RoundStartHasBeenRequested = True
        elif msg['command'] == Commands.UpdateScore:
            self.OtherScore = msg['data']
        elif msg['command'] == Commands.StartRound:
            self.Pong.Reset()
            if self.IsMain:
                self.P2P.UpdateImage(self.Pong.GetInitialImage())
            self.tcb.StartCountDown()
        elif msg['command'] == Commands.RaiseInconsistency:
            self.P2P.Close()
            if self.MsgBox:
                self.MsgBox.Remove()
                self.MsgBox = None
            self.MsgBox = label(classes = ".gameoverMessage .redText",text = "Validation error!")
            self.WorldContainer.Children += self.MsgBox

    def RaiseInconsistency(self):
        self.P2P.RaiseInconsistency()
        self.P2P.Close()
        if self.MsgBox:
            self.MsgBox.Remove()
            self.MsgBox = None
        self.MsgBox = label(classes = ".gameoverMessage .redText",text = "Validation error!")
        self.WorldContainer.Children += self.MsgBox
        

    def Destroy(self):
        super().Destroy()
        self.Pong.PauseRound() 
        self.P2P.Close()
        self.Window.Resources.Networking.ReleaseResource("peerListener")

    def NavigateTo(self, dest):
        if dest == "MainMenu":
            from ..MainMenu import MainMenu
            self.Window.ChangeDocumentTo(MainMenu)