from . import Sprite
from ....Core.DataTypes.Standard import Vector

class Circle(Sprite):
    """
    A Sprite with a circular shape
    *Radius given will be in em
    """
    def __init__(self, centre, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._Radius = 5
        self._Centre = Vector(0, 0)

        # This part has possible redundancy
        self.Radius = radius # This will also be a property
        self.Centre = centre # This will be a property



    
    # region Radius
    @property
    def Radius(self):
        """The Radius property."""
        return self._Radius
    @Radius.setter
    def Radius(self, value):
        self._Radius = value
        self.Styles.Set("Size", (f"{self._Radius * 2}:em", f"{self._Radius * 2}:em"), update=False)
    # endregion

    # region Centre
    @property
    def Centre(self):
        return self._Centre
    @Centre.setter
    def Centre(self, value):
        self.Displacement += value - self._Centre
        self._Centre = value
        self.Styles.Set("Position", (f"{self._Centre.x}:em", f"{self._Centre.y}:em"), update=False)
        
    # end Region

    def __CreateCircle(self):
        return self.Window.Document.create_oval(self.ComputedStyles.TopLeft.x ,self.ComputedStyles.TopLeft.y, self.ComputedStyles.TopLeft.x + self.ComputedStyles.Size.x , self.ComputedStyles.TopLeft.y + self.ComputedStyles.Size.y, fill = self.Styles.BackgroundColor, width = self.Styles.BorderStroke, outline = self.Styles.BorderColor)

    def _Render(self):
        self._CanvasIDs += self.__CreateCircle()


    def _Update(self, updateRender = True):
        if updateRender:
            _id = self._CanvasIDs.list[0] # The canvas id of our circle
            self.Window.Document.coords(
                _id,
                self.ComputedStyles.TopLeft.x, self.ComputedStyles.TopLeft.y, 
                self.ComputedStyles.TopLeft.x + self.ComputedStyles.Size.x, self.ComputedStyles.TopLeft.y + self.ComputedStyles.Size.y
            )