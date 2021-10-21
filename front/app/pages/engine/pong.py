from .entities import Ball,Player

class Game:
    def __init__(self, drawer, settings, playerManager):
        self.settings = settings
        self.drawer = drawer
        self.playerManager = playerManager

    def start(self):
        pass

    def pause(self):
        pass

    def end(self):
        pass

class GameSettings:
    def __init__(self, difficulty = 10,duece = False, winCondition = 5, difficultySlope = 0.5):
        self.speed = difficulty
        self.duece = duece
        self.winCondition = winCondition
        self.difficultySlope = difficultySlope

    def __repr__(self):
        return f"<GameSettings speed={self.speed} duece={self.duece} difficultySlope={self.difficultySlope} winCondition={self.winCondition}>" 