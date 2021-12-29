from . import World,Physics
from . import Entities
from ..DataTypes.Standard import Vector
from ..DataTypes.Physics import EulersVector
from random import randint
class Pong:
    '''
    Deals with world physics and adding entitites
    '''
    def __init__(
        self,
        worldContainer,
        gameSettings, # Settings
        players = [],
        balls = [], 
        walls = [],
        goals = [],

        renderDelay = 15
        ):
        self.World = World(worldContainer, renderDelay=renderDelay)

        self.IsPaused = True
        self.RoundHasStarted = False

        for ball in balls:self.World.Entities += ball
        for wall in walls:self.World.Entities += wall
        for goal in goals:self.World.Entities += goal

    def StartRound(self):
        for entity in self.World.Entities:
            entity.Reset()
        self.RoundHasStarted = True
        self.ContinueRound()


    def TogglePause(self):
        if not self.RoundHasStarted:return
        if self.IsPaused:
            self.ContinueRound()
        else:
            self.PauseRound()

    def ContinueRound(self):
        self.World.Continue()
        self.IsPaused = False

    def PauseRound(self):
        self.World.Pause()
        self.IsPaused = True



class LocalMultiplayerPong(Pong):
    def __init__(self, container, settings, physicsDelay = 10, renderDelay = 15, onGoal = lambda:0):
        def PlusMinus(n):
            tmp = randint(0, 1)
            return n* (-1 if tmp else 1)
        def GetRandomDirection():
            return Vector(PlusMinus(randint(5, 10)), PlusMinus(randint(2,7))).normalized()
        def GetRandomVelocity():
            return EulersVector(magnitude=100, direction=GetRandomDirection())
        balls = [
            Entities.Ball(GetRandomVelocity, 0)
        ]
        walls = [
            Entities.Wall( # The horizontal wall on top
                Vector(0, 0),Vector(100, 0)
            ),
            Entities.Wall( # The horizontal wall on bottom
                Vector(0, 51.25),Vector(100, 51.25)
            )
        ]
        goals = [
            Entities.Goal( # The goal on the left
                Vector(0, 0), Vector(0, 51.25),
                "P2Goal"
            ),
            Entities.Goal( # The goal on the right
                Vector(100, 0), Vector(100, 51.25),
                "P1Goal"
            )
        ]
        players = ()

        super().__init__(
            container, 
            settings,
            players = players,
            walls = walls,
            goals = goals,
            balls = balls,
            renderDelay=renderDelay
        )
    	
        self.Physics = Physics(container, balls, walls, goals, physicsDelay, self.OnGoal)
        self.Score  = [0, 0]
        self.OnGoalCallback = onGoal

    def ContinueRound(self):
        self.World.Continue()
        self.Physics.Continue()
        self.IsPaused = False

    def OnGoal(self, goal):
        self.PauseRound()
        self.RoundHasStarted = False
        if goal.GoalName == "P1Goal":
            self.Score[0] += 1
        elif goal.GoalName == "P2Goal":
            self.Score[1] += 1
        self.OnGoalCallback()

    def PauseRound(self):
        self.World.Pause()
        self.Physics.Pause()
        self.IsPaused = True