from .Standard import Vector

class EulersVector:
    def __init__(self, magnitude = 1, direction = Vector(0, 1)):
        self.Magnitude = magnitude
        self.Direction = direction