from ..Elements import div
from ..Base.Util import ComputeStyles
from ..Styles import Positions

class AspectRatioPreservedContainer(div):
    '''
    AspectRatioPreservedDiv will try to fill its parent as much as it can while preserving aspect ratio
    Aspect ratio = width/height
    '''
    def __init__(self, * args, aspectRatio = 1,**kwargs):
        super().__init__(*args,**kwargs)

        self.AspectRatio = aspectRatio

    def __SetPositionToCentre(self,oldSize, newSize):
        self._ComputedStyles.TopLeft += (oldSize - newSize) / 2
        self._ComputedStyles.Position += (oldSize - newSize) / 2

    def ComputeStyles(self):

        self._Styles.Size = ("100:w%", "100:h%") # Our size will always try to be 100%
        self._Styles.OriginType = Positions.Centre # Our position will always be at the centre
        self._Styles.Position = ("50:w%", "50:h%") # Always at the centre
        self._ComputedStyles = ComputeStyles(self.Styles, self) # Compute our styles

        ourSize = self._ComputedStyles.Size

        if ourSize.x/ourSize.y > self.AspectRatio: # If x value is too much
            old = self._ComputedStyles.Size + (0,0) # This is just to create a new vector obj otherwise old would point to new
            self._ComputedStyles.Size.x = ourSize.y * self.AspectRatio # Adjust based on aspect ratio
            self.__SetPositionToCentre(old, self._ComputedStyles.Size) # Reposition it to the centre
        else:
            old = self._ComputedStyles.Size + (0,0) # Same deal as previous block
            self._ComputedStyles.Size.y = ourSize.x / self.AspectRatio
            self.__SetPositionToCentre(old, self._ComputedStyles.Size)


