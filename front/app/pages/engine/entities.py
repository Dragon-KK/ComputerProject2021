from . import drawing as shapes
from ...common.tools import Vector
from typing import List
from .physics import CollisionData
import math
from random import randint
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

    def checkForCollision(self, ball, juice,absoluteDisplacement):
        # Need to restrucutre
        # this function is exclusive to player and shoouldnt be on wall but meh it works ig
        if self.vertical:
            r = ball.info()['radius']
            grace = r
            r *= -1 if ball.direction.x < 0 else 1
            
            absoluteInfo = {'p1':self.arena.items[self.itemID].absoluteInfo['p1'] + absoluteDisplacement,'p2':self.arena.items[self.itemID].absoluteInfo['p2'] + absoluteDisplacement}
            if (ball.position.x + r - absoluteInfo['p1'].x) * (ball.position.x + r + (ball.direction.x * juice) - absoluteInfo['p1'].x) < 0:
                tmp = absoluteInfo['p1'].x - ball.position.x - r
                usedJuice = tmp / ball.direction.x
                
                displacement = Vector(tmp,usedJuice * ball.direction.y)
                if not((absoluteInfo['p1'].y < (displacement + ball.position).y + grace)and( (displacement + ball.position).y - grace< absoluteInfo['p2'].y)):return (False,0)
                ball.displace(displacement)
                ball.direction.x *= -1
                ball.hasCollidedSinceCheck = True
                return (True,usedJuice)
        else:
            r = ball.info()['radius']
            r *= -1 if ball.direction.y < 0 else 1
            absoluteInfo = {'p1':self.arena.items[self.itemID].absoluteInfo['p1'] + absoluteDisplacement,'p2':self.arena.items[self.itemID].absoluteInfo['p2'] + absoluteDisplacement}

            if (ball.position.y + r - absoluteInfo['p1'].y) * (ball.position.y + r + juice * ball.direction.y - absoluteInfo['p1'].y) < 0:
                tmp = absoluteInfo['p1'].y - ball.position.y - r
                usedJuice = tmp / ball.direction.y
                displacement = Vector(usedJuice * ball.direction.x,tmp)
                if not(absoluteInfo['p1'].x < (displacement + ball.position).x < absoluteInfo['p2'].x):return (False,0)

                ball.displace(displacement)
                ball.direction.y *= -1
                ball.hasCollidedSinceCheck = True
                return (True, usedJuice)
        
        return (False,0) 

    def checkForCollisionAndMove(self, ball, juice):
        if self.vertical:

            r = ball.info()['radius']
            r *= -1 if ball.direction.x < 0 else 1
            if (ball.position.x + r - self.arena.items[self.itemID].absoluteInfo['p1'].x) * (ball.position.x + r + (ball.direction.x * juice) - self.arena.items[self.itemID].absoluteInfo['p1'].x) < 0:
                tmp = self.arena.items[self.itemID].absoluteInfo['p1'].x - ball.position.x - r
                usedJuice = tmp / ball.direction.x
                displacement = Vector(tmp,usedJuice * ball.direction.y)
                ball.displace(displacement)
                ball.direction.x *= -1
                ball.hasCollidedSinceCheck = True
                return usedJuice
        else:
            r = ball.info()['radius']
            r *= -1 if ball.direction.y < 0 else 1
            if (ball.position.y + r - self.arena.items[self.itemID].absoluteInfo['p1'].y) * (ball.position.y + r + juice * ball.direction.y - self.arena.items[self.itemID].absoluteInfo['p1'].y) < 0:
                tmp = self.arena.items[self.itemID].absoluteInfo['p1'].y - ball.position.y - r
                usedJuice = tmp / ball.direction.y
                displacement = Vector(usedJuice * ball.direction.x,tmp)
                ball.displace(displacement)
                ball.direction.y *= -1
                ball.hasCollidedSinceCheck = True
                return usedJuice
        ball.displace(ball.direction * juice)
        return juice

    
        
