from ..Elements import div
from ..Base.Util import ComputeStyles
from ..Styles import Positions

class Sprite(div):
    '''
    All values are by default in % for Sprite (unless its em)
    '''
    def __init__(self, * args, **kwargs):
        super().__init__(*args,**kwargs)

    # TODO
    # Make this work
    # Maybe try changing the compute styles function?
