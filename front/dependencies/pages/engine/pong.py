from .entities import Ball,Player

class Game:
    def __init__(self, drawer, settings, playerManager):
        pass

    def start(self):
        pass

    def pause(self):
        pass

class GameSettings:
    def __init__(self, difficulty = 10,duece = False, winCondition = 5, difficultySlope = 0.5):
        self.difficulty = difficulty
        self.duece = duece
        self.winCondition = 5
        self.difficultySlope = difficultySlope