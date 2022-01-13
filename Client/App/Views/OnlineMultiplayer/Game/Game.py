from ....Core.DataTypes.UI import EventListener, Interval
from ....Core.Engine.Pong import OnlineMultiplayerPong
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.CompoundItems import TimedContinueButton
from ....UI.Components import AspectRatioPreservedContainer
from ....UI.Elements import *
from ....Core.DataTypes.Game import GameSettings
from ....Core.Connection import PeerToPeer
from ....Core.Connection import Protocol
import threading
from ....Core.Diagnostics.Debugging import Console

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/OnlineMultiplayer/Game"
    StyleSheet = "Styles/OnlineMultiplayer/Game.json"
    ResourceKey = "OnlineMultiplayer"
    
    def OnMessage(self,msg):
        if msg == Protocol.Commands.DISCONNECT:
            self.Pong.PauseRound()
            self.MessageLabel = label(name = ".messageLabel", text = "Connecting to player...")
            self.WorldContainer.Parent.Children += self.MessageLabel
            self.WorldContainer.Remove()
            self.P2P.WordlessClose()
            self.MessageLabel.Text = "Connection Lost :("
        elif msg['type'] == 'command':
            if msg['data'] == 'RequestRoundStart':
                if self.HasRequestedStart:                    
                    self.P2P.SendMessage({
                        'type' : 'command',
                        'data' : 'StartRound'
                    })
                    self.StartRound()
            elif msg['data'] == 'StartRound':
                self.StartRound()

        elif msg['type'] == 'validate':
            return
                    

    def StartRound(self):     
        self.MessageLabel.Remove()
        def OnCountDownEnd():
            self.Pong.StartRound()
        tcb = TimedContinueButton(self.WorldContainer, OnCountDownEnd, self.Window.Resources.Images.OnlineMultiplayer.Play)
        tcb.StartCountDown()

    def RequestRoundStart(self):
        self.StartRoundButton.Remove()
        self.HasRequestedStart = True
        self.MessageLabel = label(name = ".messageLabel", text = "Waiting for opponent...")
        self.WorldContainer.Parent.Children += self.MessageLabel
        self.P2P.SendMessage({
            'type' : 'command',
            'data' : 'RequestRoundStart'
        })
        

    def ShowStartRoundButton(self):
        self.StartRoundButton = img(self.Window.Resources.Images.OnlineMultiplayer.Play, name = ".startRoundbutton")
        self.StartRoundButton.EventListeners += EventListener("<Button-1>", lambda e: self.RequestRoundStart())

        self.WorldContainer.Children += self.StartRoundButton

    def OnConnection(self):
        self.MessageLabel.Remove()
        settings = GameSettings.FromJson(self.Window.Resources.Storage.OnlineMultiplayer['GameSettings'])
        self.Pong = OnlineMultiplayerPong(self.WorldContainer,settings, onGoal=lambda *args,**kwargs:OnGoal(*args,**kwargs))

        self.ShowStartRoundButton()

    def OnConnectionError(self):
        self.Styles['.messageLabel'][0]['Styles']['ForegroundColor'] = "Red"
        self.MessageLabel.Text = "Could not connect"
        self.MessageLabel.UpdateBasedOnStyleSheet()

    def ConnectToPeer(self):
        from time import sleep
        sleep(4)
        Console.log("Trying to connect to peer")
        if self.P2P.ConnectToPeer(self.Window.Resources.Storage.OnlineMultiplayer['PeerAddress']):
            self.OnConnection()
        else:
            self.OnConnectionError()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.HasRequestedStart = False

        
        self.P2P = PeerToPeer()
        self.P2P.Listen(self.Window.Resources.Storage.OnlineMultiplayer['ListeningAddress'], self.OnMessage) # Start listening
        threading.Thread(target=self.ConnectToPeer,daemon=True).start() # Connect to peer
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
        
        self.P2P.Close()
        


        

        
