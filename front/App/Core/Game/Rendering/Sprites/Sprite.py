class Sprite:
    '''Something that can be drawn into the world'''

    def __init__(self, Canvas, Mesh, Position, Scale):
        self.Mesh = Mesh
        self.Canvas = Canvas
        self.__Position = Position
        self.__Scale = Scale

    def Render(self):
        self.Mesh.Render()

    def Remove(self):
        self.Mesh.Remove()
    
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