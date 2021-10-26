from .entities import Ball,Player,Wall,WinZone
from typing import List
from .playerManagers import playerManager
from .util import Daemon

class GameSettings:
    def __init__(self, difficulty = 10,duece = False, winCondition = 5, difficultySlope = 0.5):
        self.speed = difficulty
        self.duece = duece
        self.winCondition = winCondition
        self.difficultySlope = difficultySlope

    def __repr__(self):
        return f"<GameSettings speed={self.speed} duece={self.duece} difficultySlope={self.difficultySlope} winCondition={self.winCondition}>" 

class Game:
    # setting msPerFrame to 1 gives nice graphics but takes 12% ram.. : D
    # I think the main issue is that tkinter really isnt built for this kind of stuff
    # We shouldve just used pygame lol
    def __init__(self, arena, settings : GameSettings, playerManager : playerManager,msPerFrame = 5,walls = {}, winZones = {}, balls  = []):
        self.settings = settings
        self.arena = arena
        self.playerManager = playerManager
        self.balls = balls
        self.walls = walls
        self.interval = msPerFrame
        self.winZones = winZones

        for ball in self.balls:
            ball.setWallsAndWinZones(self.walls,self.winZones)

        self.daemon = Daemon(arena.getTkObj(), self.interval, self.work)

    def work(self, dt = 0.1):
        
        for ball in self.balls:
            ball.work(dt = dt)

        # I had some issue where the canvas would clip an item when canvas.move moved stuff either too fast or too much
        # this .configure(cursor='arror') seems to magically fix it so i shall not question it
        self.daemon.tk.configure(cursor='arrow') # i just need that tk obj, you could do this in many ways, i did this cause im lazy

    def start(self):
        pass

    def pause(self):
        pass

    def end(self):
        pass

    def forceQuit(self):
        self.daemon.pause()

