from .Engine import World
from . import Entities

class Pong:
    def __init__(
        self, 
        worldContainer, # The canvas component
        balls, # List of ball entities
        walls, # List of wall entities
        goals, # List of goal entities
        ):
        self.Canvas = worldContainer # Save worldContainer
        self.IsPaused = True

        self.World = World(self.Canvas) # Create World
        self.Balls = balls # Save balls
        self.Walls = walls # Save walls
        self.Goals = goals # Save goals

        # Add entities
        for ball in balls:self.World.Entities += ball
        for wall in walls:self.World.Entities += wall
        for goal in goals:self.World.Entities += goal

        self.Canvas.OnRender = self.InitializeGame # When the canvas has been rendered, initialize the game
        
    def TogglePause(self):
        if self.IsPaused:
            self.ContinueRound()
        else:
            self.PauseRound()

    def InitializeGame(self):
        self.World.InitializeWorld()

    def NewRound(self):
        for ball in self.Balls:ball.Reset()
        for wall in self.Walls:wall.Reset()
        for goal in self.Goals:goal.Reset()

    def ContinueRound(self):
        self.World.Continue()
        self.IsPaused = False

    def PauseRound(self):
        self.World.Pause()
        self.IsPaused = True

class LocalMultiplayerPong(Pong):
    def __init__(self, WorldContainer):
        super().__init__(
            WorldContainer,
            [Entities.Ball()],
            [],
            []
        )