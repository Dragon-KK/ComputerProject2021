from ...UI.Base import Document
from ...UI.Elements import div,img,label,ListBox
from ...Core.DataTypes.UI import EventListener
from ...Core.Connection import Client
from ...Core.Connection.Commands import Commands
from ...UI.CustomElements import AspectRatioPreservedContainer

class Lobby(Document):
    Name = "Pong/OnlineMultiplayer/Lobby"
    StyleSheet = "Styles/OnlineMultiplayer/Lobby.json"
    ResourceKey = "OnlineMultiplayer"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # region Background
        container = AspectRatioPreservedContainer() # The container
        self.Children += container # Add child
        background = img(self.Window.Resources.Images.Background,classes = ".background") # The background
        container.Children += background # Add child
        # endregion

        # title
        background.Children += label(text="Lobby", classes = ".title")

        # region goHomeButton
        goHomeButton = img(self.Window.Resources.Images.Home, classes = ".goHome .imgButton")
        goHomeButton.EventListeners += EventListener("<Button-1>", lambda e:self.NavigateTo("MainMenu"))
        background.Children += goHomeButton
        # endregion

        self.ContentContainer = div(classes = '.lobbyContainer')
        background.Children += self.ContentContainer
        self.ListBox = ListBox(classes = ".gameRequestList")
        self.ContentContainer.Children += self.ListBox
        self.Client = Client()
        self.Client.Connect(tuple(self.Window.Resources.Storage.OnlineMultiplayer['ServerAddress']), onError=self.ConnectionFailure, onConnection=self.ConnectionSucces)

    def ConnectionFailure(self):
        self.ContentContainer.Children += label(classes = '.msgBox .error', text = "Could Not Connect to Server")

    def ConnectionSucces(self):
        self.Client.Listen(self.OnMessage)
        
        
        addItemBox = div(classes = ".addItemBox")
        addItemImg = img(self.Window.Resources.Images.Add, classes = ".addItemImg")
        addItemBox.EventListeners += EventListener("<Button-1>",lambda e:self.CreateItem())
        addItemImg.EventListeners += EventListener("<Button-1>",lambda e:self.CreateItem())
        self.ListBox.Children += addItemBox
        addItemBox.Children += addItemImg
        for _ in range(10):
            self.ListBox.Children.Add(div(classes = ".addItemBox"))
        self.Client.RequestGameList()

    def CreateItem(self):
        print("Creating Item")

    def SHowItemInfo(self, item):
        print("Showing item", item)

    def AddItems(self, items):
        print("Adding Items", items)

    def RemoveItems(self, items):
        print("Removing items", items)

    def StartGame(self, game, peerAddr):
        print("Need to start game", game)

    def AcceptGame(self, game):
        print("Accepting game", game)

    def OnMessage(self,message):
        if message['command'] == Commands.HideGames:
            self.RemoveItems(message['games'])
        elif message['command'] == Commands.ShowGames:
            self.AddItems(message['games'])
        elif message['command'] == Commands.BeginGame:
            self.StartGame(message['game'], message['addr'])

    def Destroy(self):
        self.Client.Close()
        super().Destroy()

    def NavigateTo(self, dest):
        if dest == "MainMenu":
            from ..MainMenu import MainMenu
            self.Window.ChangeDocumentTo(MainMenu)
        elif dest == "PlayGame":
            self.SetSettings()
            from .PlayGame import PlayGame
            self.Window.ChangeDocumentTo(PlayGame)