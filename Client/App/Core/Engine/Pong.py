from . import World,Physics
from . import Entities
from ..DataTypes.Standard import Vector
from ..DataTypes.Physics import EulersVector
from .Helpers import LocalMultiplayer,Arcade
from random import randint
class Pong:
    '''
    Deals with world physics and adding entitites
    '''
    def __init__(
        self,
        worldContainer,
        gameSettings, # Settings
        paddles = [],
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
        for paddle in paddles:self.World.Entities += paddle

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
    def __init__(self, container, settings, physicsDelay = 10, renderDelay = 15, onGoal = lambda winner="":0):

        #region Random Velocity
        def PlusMinus(n):
            tmp = randint(0, 1)
            return n* (-1 if tmp else 1)
        def GetRandomDirection():
            return Vector(PlusMinus(randint(5, 10)), PlusMinus(randint(2,7))).normalized()
        def GetRandomVelocity():
            
            return EulersVector(magnitude=settings.Difficulty, direction=GetRandomDirection())
        # endregion

        
        balls = [
            Entities.Ball(GetRandomVelocity, settings.DifficultySlope,initialPosition=Vector(50, 25.625)) for _ in range(settings.BallCount)
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
        paddles = [
            Entities.Paddle(Vector(2, 25.625), Vector(2, 10), Entities.Paddle.OrientationTypes.Left, name = "LeftPaddle"),
            Entities.Paddle(Vector(98, 25.625), Vector(2, 10), Entities.Paddle.OrientationTypes.Right, name = "RightPaddle"),
        ]

        super().__init__(
            container, 
            settings,
            paddles = paddles,
            walls = walls,
            goals = goals,
            balls = balls,
            renderDelay=renderDelay
        )
    	
        self.Physics = Physics(container, balls, walls, goals,paddles, physicsDelay, self.OnGoal)
        self.Score  = [0, 0]
        self.OnGoalCallback = onGoal
        self.InputManager = LocalMultiplayer.InputManager(container,paddles)
        self.Settings = settings

    def ContinueRound(self):
        self.InputManager.Continue()
        self.World.Continue()
        self.Physics.Continue()
        self.IsPaused = False

    def CheckForWinner(self):
        if self.Score[1] >= self.Settings.WinCondition and (not self.Settings.Duece or self.Score[1] - self.Score[0] > 1):
            return "Player2"
        elif self.Score[0] >= self.Settings.WinCondition and (not self.Settings.Duece or self.Score[0] - self.Score[1] > 1):
            return "Player1"
        else:
            return ""

    def OnGoal(self, goal):
        self.PauseRound()
        self.World.Render() # Soemtimes the world misses a render 
        self.RoundHasStarted = False
        if goal.GoalName == "P1Goal":
            self.Score[0] += 1
        elif goal.GoalName == "P2Goal":
            self.Score[1] += 1

        self.OnGoalCallback(winner = self.CheckForWinner())

    def PauseRound(self):
        self.World.Pause()
        self.InputManager.Pause()
        self.Physics.Pause()
        self.IsPaused = True

class ArcadePong(Pong):
    def __init__(self, container, settings, physicsDelay = 10, renderDelay = 15, onGoal = lambda:0):

        #region Random Velocity
        def PlusMinus(n):
            tmp = randint(0, 1)
            return n* (-1 if tmp else 1)
        def GetRandomDirection():
            return Vector(PlusMinus(randint(5, 10)), PlusMinus(randint(1,6))).normalized()
        def GetRandomVelocity():            
            return EulersVector(magnitude=settings.Difficulty, direction=GetRandomDirection())
        # endregion

        
        balls = [
            Entities.Ball(GetRandomVelocity, settings.DifficultySlope,initialPosition=Vector(50, 25.625)) for _ in range(settings.BallCount)
        ]
        walls = [
            Entities.Wall( # The horizontal wall on top
                Vector(0, 0),Vector(100, 0)
            ),
            Entities.Wall( # The horizontal wall on bottom
                Vector(0, 51.25),Vector(100, 51.25)
            ),
            Entities.Wall( # The wall on the right
                Vector(100, 0), Vector(100, 51.25),horizontal=False
            )
        ]
        goals = [
            Entities.Goal( # The goal on the left
                Vector(0, 0), Vector(0, 51.25),
                "P2Goal"
            )        
        ]
        paddles = [
            Entities.Paddle(Vector(2, 25.625), Vector(2, 10), Entities.Paddle.OrientationTypes.Left, name = "LeftPaddle")
        ]

        super().__init__(
            container, 
            settings,
            paddles = paddles,
            walls = walls,
            goals = goals,
            balls = balls,
            renderDelay=renderDelay
        )
    	
        self.Physics = Physics(container, balls, walls, goals,paddles, physicsDelay, self.OnGoal)
        self.Score  = [0, 0]
        self.OnGoalCallback = onGoal
        self.InputManager = Arcade.InputManager(container,paddles[0])
        self.Settings = settings

    def ContinueRound(self):
        self.InputManager.Continue()
        self.World.Continue()
        self.Physics.Continue()
        self.IsPaused = False

    def OnGoal(self, goal):
        self.PauseRound()
        self.World.Render() # Soemtimes the world misses a render 
        self.RoundHasStarted = False

        self.OnGoalCallback()

    def PauseRound(self):
        self.World.Pause()
        self.InputManager.Pause()
        self.Physics.Pause()
        self.IsPaused = True


class OnlineMultiplayerPong(Pong):
    def __init__(self, container, settings, physicsDelay = 10, renderDelay = 15, onGoal = lambda winner="":0):

        #region Random Velocity
        def PlusMinus(n):
            tmp = randint(0, 1)
            return n* (-1 if tmp else 1)
        def GetRandomDirection():
            return Vector(7,3).normalized()
        def GetRandomVelocity():            
            return EulersVector(magnitude=settings.Difficulty, direction=GetRandomDirection())
        # endregion

        
        balls = [
            Entities.Ball(GetRandomVelocity, settings.DifficultySlope,initialPosition=Vector(50, 25.625))
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
        paddles = [
            Entities.Paddle(Vector(2, 25.625), Vector(2, 10), Entities.Paddle.OrientationTypes.Left, name = "LeftPaddle"),
            Entities.Paddle(Vector(98, 25.625), Vector(2, 10), Entities.Paddle.OrientationTypes.Right, name = "RightPaddle"),
        ]

        super().__init__(
            container, 
            settings,
            paddles = paddles,
            walls = walls,
            goals = goals,
            balls = balls,
            renderDelay=renderDelay
        )
    	
        self.Physics = Physics(container, balls, walls, goals,paddles, physicsDelay, self.OnGoal)
        self.Score  = [0, 0]
        self.OnGoalCallback = onGoal
        self.InputManager = LocalMultiplayer.InputManager(container,paddles)
        self.Settings = settings

    def ContinueRound(self):
        self.InputManager.Continue()
        self.World.Continue()
        self.Physics.Continue()
        self.IsPaused = False

    def CheckForWinner(self):
        if self.Score[1] >= self.Settings.WinCondition and (not self.Settings.Duece or self.Score[1] - self.Score[0] > 1):
            return "Player2"
        elif self.Score[0] >= self.Settings.WinCondition and (not self.Settings.Duece or self.Score[0] - self.Score[1] > 1):
            return "Player1"
        else:
            return ""

    def Reset(self):
        for entity in self.World.Entities:
            entity.Reset()

    def StartRound(self):
        for entity in self.World.Entities:
            entity.Reset()
        self.RoundHasStarted = True
        self.ContinueRound()

    def OnGoal(self, goal):
        self.PauseRound()
        self.World.Render() # Soemtimes the world misses a render 
        self.RoundHasStarted = False
        if goal.GoalName == "P1Goal":
            self.Score[0] += 1
        elif goal.GoalName == "P2Goal":
            self.Score[1] += 1

        self.OnGoalCallback(winner = self.CheckForWinner())