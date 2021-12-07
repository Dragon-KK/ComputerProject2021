from ...common.tools import Vector
class options:
    default = 0x00
    absolute = 0x01
    relative = 0x02
    flex = 0x03
    grid = 0x04
    block = 0x05

    @staticmethod
    def getOption(id):
        if type(id) != int:return id
        return ['default', 'absolute', 'relative', 'flex', 'grid', 'block'][id]

class css:
    def __init__(self):
        self.origin = Vector(0, 0)
        self.position = options.default
        self.display = options.default
        self.grid = {}
        self.flex = {}
        self.width = '0:px'
        self.height = '0:px'
        self.border = { 'color' : None, 'size' : 0, 'radius' : 0,'dash' : None}
        self.padding = {}
        self.background = {'color' : None}
        self.font = {'color' : 'black', 'size' : 5, 'style': 'ariel'}
        self.margin = {}
        self.top = None
        self.left = None
        self.bottom = None
        self.right = None
        self.zIndex = 1

        self.attrs = [
            'origin',
            'position',
            'display',
            'grid',
            'flex',
            'width',
            'height',
            'border',
            'padding',
            'margin',
            'top',
            'left',
            'bottom',
            'right',
            'background',
            'font',
            'zIndex' 
        ]

    def set(self, **kwargs):
        for i in kwargs:
            if i in self.attrs:
                if type(kwargs[i]) == dict and type(self.__getattribute__(i)) == dict:
                    self.__getattribute__(i).update(kwargs[i])
                else:
                    self.__setattr__( i, kwargs[i])

        
    def __repr__(self):
        res = {}
        for i in self.attrs:
            res[i] = options.getOption(self.__getattribute__(i))
        return repr(res)

    

