class shape:
    def __init__(self, _type):
        self.type = _type
        self.canvasID = -1

class line(shape):
    """This is a line"""
    def __init__(self,p1,p2,absolute = False,color = 'white', size = 5, dash = None):
        super().__init__('line')
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.size = size
        self.dash = dash
        self.absolute = absolute

    def update(self,p1=None,p2 = None, absolute = False,color = 'white', size = 5, dash = None):

        pass
        
    
        
        