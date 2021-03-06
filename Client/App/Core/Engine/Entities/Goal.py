from . import Entity
from ...DataTypes.Standard import Vector
from ....UI.CustomElements.Sprites import EmptySprite

class Goal(Entity):
    
    def __init__(self,P1, P2,name, *args, horizontal = False, **kwargs):
        super().__init__(EmptySprite(), dynamic=False, tag="Goal")

        self.IsHorizontal = horizontal
        self.P1 = P1
        self.P2 = P2

        self.GoalName = name

