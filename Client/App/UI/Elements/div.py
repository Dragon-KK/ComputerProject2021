from ..Base import Element
from ...Core.DataTypes.Standard import Vector
class div(Element):
    def __init__(self,*args, **kwargs):
        kwargs['elemName'] = kwargs.get('elemName', 'div')
        super().__init__(*args, **kwargs)

    def _GetSpacialRectBox(self):
        # In the future if we want to do some automatic positioning
        w = self.ComputedStyles.Size.x
        h = self.ComputedStyles.Size.y
        x = self.ComputedStyles.TopLeft.x
        y = self.ComputedStyles.TopLeft.y
        return [
            Vector(x,y),
            Vector(x+w,y),
            Vector(x+w,y+h),
            Vector(x,y+h)
        ]

    

    def _Update(self):
        if self._CanvasID.div is None:return
        # Move our box
        self.Window.Document.coords(self._CanvasID.div,*self._GetVisualRectBox()) 

        # Item config our box           
        self.Window.Document.itemconfig(
            self._CanvasID.div,
            width=self.Styles.BorderStroke,
            outline=self.Styles.BorderColor,
            fill=self.Styles.BackgroundColor
        )

        

    def _Render(self):
        self._CanvasID.div = self.Window.Document.create_polygon(*self._GetVisualRectBox(),width=self.Styles.BorderStroke,outline=self.Styles.BorderColor,fill=self.Styles.BackgroundColor, smooth=True)
        
