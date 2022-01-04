from ..DataTypes.UI import Resource
from ...Core.DataManagers import ImageManager, FileManager

class ImageList:
    def __init__(self, imgList):
        self.__Images = {}
        for key in imgList:
            self.__Images[key] = ImageManager.Load(imgList[key])
    
    def __getattr__(self, name):
        return self.__Images.get(name)

    def UnloadAll(self):
        for image in self.__Images.values():
            image.close()


class Images(Resource):
    StorageFilePath = "Data/Images.json"
    def __init__(self):
        super().__init__("Images")
        self.__ActiveResource = {}
        self.__Data = {}

    def __getattr__(self, name):
        return self.__ActiveResource.get(name)

    def Unload(self):
        for imagelist in self.__ActiveResource.values():
            imagelist.UnloadAll()

    def LoadResources(self, name):
        if name in self.__Data and name not in self.__ActiveResource:
            self.__ActiveResource[name] = ImageList(self.__Data[name])

    def UnloadResources(self, name):
        if name in self.__ActiveResource:
            self.__ActiveResource[name].UnloadAll()
            del self.__ActiveResource[name]

    def Load(self):
        self.__Data = FileManager.ReadJson(self.StorageFilePath)