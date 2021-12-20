from . import World,Physics
from . import Entities

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

        for ball in balls:self.World.Entities += ball
        for wall in walls:self.World.Entities += wall
        for goal in goals:self.World.Entities += goal

    def StartRound(self):
        pass

    def TogglePause(self):
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
    def __init__(self, container, settings, physicsDelay = 10, renderDelay = 15):

        balls = [
            Entities.Ball(10, 10)
        ]
        walls = [ ]
        goals = [ ]
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

        self.Physics = Physics(container, balls, walls, goals, physicsDelay)

    def ContinueRound(self):
        self.World.Continue()
        self.Physics.Continue()
        self.IsPaused = False

    def PauseRound(self):
        self.World.Pause()
        self.Physics.Pause()
        self.IsPaused = True