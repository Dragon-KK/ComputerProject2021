from ...UI.Elements import ListBox


class GameItem:
    def __init__(self, Id, addr, name, gamesettings ,container):
        self.GameSettings = gamesettings
        self.Name = name
        self.Addr = addr
        self.Id = Id

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

class GameList:
    def __init__(self, container):
        self.Listbox = ListBox(classes = ".gameContainerListBox")
        container.Children += self.Listbox        

    def AddGames(self, games):
        pass

    def RemoveGames(self, games):
        pass