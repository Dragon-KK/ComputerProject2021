from .Standard import Vector

class EulersVector:
    def __init__(self, magnitude = 1, direction = Vector(1, 0)):
        self.Magnitude = magnitude
        self.Direction = direction

class Collision:
    def __init__(self, body, pointOfCollision):
        self.CollidingBody = body # The entity that the ball collided with
        self.PointOfCollision = pointOfCollision # The point of collision