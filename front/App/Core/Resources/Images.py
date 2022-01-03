from ..DataTypes.UI import Resource
from ..DataManagers import FileManager

class Images(Resource):
    StorageFilePath = "Data/Storage.json"
    def __init__(self):
        super().__init__("Images")
        self.__Data = {}

    def __getattr__(self, name):
        return self.__Data.get(name, {})

    def Unload(self):
        pass

    def Load(self):
        pass