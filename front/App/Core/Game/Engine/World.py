from .DataTypes import EntityHolder

class World:
    '''
    Handles the pong
    '''
    def __init__(self, GameContainer):
        self.Canvas = GameContainer
        self.Entities = EntityHolder()

    def InitializeWorld(self):
        for entity in self.Entities:
            self.Canvas.RegisterSprite(entity)

    def PhysicsLoop(self):
        pass

    def RenderLoop(self):
        pass