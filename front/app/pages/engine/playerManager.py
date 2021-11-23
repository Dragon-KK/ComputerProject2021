from ...utils.keyInput import inputWatcher
from ...common.tools import Vector
LEFTPLAYER = -1
RIGHTPLAYER = 1


# ! IMP make a pause function for playermanager also
class playerManager:
    def __init__(self, players):
        self.players = players

    def getPlayers(self):
        return self.players

    def render(self):
        for i in self.players:
            i.draw()

    def end(self):
        pass

class localMultiplayer(playerManager):
    def __init__(self, player1, player2, arena):
        super().__init__([player1,player2])
        self.p1 = player1
        self.p2 = player2
        self.input = inputWatcher(arena.getTkObj())
        self.input.bind("w", self.keyDown)
        self.input.bind("s", self.keyDown)
        self.input.bind("<Up>", self.keyDown, spclCode="Up")
        self.input.bind("<Down>", self.keyDown, spclCode="Down")

        

    def keyDown(self, k):
        if k == "w":self.p1.displace(Vector(0,-20))
        elif k == "s":self.p1.displace(Vector(0, 20))
        elif k == "Up":self.p2.displace(Vector(0,-20))
        elif k == "Down":self.p2.displace(Vector(0, 20))

    def end(self):
        print("Closing input watcher")
        self.input.pause()



