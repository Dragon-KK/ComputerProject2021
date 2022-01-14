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
        self.__ActiveResource = None
        self.__Data = {}

    def __getattr__(self, name):
        return self.__ActiveResource.__getattr__(name)

    def Unload(self):
        if self.__ActiveResource:self.__ActiveResource.UnloadAll()

    def LoadResources(self, name):
        if name in self.__Data:
            self.__ActiveResource = ImageList(self.__Data[name])

    def UnloadResources(self, name):
        if self.__ActiveResource:
            self.__ActiveResource.UnloadAll()
            self.__ActiveResource = None

    def Load(self):
        self.__Data = FileManager.ReadJson(self.StorageFilePath)