from . import Entity
from ..Rendering.Sprites import BallSprite

class Ball(Entity):
    def __init__(self):
        super().__init__(dynamic=True, tag = "Ball")

    def _SetParent(self, canvas):
        self.Canvas = canvas
        self.Sprite = BallSprite(canvas, 20)

