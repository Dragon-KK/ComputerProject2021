from ..DataTypes.UI import Resource
from ..DataManagers import FileManager

class Audio(Resource):
    StorageFilePath = "Data/Audio.json"
    def __init__(self):
        super().__init__("Audio")
        self.__Data = {}

    def __getattr__(self, name):
        return self.__Data.get(name, {})

    def Unload(self):
        pass

    def LoadResources(self, name):
        pass

    def Load(self):
        pass