class WinZone(Wall):
    def __init__(self, result,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.result = result

    def checkForWinOrMove(self, ball, juice):
        if self.vertical:

            r = ball.info()['radius']
            r *= 1 if ball.direction.x < 0 else -1
            if (ball.position.x + r - self.arena.items[self.itemID].absoluteInfo['p1'].x) * (ball.position.x + r + (ball.direction.x * juice) - self.arena.items[self.itemID].absoluteInfo['p1'].x) < 0:
                return True,self.result
        else:
            r = ball.info()['radius']
            r *= 1 if ball.direction.y < 0 else -1
            if (ball.position.y + r - self.arena.items[self.itemID].absoluteInfo['p1'].y) * (ball.position.y + r + juice * ball.direction.y - self.arena.items[self.itemID].absoluteInfo['p1'].y) < 0:
                return True,self.result
        ball.displace(ball.direction * juice)
        return False,None
def plusMinus(n):
    return (1 if randint(0,1) == 1 else -1) * n

class Ball:
    
    def getRandomishDirection(self):
        #return Vector(-0.9805806756909202, -0.19611613513818404)
        return Vector(plusMinus(randint(5,10)), plusMinus(randint(0, 0))).normalized()

    def __init__(self,arena,walls = [], winZones = [],initialSpeed = 5, acceleration = 1, radius = '10:px', color = 'white'):
        self.itemID = arena.registerItem(
            shapes.circle(
                Vector('50:w%','50:h%'), radius,
                color = color,
                init=self.initialize
            )
        )
        
        # half of these variables are probably redundant but ig thats what i get for not writing comments ;_;
        self.hasCollidedSinceCheck = True
        self.nextCollidingWall = None
        self.arena = arena
        self.speed = initialSpeed
        self.initialSpeed = initialSpeed
        self.initialAcceleration = acceleration
        self.position = Vector(0, 0)
        self.acceleration = acceleration
        self.direction = self.getRandomishDirection()
        self.walls = walls
        self.winZones = winZones
        self.totalDisplacement = Vector(0,0)

    def initialize(self):
        self.position = self.arena.items[self.itemID].absoluteInfo['position']

    def info(self):
        return self.arena.items[self.itemID].absoluteInfo

    def draw(self):
        self.arena.moveItem(self.itemID, self.totalDisplacement)        
        self.totalDisplacement = Vector(0, 0)

    def displace(self, displacement):
        self.position += displacement
        self.totalDisplacement += displacement

    def reset(self):
        
        self.initialize()
        # half of these variables are probably redundant but ig thats what i get for not writing comments ;_;
        self.hasCollidedSinceCheck = True
        self.nextCollidingWall = None
        self.speed = self.initialSpeed
        self.acceleration = self.initialAcceleration
        self.direction = self.getRandomishDirection()
        self.totalDisplacement = Vector(0,0)
        


class Player:
    def setBoundsYmin(self,v):
        self.absoluteBounds.x = v
    def setBoundsYmax(self,v):
        self.absoluteBounds.y = v
    def __init__(self,arena, walls, playerType, maxDisplacement):
        self.arena = arena
        self.walls = walls
        self.playerType = playerType
        self.absoluteBounds = Vector(0, 0)
        self.position = Vector(0, 0)
        self.arena.query('absolute_wrt_self', maxDisplacement.x, self.setBoundsYmin)
        self.arena.query('absolute_wrt_self', maxDisplacement.y, self.setBoundsYmax)
        self.totalDisplacement = Vector(0,0)
        self.frameDisplacement = Vector(0, 0)
        # Player will basically just have 3 walls and each wall will be moved in displace
        
    def debug(self):
        print(self.absoluteBounds)

    def displace(self, amount):
        self.frameDisplacement += amount
        if (self.frameDisplacement + self.totalDisplacement).y > self.absoluteBounds.y:
            tmp  = Vector(0, self.absoluteBounds.y)
            self.frameDisplacement = tmp - self.totalDisplacement
            self.totalDisplacement = tmp
        elif (self.frameDisplacement + self.totalDisplacement).y < self.absoluteBounds.x:
            tmp  = Vector(0, self.absoluteBounds.x)
            self.frameDisplacement = tmp - self.totalDisplacement
            self.totalDisplacement = tmp
        else:
            self.totalDisplacement += amount


    def draw(self):
        for i in self.walls.values():self.arena.moveItem(i.itemID, self.frameDisplacement)
        self.frameDisplacement = Vector(0, 0)

    def reset(self):
        self.frameDisplacement = Vector(0, 0)
        self.totalDisplacement = Vector(0, 0)
        
        