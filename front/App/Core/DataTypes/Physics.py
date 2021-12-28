from .Standard import Vector

class EulersVector:
    def __init__(self, magnitude = 1, direction = Vector(1, 0)):
        self.Magnitude = magnitude
        self.Direction = direction

class Collision:
    def __init__(self, body, fuelSpent):
        self.CollidingBody = body # The entity that the ball collided with
        self.FuelSpent = fuelSpent # The amount of fuel spent to reach the point of collision (Refer to Engine/Physics.py for what fuel is)