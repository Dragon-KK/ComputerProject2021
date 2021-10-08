from ...common.tools import Vector
from typing import List
class rect:
    '''
    size, position, origin
    '''
    def __init__(self, *args : List[Vector]):
        self.size = args[0] if len(args) > 0 else Vector(0,0)
        self.position = args[1] if len(args) > 1 else Vector(0,0)
        self.origin = args[2] if len(args) > 2 else Vector(0,0)