from .Util import Time
from ..DataTypes.UI import Interval
from ..DataTypes.Standard import Vector
from ..DataTypes.Physics import Collision
from ..Diagnostics.Debugging import Console

def sign(n):
    '''Returns the sign of the number n'''
    return 1 if n > 0 else -1 if n < 0 else 0

class Physics:

    def HandleBall(self, ball, dt):
        '''
        Called every physics loop
        Handles interactions of a single ball
        '''
        fuel = ball.Velocity.Magnitude * dt # The distance to be covered by the ball in this dt time

        while fuel > 0: # While we still have fuel,
            
            PaddleCollisionData = self.CheckPaddleCollision(ball, fuel) # First we check if the ball collides with any of the paddles
            if PaddleCollisionData: # If it did,
                FuelUsed = self.OnBallCollision(ball, PaddleCollisionData)
                fuel -= FuelUsed
                continue

            if not ball.NextCollidingStaticBody: 
                if not self.CalculateNextCollidingStaticBody(ball): return True

            staticBodyCollisionData = self.CheckStaticBodyCollision(ball, fuel) # Check if it collided with any of the walls or goals
            if staticBodyCollisionData: # If it did,
                if staticBodyCollisionData.CollidingBody.Tag == "Goal": # If what it collided with was a goal,
                    return staticBodyCollisionData # Return the collisionData

                else: # If what it collided with was a wall
                    FuelUsed = self.OnBallCollision(ball, staticBodyCollisionData)
                    ball.Position = staticBodyCollisionData.PointOfCollision
                    fuel -= FuelUsed
                    continue

            ball.Position += ball.Velocity.Direction * fuel # Move our ball using all the fuel
            fuel = 0 # All the fuel has been used

        ball.Velocity.Magnitude += ball.Acceleration * dt # Increase velocity

        return None # The ball did not touch the goal

    def CheckPaddleCollision(self, ball, fuel):
        '''
        Looks for collision with any of the paddles
        Return None if no collision else return Collision object
        '''
        nextCollidingOptions = {}
        for paddle in self.Paddles:

            walls = paddle.ActiveWalls(ball)
            for entity in walls: # I go through each of the walls it could theoretically collide with
                if entity.IsHorizontal: # If the wall is horizontal,
                    poc = ball.Position + Vector(0, sign(ball.Velocity.Direction.y) * ball.Radius)
                    FuelNeeded = (entity.P1.y - poc.y) / ball.Velocity.Direction.y # distance.y * speed / velocity.y
                    if FuelNeeded > fuel or FuelNeeded < 0:continue             
                    xCoordOfCollision = poc.x + (FuelNeeded * ball.Velocity.Direction.x)
                    if entity.P1.x < xCoordOfCollision < entity.P2.x: # The x coordinate of collision falls bw the ends of the wall/goal
                        nextCollidingOptions[FuelNeeded] = (entity, Vector(xCoordOfCollision,ball.Position.y + (ball.Velocity.Direction.y * FuelNeeded)))
                else: # If the wall is vertical,
                    # The actual point of contact of the collision is going to be on the circumpherence of the ball
                    # So we use the point on circumpherence to calculate collision but point of contact is still taken as position of centre of the ball when it collides

                    poc = ball.Position + Vector(sign(ball.Velocity.Direction.x) * ball.Radius, 0)
                    # The point on circumpherence that will collide (point of contact, poc)

                    FuelNeeded = (entity.P1.x - poc.x) / ball.Velocity.Direction.x # distance.x / velocity.x
                    if FuelNeeded > fuel or FuelNeeded < 0:continue                
                    yCoordOfCollision = poc.y + (FuelNeeded * ball.Velocity.Direction.y)
                    if entity.P1.y < yCoordOfCollision < entity.P2.y: # The y coordinate of collision falls bw the ends of the wall/goal
                        nextCollidingOptions[FuelNeeded] = (entity, Vector(ball.Position.x + (ball.Velocity.Direction.x * FuelNeeded), yCoordOfCollision))
        if not nextCollidingOptions:
            return None
        
        minIndex = min(nextCollidingOptions.keys())
        return Collision(nextCollidingOptions[minIndex][0], nextCollidingOptions[minIndex][1])

    def CheckStaticBodyCollision(self, ball, fuel):
        '''
        Looks for collision with ball.NextCollidingWall
        Return None if no collision else return Collision object
        '''
        # FIXME We can reduce this if statement by a shitload
        MaxPosition = ball.Position + (ball.Velocity.Direction * fuel)
        if (ball.Position.x < ball.PredictedCollisionPoint.x < MaxPosition.x) or \
           (ball.Position.y < ball.PredictedCollisionPoint.y < MaxPosition.y) or \
           (ball.Position.x > ball.PredictedCollisionPoint.x > MaxPosition.x) or \
           (ball.Position.y > ball.PredictedCollisionPoint.y > MaxPosition.y):
           return Collision(ball.NextCollidingStaticBody, ball.PredictedCollisionPoint)

        return None

    def CalculateNextCollidingStaticBody(self, ball):
        '''
        Calculates the point of collision and next colliding wall or goal for a ball
        '''      
        nextCollidingOptions = {} # A dictionary with the key being distance and value being (nextcollidingbody, point of collision)

        for entity in self.Walls + self.Goals: # Loop through all the static bodies
            if entity.IsHorizontal: # If its a horizontal wall/goal                
                # The actual point of contact of the collision is going to be on the circumpherence of the ball
                # So we use the point on circumpherence to calculate collision but point of contact is still taken as position of centre of the ball when it collides
                poc = ball.Position + Vector(0, sign(ball.Velocity.Direction.y) * ball.Radius)
                # The point on circumpherence that will collide (point of contact, poc)
                if sign(entity.P1.y - poc.y) * sign(ball.Velocity.Direction.y) <= 0:
                    # The ball will 100% never collide with this entity
                    continue
                FuelNeeded = (entity.P1.y - poc.y) / ball.Velocity.Direction.y # distance.y / velocity.y             
                xCoordOfCollision = poc.x + (FuelNeeded * ball.Velocity.Direction.x)
                if entity.P1.x < xCoordOfCollision < entity.P2.x: # The x coordinate of collision falls bw the ends of the wall/goal
                    nextCollidingOptions[FuelNeeded] = (entity, Vector(xCoordOfCollision,ball.Position.y + (ball.Velocity.Direction.y * FuelNeeded)))

            else: # If its a vertical wall/goal                
                # The actual point of contact of the collision is going to be on the circumpherence of the ball
                # So we use the point on circumpherence to calculate collision but point of contact is still taken as position of centre of the ball when it collides

                poc = ball.Position + Vector(sign(ball.Velocity.Direction.x) * ball.Radius, 0)
                # The point on circumpherence that will collide (point of contact, poc)
                
                if sign(entity.P1.x - poc.x) * sign(ball.Velocity.Direction.x) <= 0:
                    # The ball will 100% never collide with this entity
                    continue

                FuelNeeded = (entity.P1.x - poc.x) / ball.Velocity.Direction.x # distance.x / velocity.x                
                yCoordOfCollision = poc.y + (FuelNeeded * ball.Velocity.Direction.y)
                if entity.P1.y < yCoordOfCollision < entity.P2.y: # The y coordinate of collision falls bw the ends of the wall/goal

                    nextCollidingOptions[FuelNeeded] = (entity, Vector(ball.Position.x + (ball.Velocity.Direction.x * FuelNeeded), yCoordOfCollision))

        if not nextCollidingOptions: # If somehow the ball can phase out of the walls just return False
            Console.error("No next colliding bodies !!!", errorLevel=10)   
            return False

        # :)
        minIndex = min(nextCollidingOptions.keys())
        ball.NextCollidingStaticBody = nextCollidingOptions[minIndex][0] # The entity
        ball.PredictedCollisionPoint = nextCollidingOptions[minIndex][1] # The poc
        return True

    def OnBallCollision(self, ball, collisionData):
        '''Called when the ball collides'''
        if collisionData.CollidingBody.IsHorizontal:
            ball.Velocity.Direction.y *= -1
        else:
            ball.Velocity.Direction.x *= -1
        ball.NextCollidingStaticBody = None
        return ball.Position / collisionData.PointOfCollision

    def OnGoal(self,ball,collisionData):
        '''Called when a ball reaches the goal'''
        self.OnGoalDone(collisionData.CollidingBody)

    def PhysicsLoop(self):
        '''
        The callback of self.__PhysicsInterval
        '''
        dt = self.Time.DeltaTime
        if dt == 0: # Sometimes dt is 0 (like when the game is just unpaused etc.)
            return

        for ball in self.Balls:
            GoalCollisionData = self.HandleBall(ball, dt)
            if GoalCollisionData:
                ball.Position = ball.PredictedCollisionPoint
                self.OnGoal(ball, GoalCollisionData)
                break

    def __init__(self, canvas, balls, walls, goals,paddles, physicsDelay, onGoal):
        self.__PhysicsInterval = Interval(physicsDelay, self.PhysicsLoop)

        self.Canvas = canvas

        self.Balls = balls
        self.Walls = walls
        self.Goals = goals
        self.Paddles = paddles

        self.OnGoalDone = onGoal

        self.Time = Time()

    def Continue(self):
        self.Canvas.Window.Intervals += self.__PhysicsInterval

    def Pause(self):
        self.Canvas.Window.Intervals -= self.__PhysicsInterval
        self.Time.DeltaTime = 0