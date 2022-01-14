from . import Entity
from ...DataTypes.Standard import Vector
from ....UI.CustomElements.Sprites import EmptySprite

class Wall(Entity):
    
    def __init__(self,P1, P2, *args, horizontal = True, **kwargs):
        super().__init__(EmptySprite(), dynamic=False, tag="Wall")

        self.IsHorizontal = horizontal
        self.P1 = P1
        self.P2 = P2

