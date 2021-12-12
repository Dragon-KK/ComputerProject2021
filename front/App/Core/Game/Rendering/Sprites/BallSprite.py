from . import Sprite
from ..Meshes import Circle

class BallSprite(Sprite):
    def __init__(self, Canvas):
        super().__init__(Canvas, Circle(Canvas,10,(0,0)),(0,0),2)

    def Draw(self):
        self.Mesh.Draw()
    
    @property
    def Position(self):
        return self.__Position
    @Position.setter
    def Position(self, newPos):
        self.__Position = newPos

    @property
    def Scale(self):
        return self.__Scale
    @Scale.setter
    def Scale(self, newScale):
        self.__Scale = newScale

