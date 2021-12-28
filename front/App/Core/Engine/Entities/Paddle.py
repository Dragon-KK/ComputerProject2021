from ....UI.Components.Sprites import Rectangle
from ...DataTypes.Standard import Vector
from . import Entity

class Paddle(Entity):
    
    def __init__(self, initialPosition = ('50:w%', '50:h%')):
        '''Initial position of the'''
        super().__init__(Circle(Vector(0, 0), 5), dynamic=True, tag="Ball")

        self.Velocity = initialVelocity
        self.Acceleration = acceleration

        #self.Sprite.Styles.Set('Position', initialPosition) # Set the initial position of the ball

    # region Position
    @property
    def Position(self):
        return self.Sprite.Centre
    @Position.setter
    def Position(self, NewPosition):
        self.Sprite.Centre = NewPosition
    # endregion