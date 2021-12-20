from ..Elements import div
from ..Base.Util import ComputeStyles
from ..Styles import Positions

class Sprite(div):
    '''
    Basically a div just renamed for clarity
    '''
    def __init__(self, * args, **kwargs):
        super().__init__(*args,**kwargs)
        
    def Update(self, propogationDepth=0, ReRender=True):
        self.ComputeStyles()
        self._Update(updateRender=ReRender)  # In case an inherited class has to do some extra stuff on update

        # That update glitch only seems to happen when the element has children but since sprites dont have children we dont need to double update

