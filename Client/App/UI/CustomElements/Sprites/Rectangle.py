from . import Sprite
from ....Core.DataTypes.Standard import Vector


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

        self.Size = Size
        self._Position = Position
        self.Position = Position # This will be a property

    # region Position
    @property
    def Position(self):
        return self._Position
    @Position.setter
    def Position(self, value):
        self.Displacement += value - self._Position
        self._Position = value
        self.Styles.Position = (f"{self._Position.x}:em", f"{self._Position.y}:em")    
    # end Region
    # region Size
    @property
    def Size(self):
        return self._Size
    @Size.setter
    def Size(self, value):
        self._Size = value
        self.Styles.Size = (f"{self._Size.x}:em", f"{self._Size.y}:em")       
    # end Region