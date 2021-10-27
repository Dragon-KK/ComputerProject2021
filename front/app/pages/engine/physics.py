class CollisionData:
    x = 0
    y = 1
    def __init__(self, collider, collisionPoint, collisionAxis = 0):
        self.collider = collider
        self.collisionPoint = collisionPoint
        self.collisionAxis = collisionAxis