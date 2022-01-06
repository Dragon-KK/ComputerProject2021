from ..Base import Element
from ...Core.DataTypes.Standard import Vector
class div(Element):
    def __init__(self,*args, **kwargs):
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

    def _GetVisualRectBox(self):
        w = self.ComputedStyles.Size.x
        h = self.ComputedStyles.Size.y
        x = self.ComputedStyles.TopLeft.x
        y = self.ComputedStyles.TopLeft.y
        r1,r2,r3,r4 = self.ComputedStyles.CornerRadius

        # Putting the points 2 times seemw to give slightly better results
        return [
            x+r1, y,
            x+r1, y,
            x + w - r2, y,
            x + w - r2, y,
            x + w, y,
            x + w, y + r2,
            x + w, y + r2,
            x + w, y + h - r3,
            x + w, y + h - r3,
            x + w, y + h,
            x + w- r3, y + h,
            x + w- r3, y + h,
            x + r4, y + h,
            x + r4, y + h,
            x, y + h,
            x, y + h - r4,
            x, y + h - r4,
            x, y + r1,
            x, y + r1,
            x, y
        ]

    def _Update(self, updateRender = True):
        if updateRender:
            boxID = self._CanvasIDs.list[0]
            # Move our box
            self.Window.Document.coords(boxID,*self._GetVisualRectBox()) 

            # Item config our box           
            self.Window.Document.itemconfig(
                boxID,
                width=self.Styles.BorderStroke,
                outline=self.Styles.BorderColor,
                fill=self.Styles.BackgroundColor
            )

    def _Render(self):
        self._CanvasIDs += self.Window.Document.create_polygon(self._GetVisualRectBox(),width=self.Styles.BorderStroke,outline=self.Styles.BorderColor,fill=self.Styles.BackgroundColor, smooth=True)