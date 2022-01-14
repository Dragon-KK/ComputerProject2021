from ..Elements import div
from ..Helper import ComputedStyles

class AspectRatioPreservedContainer(div):
    '''
    AspectRatioPreservedDiv will try to fill its parent as much as it can while preserving aspect ratio
    Aspect ratio = width/height
    '''
    def __init__(self, * args, aspectRatio = 16 / 9,**kwargs):
        kwargs['elemName'] = kwargs.get('elemName', 'AspectRatioPreservedContainer')
        super().__init__(*args,**kwargs)
        self.AspectRatio = aspectRatio

    def ComputeStyles(self):

        parentSize = self.Parent.ComputedStyles.Size  # Our size will always try to be 100%
        mySize = (0,0)
        if parentSize.x/parentSize.y > self.AspectRatio: # If x value is too much
            mySize = (parentSize.y * self.AspectRatio, parentSize.y )# Adjust based on aspect ratio
        else:
            mySize = (parentSize.x , parentSize.x / self.AspectRatio )# Adjust based on aspect ratio

        self.Styles.Size = mySize
        self._ComputedStyles = ComputedStyles.FromStyles(self.Styles, self) # Compute our styles

    def _GetStyleUnits(self):
        # Aspect ratio conserved div acts as za em container thing thingy
        return {'em':self.ComputedStyles.Size.x / 100}

        


