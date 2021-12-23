from . import Sprite
from ....Core.DataTypes.Standard import Vector


# TODO
# Add functionality to Rectangle
# Start the physics : )

# NOT TESTED
class Rectangle(Sprite):
    """
    A Sprite with a rectangular shape
    Position must be given in em
    Size must be given in em
    Go to GameGraphics.json to change origin type etc for a certain Tag
    """
    def __init__(self, Position, Size, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._Radius = 5
        self._Centre = Vector(0, 0)

        # This part has possible redundancy
        self.Radius = radius # This will also be a property
        self.Centre = centre # This will be a property

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