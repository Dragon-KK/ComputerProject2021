from .entities import Ball,Player,Wall,WinZone
from typing import List
from .playerManagers import playerManager
from .util import Daemon
from .physics import world

# This is where the pong part happens
# !!
# !!!
# !!!!
#
#
#
# The timing loop part is dogshit fix it
# 
#
# !!!!!!!
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
    def __init__(self, arena, settings : GameSettings, playerManager : playerManager,fps = 10,walls = {}, winZones = {}, balls  = []):
        self.settings = settings
        self.arena = arena
        self.playerManager = playerManager
        self.balls = balls
        self.walls = walls
        self.drawInterval = fps
        self.winZones = winZones
        self.renderSlave = Daemon(arena.getTkObj(), self.drawInterval, self.renderFrame)
        
    def renderFrame(self, dt = 1):
        
        for i in self.balls:
            i.draw()
        self.renderSlave.tk.configure(cursor='arrow') # i just need that tk obj, you could do this in many ways, i did this cause im lazy

    def cont(self):
        self.renderSlave.cont()

    def pause(self):
        self.renderSlave.pause()

    def reset(self):
        self.pause()
        for i in self.balls:
            i.reset()

    def forceQuit(self):
        self.renderSlave.pause()

