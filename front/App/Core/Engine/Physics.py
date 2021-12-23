from .Util import Time
from ..DataTypes.UI import Interval
from ..DataTypes.Standard import Vector

class Physics:
    
    def __init__(self,canvas, balls, walls, goals, physicsDelay):
        self.__PhysicsInterval = Interval(physicsDelay, self.PhysicsLoop)

        self.Canvas = canvas

        self.Balls = balls
        self.Walls = walls
        self.Goals = goals

        self.Time = Time()



    def PhysicsLoop(self):
        # TODO
        dt = self.Time.DeltaTime # I say dt but its more of a correction constant at this point ideally this will be removed when position is based on %
        # Use the same next colliding wall business we used in v2
        self.Balls[0].Position += Vector(10,10) * dt

    def Continue(self):
        self.Canvas.Window.Intervals += self.__PhysicsInterval

    def Pause(self):
        self.Canvas.Window.Intervals -= self.__PhysicsInterval
        self.Time.DeltaTime = 0