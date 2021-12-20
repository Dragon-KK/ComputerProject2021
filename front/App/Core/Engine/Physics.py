from ..DataTypes.UI import Interval
from ..DataTypes.Standard import Vector

class Physics:
    
    def __init__(self,canvas, balls, walls, goals, physicsDelay):
        self.__PhysicsInterval = Interval(physicsDelay, self.PhysicsLoop)

        self.Canvas = canvas

        self.Balls = balls
        self.Walls = walls
        self.Goals = goals

    def PhysicsLoop(self):
        # Use the same next colliding wall business we used in v2
        self.Balls[0].Position += Vector(1,0)

    def Continue(self):
        self.Canvas.Window.Intervals += self.__PhysicsInterval

    def Pause(self):
        self.Canvas.Window.Intervals -= self.__PhysicsInterval