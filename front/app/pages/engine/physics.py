from ...common.tools import Vector
from . import entities
class CollisionData:
    x = 0
    y = 1
    def __init__(self, collider, collisionPoint, collisionAxis = 0):
        self.collider = collider
        self.collisionPoint = collisionPoint
        self.collisionAxis = collisionAxis

class world:
    def __init__(self, game, onRoundFinish):
        self.balls = game.balls
        self.walls = game.walls
        for i in game.winZones:
            self.walls[i] = game.winZones[i]
        self.game = game
        self.onRoundFinish = onRoundFinish


        self.players = game.getPlayers()

    def calculateNextCollidingWall(self,ball):
        potentialWalls = {}
        for i in ball.walls + ball.winZones:
            
            absInfo = self.walls[i].getAbsoluteInfo()
            if self.walls[i].vertical:
                
                tmp = ball.direction.x * (-ball.position.x + absInfo['p1'].x)
                if tmp > 0:
                    r = ball.info()['radius']
                    r *= -1 if ball.direction.x < 0 else 1
                    tmp = absInfo['p1'].x - ball.position.x - r
                    usedJuice = tmp / ball.direction.x
                    yCheck = usedJuice * ball.direction.y + ball.position.y
                    if absInfo['p1'].y < yCheck < absInfo['p2'].y:
                        potentialWalls[tmp] = self.walls[i]
            else:
                tmp = ball.direction.y * (-ball.position.y + absInfo['p2'].y)
                if tmp > 0:
                    r = ball.info()['radius']
                    r *= -1 if ball.direction.y < 0 else 1
                    tmp = absInfo['p1'].y - ball.position.y - r
                    usedJuice = tmp / ball.direction.y
                    xCheck = usedJuice * ball.direction.x + ball.position.x
                    if absInfo['p1'].x < xCheck < absInfo['p2'].x:
                        potentialWalls[tmp] = self.walls[i]
        if len(potentialWalls.values()) == 0:
            print("No go")
            pass
        else:
            ball.nextCollidingWall = potentialWalls[min(potentialWalls.keys())]
        ball.hasCollidedSinceCheck = False

    def handleBallCollision(self, currPos, juice, direction, wall):
        newPos = Vector(0,0)
        return (newPos, juice, newDirection)

    def roundHasEnded(self,res):
        
        self.game.reset()
        self.onRoundFinish(res)
        

    def handleBall(self,ball, dt):
        juice = ball.speed * dt
        while juice > 0:
            cont = True
            # TODO fix checkForCollision function
            for player in self.players:
                
                (collided, juiceUsed) = player.walls['verticalWall'].checkForCollision(ball,juice,player.totalDisplacement)
                if collided:
                    juice -= juiceUsed
                    cont = False
                    break
            if not cont:continue
            if (ball.hasCollidedSinceCheck):self.calculateNextCollidingWall(ball)
            if type(ball.nextCollidingWall) is entities.Wall:
                juice -= ball.nextCollidingWall.checkForCollisionAndMove(ball, juice)
            else:
                (roundFinish, result) = ball.nextCollidingWall.checkForWinOrMove(ball, juice)
                if roundFinish:
                    self.roundHasEnded(result)
                else:
                    juice = 0

            

        ball.speed += ball.acceleration * dt
        pass

    def work(self, dt = 0.1):
        for ball in self.balls:
            self.handleBall(ball, dt)