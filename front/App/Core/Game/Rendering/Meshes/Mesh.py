from ....DataTypes.Standard import Vector

class Mesh:
    def __init__(self, _type, Canvas):
        self.Type = _type
        self.Canvas = Canvas
        self.CanvasID = -1
        self.Bounds = [ Vector(0, 0), Vector(0, 0), Vector(0, 0), Vector(0, 0)] # Every shape must have 4 marking points

    def Draw(self, *args, **kwargs):
        '''Draws the mesh'''
        pass