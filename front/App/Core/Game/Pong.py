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
        self.Canvas = worldContainer
        self.World = World(self.Canvas)
        self.Balls = balls
        self.Walls = walls
        self.Goals = goals
        for ball in balls:self.World.Entities += ball
        for wall in walls:self.World.Entities += wall
        for goal in goals:self.World.Entities += goal

        self.Canvas.OnRender = self.InitializeGame
        

    def InitializeGame(self):
        self.World.InitializeWorld()
        pass

    def NewRound(self):
        pass

class LocalMultiplayerPong(Pong):
    def __init__(self, WorldContainer):
        super().__init__(
            WorldContainer,
            [Entities.Ball()],
            [],
            []
        )