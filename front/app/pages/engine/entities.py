from . import drawing as shapes
from ...common.tools import Vector


class Ball:
    def __init__(self,arena, radius = '10:px', color = 'white', fill = 'white'):
        self.itemID = arena.registerItem(
            shapes.circle(
                Vector('50:w%','50:h%'), radius,
                color = color,
                fill = 'white'
            )
        )


class Player:
    def __init__(self):
        pass

class Wall:
    def __init__(self, arena):
        self.itemID = arena.registerItem(
            shapes.line(
                Vector('25:vw', '0:vh'),
                Vector('50:vw', '100:vh'),
                absolute = True,
                size = 2,
                color = "white"
            )
        )

class WinZone(Wall):
    def __init__(self):
        pass