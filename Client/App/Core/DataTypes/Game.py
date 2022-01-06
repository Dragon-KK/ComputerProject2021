class EntityHolder(list):
    def __init__(self,container, Styles  = {}):
        super().__init__()
        self.Styles = Styles
        self.Container = container

    def AddEntity(self,entity):
        self.append(entity)
        entity.SetStyles(self.Styles.get(entity.Tag, {}))
        self.Container.Children += entity.Sprite

    def RemoveEntity(self, entity):
        if entity in self:
            self.remove(entity)
            self.Container.Children -= entity.Sprite

    def __add__(self, entity):
        self.AddEntity(entity)
        return self
    def __iadd__(self, entity):
        self.AddEntity(entity)
        return self

    def __sub__(self, entity):
        self.RemoveEntity(entity)
        return self
    def __isub__(self, entity):
        self.RemoveEntity(entity)
        return self

from dataclasses import dataclass


@dataclass
class GameSettings:
    """Game Settings"""
    Difficulty : float # Initial Speed
    DifficultySlope : float # Accelereration
    BallCount : int # Number of balls
    Duece : bool # Are dueces to be considered
    WinCondition : int # Best of how much

    @classmethod
    def FromJson(cls, data):
        return cls(
            data['Difficulty'],
            data['DifficultySlope'],
            data['BallCount'],
            data['Duece'],
            data['WinCondition']
        )
    