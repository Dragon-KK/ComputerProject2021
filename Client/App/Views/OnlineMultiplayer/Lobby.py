from ...UI.Base import Document
from ...UI.Elements import div,img,label,ListBox,input,radio
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
        self.CurrGameID = 0
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
        addItemImg = img(self.Window.Resources.Images.Plus, classes = ".addItemImg")
        addItemBox.EventListeners += EventListener("<Button-1>",lambda e:self.CreateItem())
        addItemImg.EventListeners += EventListener("<Button-1>",lambda e:self.CreateItem())
        addItemImg.EventListeners += EventListener("<Enter>",lambda e:addItemBox.State.AddState("Hovered"))
        addItemImg.EventListeners += EventListener("<Leave>",lambda e:addItemBox.State.RemoveState("Hovered"))
        self.Items = []
        self.ListBox.Children += addItemBox
        addItemBox.Children += addItemImg
        self.Client.RequestGameList()

    def CreateItem(self):
        createItemBox = div(classes = ".popupBox")
        self.ContentContainer.Children += createItemBox
        closeButton = img(self.Window.Resources.Images.Close, classes = ".closeButton")
        closeButton.EventListeners += EventListener("<Button-1>", lambda e:OnCloseClick())
        createItemBox.Children += closeButton

        nameInput = input(classes = ".name", placeHolder="Name...", maxLength=19)
        createItemBox.Children += nameInput

        # region radio
        OptionsRadio = radio(classes = ".optionsRadio")
        createItemBox.Children += OptionsRadio

        OptionsRadio.Children += label(text = "Beginner",classes = ".option .lvl1")
        OptionsRadio.Children += label(text = "Novice",classes = ".option .lvl2")
        OptionsRadio.Children += label(text = "Amateur",classes = ".option .lvl3")
        OptionsRadio.Children += label(text = "Expert",classes = ".option .lvl4")
        OptionsRadio.Children += label(text = "Impossible",classes = ".option .lvl5")

        OptionsRadio.SelectedElement = OptionsRadio.Children[0]
        # endregion

        #region duece Button
        allowDuece = label(classes = ".allowDueceToggles",text = "No Duece")
        allowDuece.EventListeners += EventListener("<Button-1>", lambda e:ToggleDueceSelect())
        createItemBox.Children += allowDuece
        #endregion

        winCondInp = input(classes = '.winCondInp',Type=int,allowNegative=False,placeHolder="Race to ? Eg: 5",maxLength=3)
        createItemBox.Children += winCondInp

        acceptIcon = img(self.Window.Resources.Images.Plus, classes = ".createButton")
        acceptIcon.EventListeners += EventListener("<Button-1>", lambda e:Create())
        createItemBox.Children += acceptIcon

        def ToggleDueceSelect():
            if ".confirmGreen" in allowDuece.ClassList:
                allowDuece.Text = "No Duece"
                allowDuece.ClassList.RemoveClass(".confirmGreen")
            else:
                allowDuece.Text = "Allow Duece"
                allowDuece.ClassList.AddClass(".confirmGreen")
        def OnCloseClick():
            createItemBox.Remove()

        def getGameSettings():
            settings = {}
            difficulty = OptionsRadio.SelectedElement.Text
            if difficulty == "Beginner":
                settings = {
                    "Difficulty" : 30,
                    "DifficultySlope" : 0,
                    "BallCount" : 1,
                    "Duece" : False,
                    "WinCondition" : 0,
                }
            elif difficulty == "Novice":
                settings = {
                    "Difficulty" : 40,
                    "DifficultySlope" : 0.01,
                    "BallCount" : 1,
                    "Duece" : False,
                    "WinCondition" : 0,
                }
            elif difficulty == "Amateur":
                settings = {
                    "Difficulty" : 30,
                    "DifficultySlope" : 0.1,
                    "BallCount" : 1,
                    "Duece" : False,
                    "WinCondition" : 0,
                }
            elif difficulty == "Expert":
                settings = {
                    "Difficulty" : 30,
                    "DifficultySlope" : 0.1,
                    "BallCount" : 2,
                    "Duece" : False,
                    "WinCondition" : 0,
                }       
            elif difficulty == "Impossible":
                settings = {
                    "Difficulty" : 40,
                    "DifficultySlope" : 0.01,
                    "BallCount" : 5,
                    "Duece" : False,
                    "WinCondition" : 0,
                }
            settings["WinCondition"] = winCondInp.Value if winCondInp.Value > 0 else 5
            settings["Duece"] = allowDuece.Text == "Allow Duece"
            return settings

        def Create():
            self.CurrGameID += 1
            item = {}
            item['id'] = self.CurrGameID
            item['addr'] = self.Client.TalkerAddr
            item['gameDifficulty'] = OptionsRadio.SelectedElement.Text
            item['gameSettings'] = getGameSettings()
            item['name'] = nameInput.Value if nameInput.Value else "New Game"
            createItemBox.Remove()
            self.Client.CreateGame(item)
            self.AddItems([item])

    def ShowItemInfo(self, item):
        createItemBox = div(classes = ".popupBox")
        self.ContentContainer.Children += createItemBox
        closeButton = img(self.Window.Resources.Images.Close, classes = ".closeButton")
        closeButton.EventListeners += EventListener("<Button-1>", lambda e:OnCloseClick())
        createItemBox.Children += closeButton

        nameInput = label(elemName = "input",classes = ".name", text=item['name'])
        createItemBox.Children += nameInput

        # region radio
        OptionsRadio = div(classes = ".optionsRadio")
        createItemBox.Children += OptionsRadio

        OptionsRadio.Children += label(text = "Beginner",classes = ".option .lvl1")
        OptionsRadio.Children += label(text = "Novice",classes = ".option .lvl2")
        OptionsRadio.Children += label(text = "Amateur",classes = ".option .lvl3")
        OptionsRadio.Children += label(text = "Expert",classes = ".option .lvl4")
        OptionsRadio.Children += label(text = "Impossible",classes = ".option .lvl5")

        for i in OptionsRadio.Children:
            if i.Text == item['gameDifficulty']:
                i.State += "RadioSelected"
                break
        # endregion

        #region duece Button
        allowDuece = label(classes = ".allowDueceToggles" + (" .confirmGreen" if item['gameSettings']['Duece'] else ""),text = "Allow Duece" if item['gameSettings']['Duece'] else "No Duece")
        createItemBox.Children += allowDuece
        #endregion

        winCondInp = label(elemName = "input",classes = '.winCondInp',text = str(item['gameSettings']['WinCondition']))
        createItemBox.Children += winCondInp

        if tuple(item['addr']) == self.Client.TalkerAddr:
            acceptIcon = img(self.Window.Resources.Images.Cancel, classes = ".createButton .red")
            acceptIcon.EventListeners += EventListener("<Button-1>", lambda e:removeItem())
            createItemBox.Children += acceptIcon
        else:
            acceptIcon = img(self.Window.Resources.Images.Accept, classes = ".createButton")
            acceptIcon.EventListeners += EventListener("<Button-1>", lambda e:acceptItem())
            createItemBox.Children += acceptIcon
        def OnCloseClick():
            createItemBox.Remove()
        def removeItem():
            createItemBox.Remove()
            self.CancelItem(item)
        def acceptItem():
            createItemBox.Remove()
            self.AcceptGame(item)

    def AddItem(self, item):
        itemContainer = div(classes = ".itemBox")
        itemContainer.Item = item
        self.Items.append(itemContainer)
        self.ListBox.Children.Add(itemContainer, notify=False)
        infoImg = img(self.Window.Resources.Images.Info, classes = ".imgIcon .info")
        infoImg.EventListeners += EventListener("<Button-1>", lambda e:self.ShowItemInfo(item))
        itemContainer.Children += label(classes = ".itemName", text = item['name'])
        itemContainer.Children += infoImg

        if tuple(item['addr']) == self.Client.TalkerAddr:
            cancelImg = img(self.Window.Resources.Images.Cancel, classes = ".imgIcon .secondary")
            cancelImg.EventListeners += EventListener("<Button-1>", lambda e:self.CancelItem(item))
            itemContainer.Children += cancelImg
        else:
            acceptImg = img(self.Window.Resources.Images.Accept, classes = ".imgIcon .secondary")
            acceptImg.EventListeners += EventListener("<Button-1>", lambda e:self.AcceptGame(item))
            itemContainer.Children += acceptImg

    def AddItems(self, items):
        for item in items:
            self.AddItem(item)
                           

        self.ListBox.OnChildrenChanged()

    def CancelItem(self, item):
        self.Client.CancelGame(item)
        self.RemoveItems([item])

    def RemoveItems(self, items):
        def eq(i1,i2):
            return i1['addr'] == i2['addr'] and i1['id'] == i2['id']
        for item in items:
            for i in range(len(self.Items)):
                if eq(self.Items[i].Item, item):
                    self.Items.pop(i).Remove()
                    break

    def StartGame(self, game, peerAddr):
        self.Window.Resources.Storage.OnlineMultiplayer['peerAddr'] = peerAddr
        self.Window.Resources.Storage.OnlineMultiplayer['game'] = game
        self.Window.Resources.Storage.OnlineMultiplayer['listeningAddr'] = self.Client.TalkerAddr
        self.NavigateTo("PlayGame")

    def AcceptGame(self, game):
        self.Client.AcceptGame(game, game['addr'])

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
            from .PlayGame import PlayGame
            self.Window.ChangeDocumentTo(PlayGame)