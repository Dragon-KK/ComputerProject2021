from . import drawing as shapes
from ...common.tools import Vector
from typing import List
from .physics import CollisionData
import math
# This is also where the pong happens

# Collision code is dogshit


class Wall:
    def __init__(self, arena, vertical = True,p1 = Vector('0:px', '0:px'), p2 = Vector('0:px', '0:px'), color = None, size = 2):
        self.itemID = arena.registerItem(
            shapes.line(
                p1,
                p2,
                size = size,
                color = color
            )
        )
        self.p1 = p1
        self.p2 = p2
        self.vertical = vertical
        self.arena = arena

    def checkForCollision(self, ball):
        if ball.lastCollidedWall == self:return False,None
        tmp = ball.info()
        currPos = tmp['position']
        radius = tmp['radius']
        prevPos = ball.prevposition
        
        tmp2 = self.arena.items[self.itemID].absoluteInfo
        p1 = tmp2['p1']
        p2 = tmp2['p2']
        
        if self.vertical:
            if (p1.y < currPos.y < p2.y):
                if (currPos.x + radius > p1.x and prevPos.x + radius < p1.x) or (currPos.x - radius < p1.x and prevPos.x - radius > p1.x):
                    
                    return True,CollisionData(self, Vector(p1.x, ((p1.x - prevPos.x) * (currPos.y - prevPos.y)/(currPos.x - prevPos.x)) + prevPos.y), collisionAxis = CollisionData.y)          
        else:
            if (p1.x < currPos.x < p2.x):
                if (currPos.y + radius > p1.y and prevPos.y + radius < p1.y) or (currPos.y - radius < p1.y and prevPos.y - radius > p1.y):
                    
                    return True,CollisionData(self,Vector(((p1.y-prevPos.y) * (currPos.x - prevPos.x)/(currPos.y - prevPos.y)) + prevPos.x, p1.y), collisionAxis = CollisionData.x)
        return False,None
        
class WinZone(Wall):
    def __init__(self):
        pass


class Ball:
    def __init__(self,arena,walls = [], winZones = [],initialSpeed = 5, acceleration = 1, radius = '10:px', color = 'white'):
        self.itemID = arena.registerItem(
            shapes.circle(
                Vector('50:w%','50:h%'), radius,
                color = color
            )
        )
        
        # half of these variables are probably redundant but ig thats what i get for not writing comments ;_;
        self.lastCollidedWall = None
        self.arena = arena
        self.speed = initialSpeed
        self.position = Vector(0, 0)
        self.prevposition = Vector(0, 0) # I should probably store this in absoluteInfo but... meh atleast i know where all my bugs will probably come from now
        self.acceleration = acceleration
        self.direction = Vector(9,3).normalized()
        self._walls = walls
        self._winZones = winZones
        self.walls : List[Wall] = []
        self.winZones : List[WinZone] = []

    def setWallsAndWinZones(self,walls,winZones):
        for i in self._walls:
            self.walls.append(walls[i])
        for i in self._winZones:
            self.winZones.appedn(winZones[i])

    def info(self):
        return self.arena.items[self.itemID].absoluteInfo

    def work(self, dt = 0.1):

        s = self.direction * self.speed * dt
        self.arena.items[self.itemID].absoluteInfo['position'] += s
        self.prevposition = self.arena.items[self.itemID].absoluteInfo['position'] - s
        self.arena.moveItem(self.itemID, s)
        self.speed += self.acceleration * dt
        while True:
            for wall in self.walls:
                isColliding,collisionData = wall.checkForCollision(self)
                if isColliding:
                    self.handleCollision(collisionData)
                    break
            else:
                break

    def handleCollision(self, collisionData):
        self.lastCollidedWall = collisionData.collider
        self.prevposition = collisionData.collisionPoint
        currpos = self.arena.items[self.itemID].absoluteInfo['position']
        newpos = 0
        if collisionData.collisionAxis == CollisionData.x:
            newpos = Vector(currpos.x, collisionData.collisionPoint.y - (self.arena.items[self.itemID].absoluteInfo['radius']*math.copysign(2,self.direction.y) + currpos.y - collisionData.collisionPoint.y))
            self.direction.y *= -1
        else:
            newpos = Vector(collisionData.collisionPoint.x - (self.arena.items[self.itemID].absoluteInfo['radius']*math.copysign(2,self.direction.x) + currpos.x - collisionData.collisionPoint.x), currpos.y)
            self.direction.x *= -1

        s = newpos - currpos
        self.arena.items[self.itemID].absoluteInfo['position'] = newpos
        self.arena.moveItem(self.itemID, s)


class Player:
    def __init__(self):
        pass
