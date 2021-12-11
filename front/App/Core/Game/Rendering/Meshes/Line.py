from . import Mesh

class Line(Mesh):
    def __init__(self, Canvas):
        super().__init__(Circle, Canvas)

    def Draw(self):
        pass