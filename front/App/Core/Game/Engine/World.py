from .DataTypes import EntityHolder
from . import Physics
from ...DataTypes.UI import Interval
from ...DataManagers import FileManager

class World:
    '''
    Handles the pong
    '''
    def __init__(self, GameContainer, physicsDelay = 15, renderDelay = 16):
        self.Canvas = GameContainer
        self.Entities = EntityHolder()
        self.Physics = Physics()
        self.EntityStyles = FileManager.ReadJson("Styles/GameGraphics.json")['Entities']

        

        self.PhysicsInterval = Interval(physicsDelay, self.PhysicsLoop)
        self.RenderInterval = Interval(renderDelay, self.RenderLoop)

    def Pause(self):
        self.Canvas.Window.Intervals -= self.PhysicsInterval
        self.Canvas.Window.Intervals -= self.RenderInterval

    def Continue(self):
        self.Canvas.Window.Intervals += self.RenderInterval
        self.Canvas.Window.Intervals += self.PhysicsInterval

    def InitializeWorld(self):
        for entity in self.Entities:
            self.Canvas.RegisterSprite(entity)
            entity.SetStyles(self.EntityStyles.get(entity.Tag, {}))

    def PhysicsLoop(self):
        print(1)

    def RenderLoop(self):
        for entity in self.Entities:
            entity.Update(OnlyDynamic = True)