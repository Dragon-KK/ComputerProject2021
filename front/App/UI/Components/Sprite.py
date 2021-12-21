from ..Elements import div
from ..Base.Util import ComputeStyles
from ..Styles import Positions

class Sprite(div):
    '''
    Basically a div just renamed for clarity
    '''
    def __init__(self, * args, **kwargs):
        super().__init__(*args,**kwargs)
