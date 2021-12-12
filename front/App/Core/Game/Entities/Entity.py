class Entity:
    '''Anything that is added to our game'''
    # Entity is one of the intersections between engine and ui

    def __init__(self, dynamic = False):
        self.Dynamic = dynamic
        self.Canvas = None
        self.Sprite = None

    def Render(self):
        pass

    def Remove(self):
        pass

    def Update(self,*args, **kwargs):
        '''Called every frame if its dynamic else called only when needed'''
        pass

    def _SetParent(self, canvas):
        self.Canvas = canvas