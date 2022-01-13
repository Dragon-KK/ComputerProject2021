from ....Core.DataTypes.UI import EventListener, Interval
from ....Core.Engine.Pong import LocalMultiplayerPong
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.CompoundItems import TimedContinueButton
from ....UI.Components import AspectRatioPreservedContainer
from ....UI.Elements import *
from ....Core.DataTypes.Game import GameSettings
from ....Core.Connection import PeerToPeer
import threading
from ....Core.Diagnostics.Debugging import Console

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/OnlineMultiplayer/Game"
    StyleSheet = "Styles/OnlineMultiplayer/Game.json"
    ResourceKey = "OnlineMultiplayer"
    
    def OnMessage(self,msg):
        print(msg)

    def OnConnection(self):
        self.MessageLabel.Remove()
        settings = GameSettings.FromJson(self.Window.Resources.Storage.OnlineMultiplayer['GameSettings'])
        self.Pong = LocalMultiplayerPong(self.WorldContainer,settings, onGoal=lambda *args,**kwargs:OnGoal(*args,**kwargs))

        tcb = TimedContinueButton(self.WorldContainer,lambda : OnCountdownFinish(), self.Window.Resources.Images.OnlineMultiplayer.Play, 3)
        def OnCountdownFinish():
            self.P2P.SendMessage("Hello")
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
        
        # endregion       

        
        self.PauseButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.Pong.TogglePause())

    def OnConnectionError(self):
        self.Styles['.messageLabel'][0]['Styles']['ForegroundColor'] = "Red"
        self.MessageLabel.Text = "Could not connect"
        self.MessageLabel.UpdateBasedOnStyleSheet()

    def ConnectToPeer(self):
        from time import sleep
        sleep(4)
        Console.log("Trying to connect to peer")
        if self.P2P.ConnectToPeer(self.Window.Resources.Storage.OnlineMultiplayer['PeerAddress']):
            print("Hello")
            self.OnConnection()
        else:
            self.OnConnectionError()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.P2P = PeerToPeer()
        self.P2P.Listen(self.Window.Resources.Storage.OnlineMultiplayer['ListeningAddress'], self.OnMessage)
        threading.Thread(target=self.ConnectToPeer,daemon=True).start()
        self.config(bg="black") # Let the background be black

        # Container (since we want our page to preserve aspect ratio)
        Container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)        
        self.Children += Container
       
        # region Toolbar
        Toolbar = div(name=".toolbar")
        Container.Children += Toolbar
        GoBackButton = img(self.Window.Resources.Images.OnlineMultiplayer.Home, name = ".goHome")
        GoBackButton.EventListeners += EventListener("<Button-1>", lambda *args,**kwargs:GoHome())
        Toolbar.Children += GoBackButton

        self.PauseButton = img(self.Window.Resources.Images.OnlineMultiplayer.Pause,name = '.pause')
        Toolbar.Children += self.PauseButton
        # endregion

        self.WorldContainer = div(name=".worldContainer")
        Container.Children += self.WorldContainer

        self.MessageLabel = label(name = ".messageLabel", text = "Connecting to player...")
        Container.Children += self.MessageLabel

        def GoHome():
            from ...MainMenu import Document as MainMenu
            self.Window.Document = MainMenu

        

    def Destroy(self):
        super().Destroy()
        

        


        

        
