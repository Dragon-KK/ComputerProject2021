from ..DataTypes.Game import EntityHolder
from ..DataManagers import FileManager

class World:
    '''
    Basically just does the rendering
    '''
    StyleSheet = "Styles/GameGraphics.json"
    def __init__(self, worldContainer):
        self.Entities = EntityHolder(worldContainer,Styles = FileManager.ReadJson(self.StyleSheet)['Entities'])

    def Initialize(self):
        for entity in self.Entities:
            entity.Initialize()

    def Render(self):
        for entity in self.Entities:
            entity.Render()

    def GetImage(self):
        pass

    def UpdateImage(self, image):
        pass