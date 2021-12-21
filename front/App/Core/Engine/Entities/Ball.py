from ....UI.Components import Sprite
from . import Entity

class Ball(Entity):
    
    def __init__(self, initialVelocity, acceleration, initialPosition = ('50:w%', '50:h%')):
        '''Initial position of the'''
        super().__init__(Sprite(), dynamic=True, tag="Ball")

        self.Velocity = initialVelocity
        self.Acceleration = acceleration

        #self.Sprite.Styles.Set('Position', initialPosition) # Set the initial position of the ball

    # region Position
    @property
    def Position(self):
        return self.Sprite.ComputedStyles.Position
    @Position.setter
    def Position(self, NewPosition):
            
        self.Sprite.Styles.Set("Position", (NewPosition.x, NewPosition.y), update = False)
    # endregion