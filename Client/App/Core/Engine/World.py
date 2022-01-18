from ..DataTypes.Game import EntityHolder
from ..DataManagers import FileManager
from ..DataTypes.UI import Interval

class World:
    '''
    Basically just does the rendering
    '''
    StyleSheet = "Styles/GameGraphics.json"
    def __init__(self, worldContainer, renderDelay = 15):
        self.__RenderInterval = Interval(renderDelay, self.Render)
        self.WorldContainer = worldContainer
        self.Entities = EntityHolder(worldContainer,Styles = FileManager.ReadJson(self.StyleSheet)['Entities'])

    def Initialize(self):
        for entity in self.Entities:
            entity.Initialize()

    def Continue(self):
        self.WorldContainer.Window.Intervals += self.__RenderInterval

    def Pause(self):
        self.WorldContainer.Window.Intervals -= self.__RenderInterval

    def Render(self):
        for entity in self.Entities:
            entity.Render()