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

    def getAbsoluteInfo(self):
        return self.arena.items[self.itemID].absoluteInfo

    def checkForCollision(self, ball):
        if ball.lastCollidedWall == self:return False,None
        tmp = ball.info()
        currPos = tmp['position']
        radius = tmp['radius']
        prevPos = ball.prevposition
        
        tmp2 = self.arena.items[self.itemID].absoluteInfo
        p1 = tmp2['p1']
        p2 = tmp2['p2']
        
        # This part is trash
        if self.vertical:
            correctedY = ((p1.x - prevPos.x) * (currPos.y - prevPos.y)/(currPos.x - prevPos.x)) + prevPos.y if currPos.x  != prevPos.x else currPos.x
            if (p1.y <= correctedY <= p2.y):
                if (currPos.x + radius > p1.x and prevPos.x + radius < p1.x) or (currPos.x - radius < p1.x and prevPos.x - radius > p1.x):
                    
                    return True,CollisionData(self, Vector(p1.x, correctedY), collisionAxis = CollisionData.y)          
        else:
            correctedX = ((p1.y-prevPos.y) * (currPos.x - prevPos.x)/(currPos.y - prevPos.y)) + prevPos.x if currPos.y != prevPos.y else currPos.y
            if (p1.x <= correctedX <= p2.x):
                if (currPos.y + radius > p1.y and prevPos.y + radius < p1.y) or (currPos.y - radius < p1.y and prevPos.y - radius > p1.y):
                    
                    return True,CollisionData(self,Vector(correctedX, p1.y), collisionAxis = CollisionData.x)
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
        self.nextCollidingWall = None
        self.arena = arena
        self.speed = initialSpeed
        self.position = Vector(0, 0)
        self.prevposition = Vector(0, 0) # I should probably store this in absoluteInfo but... meh atleast i know where all my bugs will probably come from now
        self.acceleration = acceleration
        self.direction = Vector(1,0).normalized()
        self.walls = walls
        self.winZones = winZones

    def update(self):
        self.position = self.arena.items[self.itemID].absoluteInfo['position']

    def info(self):
        return self.arena.items[self.itemID].absoluteInfo

    def displace(self, displacement):
        pass

    def work(self, dt = 0.1):

        # Move this to physics, ball should be like player manager

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
