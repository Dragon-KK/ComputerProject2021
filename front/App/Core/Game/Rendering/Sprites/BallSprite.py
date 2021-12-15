from . import Sprite
from ....DataTypes.Standard import Vector
from ..Meshes import Circle

class BallSprite(Sprite):
    def __init__(self, Canvas, Radius):
        self.__Scale = Radius
        super().__init__(Canvas, Circle(
            Canvas,
            self.Scale,
            Vector(50,50),
            {
                'fill' : 'white'
            }
        ), Vector(50, 50), self.Scale)
        
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

