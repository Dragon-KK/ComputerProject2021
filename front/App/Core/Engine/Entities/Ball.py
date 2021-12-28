from ....UI.Components.Sprites import Circle
from ...DataTypes.Standard import Vector
from . import Entity

class Ball(Entity):
    def __init__(self, initialVelocity, acceleration, initialPosition = Vector(50, 24), radius = 1):
        '''Initial position of the ball is by default the centre of the arena'''
        super().__init__(Circle(initialPosition, radius), dynamic=True, tag="Ball")

        self.Velocity = initialVelocity # A Euler Velocity (refer to DataTypes/Physics.py)
        self.Acceleration = acceleration # A number

        self.Radius = radius

        self.NextCollidingStaticBody = None # The next wall / goal the ball will collide with (unless it collides with a paddle)
        self.PredictedCollisionPoint = Vector(0, 0) # The point of collision

    # region Position
    @property
    def Position(self):
        return self.Sprite.Centre
    @Position.setter
    def Position(self, NewPosition):
        self.Sprite.Centre = NewPosition
    # endregion