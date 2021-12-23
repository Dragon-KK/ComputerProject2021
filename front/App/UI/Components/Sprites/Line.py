from . import Sprite
from ....Core.DataTypes.Standard import Vector

# NOT TESTED
class Line(Sprite):
    """
    Tis but a line
    * Right now the line doesnt have any way to change its orientation when set just resize and move up and down
    * We really dont need something like that right now anyways
    """
    def __init__(self, P1, P2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arg = arg

        self.P1 = P1
        self.P2 = P2

        self.Styles.Set("Size" , (f"{P2.x - P1.x}:em", f"{P2.y - P1.y}:em"), update=False)

        self.Position = P1 # Posible redundancy

    @property
    def Position(self):
        """The Position property."""
        return self.P1
    @Position.setter
    def Position(self, value):
       self.Displacement += value - self.P1
       self.P2 += value - self.P1
       self.P1 = value
       self.Styles.Set("Position", (f"{P1.x}:em", f"{P1.y}:em"))


        