from ..DataTypes.UI import Resource
from ..DataManagers import FileManager

class Storage(Resource):
    StorageFilePath = "Data/Storage.json"
    def __init__(self):
        super().__init__("Storage")
        self.__Data = {}

    def __getattr__(self, name):
        return self.__Data.get(name, {})

    def Unload(self):
        FileManager.WriteJson(self.StorageFilePath, self.__Data)

    def Load(self):
        self.__Data = FileManager.ReadJson(self.StorageFilePath)