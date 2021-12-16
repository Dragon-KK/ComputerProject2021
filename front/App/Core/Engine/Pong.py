from . import World
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

        renderDelay = 15,
        physicsDelay = 10
        ):
        self.World = World(worldContainer)

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

    '''
    Idea :
        Isolate updating renders completely
        Just takes in list of entities and renders them

    World has jsonify and dejsonify inbuilt
    players are just entities
    Pong class doesnt store anything it just acts as the medium

    ** The entities itself just contain stuff they arent really doing any logic by themselves, physics will handle everything **
    '''

class LocalMultiplayerPong(Pong):
    def __init__(self, container, settings):
        super().__init__(
            container, 
            settings,
            players = [],
            walls = [],
            goals = [],
            balls = [
                Entities.Ball(10, 10)
            ]
        )