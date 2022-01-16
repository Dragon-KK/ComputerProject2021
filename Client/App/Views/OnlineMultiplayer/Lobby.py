from ...UI.Base import Document
from ...UI.Elements import div,img,label
from ...Core.DataTypes.UI import EventListener
from ...Core.Connection import Client,Worker
from ...Core.Connection.Commands import Commands
from ...UI.CustomElements import AspectRatioPreservedContainer
from .GameList import GameList

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

        self.Client = Client()
        self.Client.Connect(tuple(self.Window.Resources.Storage.OnlineMultiplayer['ServerAddress']), onError=self.ConnectionFailure, onConnection=self.ConnectionSucces)

    def ConnectionFailure(self):
        self.ContentContainer.Children += label(classes = '.msgBox .error', text = "Could Not Connect to Server")

    def ConnectionSucces(self):
        self.GameList = GameList(self.ContentContainer)
        self.Client.Listen(self.OnMessage)
        self.Client.RequestGameList()

    def OnMessage(self,msg):
        if message['command'] == Commands.HideGames:
            pass
        elif message['command'] == Commands.ShowGames:
            pass

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