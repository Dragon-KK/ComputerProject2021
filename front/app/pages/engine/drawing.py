from ...common.tools import Vector
# :D
class shape:
    def __init__(self, _type, **kwargs):
        print(kwargs,_type)
        self.type = _type
        self.canvasID = -1
        self.init = kwargs.get('init',self.init)

    def init(self):
        pass

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
        self.absoluteInfo = {'p1' : Vector(0, 0), 'p2': Vector(0, 0)}

    def update(self,**kwargs):
        for i in kwargs:
            self.__setattr__(i, kwargs[i])

class circle(shape):
    """This is a circle"""
    def __init__(self, c, r,absolute = False,color = 'white', size = 5, dash = None,fill = 'white',**kwargs):
        super().__init__('circle',**kwargs)
        self.c = c
        self.r = r
        self.color = color
        self.size = size
        self.dash = dash
        self.absolute = absolute
        self.absoluteInfo = {'position' : Vector(0,0),'radius' : 0} 
        self.fill = fill

    def update(self,c = None,r = None,color = 'white', size = 5, dash = None,fill = 'white'):
        if c:self.c = c
        if r:self.r = r
        self.color = color
        self.size = size
        self.dash = dash
        self.absolute = absolute
        self.fill = fill
        

        
    
        
        