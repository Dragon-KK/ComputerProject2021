from . import Sprite

class EmptySprite(Sprite):
    def __init__(self):
        super().__init__()

    def _Render(*args, **kwargs):return
    def _Update(*args, **kwargs):return