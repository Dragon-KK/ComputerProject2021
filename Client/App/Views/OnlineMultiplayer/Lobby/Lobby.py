from ....Core.DataTypes.UI import Interval, EventListener
from ....Core.DataTypes.Standard import Vector
from ....Core.Connection import Worker
from threading import Thread
from ....UI.Base import Document as doc
from ....UI.Components import *
from ....UI.Elements import *

'''
In the lobby you connect to the server and can communicate to get another partner to play
Once you get the partners address it is saved in Storage
Then game is opened

In game the connection is made with the address saved in storage
and the game is started then
'''
class GameRequest:
    def __init__(self, ID, address, name, gameSettings, container, onGameAcceptance):
        # Each sender keeps track of an id relative to themselves
        self.Id = ID # The id
        self.Address = address # The address of the sender
        self.GameSettings = gameSettings # Game settings will just be a dict cause we dont really need the gamesettings object here
        self.Name = name # The name of the game (to identify it)
        
        self.Container = container
        self.__InfoExpanded = False
        self.OnGameAcceptance = onGameAcceptance

    def Show(self):
        # This is very dirty yes. BUt we have no time       
       
        def ShowInfo():
            def acceptGame():
                self.OnGameAcceptance(self)
                closeInfo()
            def closeInfo():
                gameInfoContainer.Remove()
            gameInfoContainer = div(name = ".gameInfoContainer")
            self.Container.Window.Document.Children += gameInfoContainer
            closeInfoContainer = img(self.Container.Window.Resources.Images.OnlineMultiplayer.Close,name=".closeMoreInfo")
            gameInfoContainer.Children += closeInfoContainer
            acceptGameButton = img(self.Container.Window.Resources.Images.OnlineMultiplayer.Accept,name=".acceptGameButton")
            gameInfoContainer.Children += acceptGameButton

            listbox = ListBox(name = ".gameInfoList")
            gameInfoContainer.Children += listbox

            listbox.Children += label(name = ".gameInfo", text = self.Name[:20] + ("..." if len(self.Name) > 20 else ""))
            listbox.Children += label(name = ".gameInfo", text = f"Difficulty : {self.GameSettings['Difficulty']}")
            listbox.Children += label(name = ".gameInfo", text = f"DifficultySlope : {self.GameSettings['DifficultySlope']}")
            listbox.Children += label(name = ".gameInfo", text = f"BallCount : {self.GameSettings['BallCount']}")
            listbox.Children += label(name = ".gameInfo", text = f"Duece : {self.GameSettings['Duece']}")
            listbox.Children += label(name = ".gameInfo", text = f"WinCondition : {self.GameSettings['WinCondition']}")

            closeInfoContainer.EventListeners += EventListener("<Button-1>", lambda *args:closeInfo())
            acceptGameButton.EventListeners += EventListener("<Button-1>", lambda *args:acceptGame())


        self.GameRequestContainer = div(name = '.gameRequestContainer') # A box that shows the info of a game request
        self.Container.Children += self.GameRequestContainer


        gameReqLabel = label(name = ".gameRequestLabel", text = self.Name) # Shows the name of the game request
        self.GameRequestContainer.Children += gameReqLabel

        self.GameRequestContainer.EventListeners += EventListener("<Button-1>", lambda *args:ShowInfo())
        gameReqLabel.EventListeners += EventListener("<Button-1>", lambda *args:ShowInfo())
        


    def Remove(self):
        self.GameRequestContainer.Remove()

    @classmethod
    def FromJson(cls, data, container, ongameaccpetance = lambda *args:0):
        return cls(data['id'], data['addr'], data['name'],data['gameSettings'], container, ongameaccpetance)

    def ToJson(self):
        return {
            "id" : self.Id,
            "addr" : self.Address,
            "gameSettings" : self.GameSettings,
            'name' : self.Name
        }

    def __eq__(self, other):
        return self.Id == other.Id and self.Address == other.Address

