from ...Elements import div
from ....Core.DataTypes.Standard import Vector

class Sprite(div):
    '''    
    Everything shall be in em : )
    '''
    def __init__(self, * args, **kwargs):
        super().__init__(*args,**kwargs)

        self.Displacement = Vector(0, 0) # The amount the sprite has moved since last frameupdate

        # Since upates are going to be called like every few milliseconds for sprites we want a less needy update function

    def FrameUpdate(self):
        '''
        Just changes the position according to displacement. For proper proper update call Update itself (Sprite update is automatically called on resize and all : ) )
        '''
        for item in self._CanvasID.ALLNOEXCEPTION:
            self.Window.Document.move(item, self.Displacement.x * self.STYLE_UNITS['em'], self.Displacement.y * self.STYLE_UNITS['em'])

        self.Displacement = Vector(0, 0)