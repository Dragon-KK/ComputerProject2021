from . import Mesh
from ....DataTypes.Standard import Vector

class Circle(Mesh):
    def __init__(self, Canvas):
        super().__init__(Circle, Canvas, Radius, Centre, DrawingArguments = {})
        self.Radius = Radius
        self.Centre = Centre
        self.OldCentre = Centre
        self.DrawingArguments = DrawingArguments

    def Update(self):
        self.Canvas.UpdateItem(
            self.CanvasID,
            Displacement = self.Centre - self.OldCentre,
            # TODO
        )        

    def Draw(self):
        if self.CanvasID > 0:
            self.Canvas.Remove(self.CanvasID)
        self.CanvasID = self.Canvas.CreateCircle(self.Centre, self.Radius, **self.DrawingArguments)

    