class GameRequestList:
    def __init__(self, container,onGameAccept, name = ".gameRequestsList"):        
        self.ListBox = ListBox(name=name)
        container.Children += self.ListBox
        self.OnGameAcceptance = onGameAccept
        self.RequestList = []

    def Add(self, req):
        '''Adds a game request'''
        if type(req) == list:
            for r in req:
                s = GameRequest.FromJson(r, self.ListBox, ongameaccpetance= self.OnGameAcceptance)
                self.RequestList.append(s)
                s.Show()
        else:
            req = GameRequest.FromJson(req, self.ListBox, ongameaccpetance= self.OnGameAcceptance)
            self.RequestList.append(req)
            req.Show()
        self.ListBox.Update(propogationDepth=float('inf'))

    def Remove(self, req):
        '''Removes a game request'''
        if type(req) == list:
            for r in req:
                s = GameRequest.FromJson(r, self.ListBox)
                index = self.RequestList.index(s) if s in self.RequestList else -1
                if index > -1:
                    self.RequestList[index].Remove()
                    self.RequestList.pop(index)
        else:
            req = GameRequest.FromJson(req, self.ListBox)
            index = self.RequestList.index(req) if req in self.RequestList else -1
            if index > -1:
                self.RequestList[index].Remove()
                self.RequestList.pop(index)
        self.ListBox.Update(propogationDepth=float('inf'))

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/OnlineMultiplayer/Lobby"
    ResourceKey = "OnlineMultiplayer"
    StyleSheet = "Styles/OnlineMultiplayer/Lobby.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg="black") # Let the background be black
        # Container (since we want our page to preserve aspect ratio)
        container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)        
        self.Children += container
        # Title
        title = label(name = ".title", text = "Lobby")
        container.Children += title
        # Go Home
        def GoHome():
            from ...MainMenu import Document as MainMenu
            self.Window.Document = MainMenu
        GoBackButton = img(self.Window.Resources.Images.OnlineMultiplayer.Home, name = ".goHome")
        GoBackButton.EventListeners += EventListener("<Button-1>", lambda *args,**kwargs:GoHome())
        container.Children += GoBackButton
        self.GameRequestList = GameRequestList(container, self.OnGameAcceptance)

        self.__NextGameReqID = 0
        def createGame():
            def createGame():
                self.__NextGameReqID += 1
                self.CreateGameRequest({
                    "id" : self.__NextGameReqID,
                    "addr" : self.Worker.Address,
                    "gameSettings" : {
                        'Difficulty' : listbox.Children[1].Value,
                        'DifficultySlope' : listbox.Children[2].Value,
                        'BallCount' : listbox.Children[3].Value,
                        'Duece' : True if listbox.Children[4].Value == "y" else False,
                        'WinCondition' : listbox.Children[5].Value
                    },
                    'name' : listbox.Children[0].Value if listbox.Children[0].Value else "NewGame"
                })
                closeInfo()
            def closeInfo():
                gameInfoContainer.Remove()
            gameInfoContainer = div(name = ".gameInfoContainer")
            self.Children += gameInfoContainer
            closeInfoContainer = img(self.Window.Resources.Images.OnlineMultiplayer.Close,name=".closeMoreInfo")
            gameInfoContainer.Children += closeInfoContainer
            acceptGameButton = img(self.Window.Resources.Images.OnlineMultiplayer.Create,name=".createGameButton")
            gameInfoContainer.Children += acceptGameButton

            listbox = ListBox(name = ".gameInfoList2")
            gameInfoContainer.Children += listbox

            listbox.Children += input(name = ".gameInfo2", placeHolder="name", maxLength=15)
            listbox.Children += input(name = ".gameInfo2", placeHolder= "Difficulty", maxLength=21, Type=float,allowNegative=False)
            listbox.Children += input(name = ".gameInfo2", placeHolder = "DifficultySlope", maxLength=21,Type=float,allowNegative=False)
            listbox.Children += input(name = ".gameInfo2", placeHolder = "BallCount", maxLength=21,Type=int,allowNegative=False)
            listbox.Children += input(name = ".gameInfo2", placeHolder = "Duece? y/n", maxLength=1)
            listbox.Children += input(name = ".gameInfo2", placeHolder = "WinCondition", maxLength=21,Type=int,allowNegative=False)

            closeInfoContainer.EventListeners += EventListener("<Button-1>", lambda *args:closeInfo())
            acceptGameButton.EventListeners += EventListener("<Button-1>", lambda *args:createGame())
        createGameButton = img(self.Window.Resources.Images.OnlineMultiplayer.Create, name = ".createGameIcon")
        createGameButton.EventListeners += EventListener("<Button-1>", lambda *args:createGame())
        container.Children += createGameButton

        
        self.Worker = Worker()

        # Create a new thread for connecting as trying to connect blocks the main thread
        Thread(target=self.TryConnection, daemon=True).start()

    def OnGameAcceptance(self,game):
        if game.Address == self.Worker.Address:
            
            return

        self.Worker.SendMessage({
            'type' : "GameAccepted",
            'data' : game.ToJson(),
            'addr' : game.Address
        })

    def CreateGameRequest(self, gameReq):
        self.GameRequestList.Add(gameReq)
        self.Worker.SendMessage({
            'type' : 'RequestCreation',
            'data' : gameReq
        })

    def TryConnection(self):
        if not self.Worker.ConnectToServer(): # This function returns True if it could connect successfully else it returns False
            self.OnConnectionError() 
        else:
            self.OnConnectionSuccess()

    def Destroy(self):
        super().Destroy()
        self.Worker.Close()

    def OnMessage(self, msg):
        print(msg)
        if msg['type'] == 'NewGameRequest':
            self.GameRequestList.Add(msg['data'])
        elif msg['type'] == 'CancelGameRequests':
            self.GameRequestList.Remove(msg['data'])
        elif msg['type'] == 'StartGame':
            self.Worker.Close()
            self.Window.Resources.Storage.OnlineMultiplayer['PeerAddress'] = msg['peerAddr']
            self.Window.Resources.Storage.OnlineMultiplayer['IsBoss'] = msg['boss']
            self.Window.Resources.Storage.OnlineMultiplayer['GameSettings'] = msg['data']['gameSettings']
            from ..Game import Document as Game
            self.Window.Document = Game
            return True
    
    def OnConnectionError(self):
        '''Called when we are unable to connect to the server'''
        pass

    def OnConnectionSuccess(self):
        '''Called when we succesfully connect to the server'''
        self.Worker.Listen(self.OnMessage,delay = 1)
        

        
