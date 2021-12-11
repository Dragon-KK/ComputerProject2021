from . import Sprite
from ..Meshes import Circle

class Ball(Sprite):
    def __init__(self, Canvas):
        super().__init__(Canvas, Circle(Canvas))

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

