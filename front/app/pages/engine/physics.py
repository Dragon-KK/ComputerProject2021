class CollisionData:
    x = 0
    y = 1
    def __init__(self, collider, collisionPoint, collisionAxis = 0):
        self.collider = collider
        self.collisionPoint = collisionPoint
        self.collisionAxis = collisionAxis

class world:
    def __init__(self, balls, walls):
        self.balls = balls
        self.walls = walls
        

    def calculateNextCollidingWall(self,ball):
        potentialWalls = {}
        for i in ball.walls:
            absInfo = self.walls[i].getAbsoluteInfo()
            if self.walls[i].vertical:
                tmp = ball.direction.x * (-ball.position.x + absInfo['p1'].x)
                if tmp > 0:
                    potentialWalls[tmp] = self.walls[i]
            else:
                tmp = ball.direction.y * (-ball.position.y + absInfo['p2'].y)
                if tmp > 0:
                    potentialWalls[tmp] = self.walls[i]
        if len(potentialWalls.values()) == 0:
            # Maybe raise some error here ?
            pass
        else:
            ball.nextCollidingWall = potentialWalls[min(potentialWalls.keys())]

    def handleBall(self,ball):
        for ball in self.balls:
            ball.update()
            self.calculateNextCollidingWall(ball)
            print(ball.nextCollidingWall.p1, ball.nextCollidingWall.p2) if ball.nextCollidingWall else print("Not bounded")
        # options :
        # do collision check each frame
        # after each collision calculate the next colliding wall and when the wall is passed handle collision and repeat !!! Do this
        pass

    def work(self, dt = 0.1):
        for ball in self.balls:
            self.handleBall(ball)