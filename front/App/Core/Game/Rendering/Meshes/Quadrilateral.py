from . import Mesh

class Quadrilateral(Mesh):
    def __init__(self, Canvas):
        super().__init__(Circle, Canvas)

    def Draw(self):
        pass