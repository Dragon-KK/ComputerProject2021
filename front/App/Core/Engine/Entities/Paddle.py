from ....UI.Components.Sprites import Rectangle
from ...DataTypes.Standard import Vector
from . import Entity

class VirtualWall:
    def __init__(self, P1, P2, isHorizontal = False):
        self.P1 = P1
        self.P2 = P2
        self.IsHorizontal = isHorizontal

    def Displace(self, displacement):
        self.P1 += displacement
        self.P2 += displacement

class Orientation:
    Left = 0 # The paddle defends the goal on the left
    Right = 1 # The paddle defends the goal on the right
    

class Paddle(Entity):
    OrientationTypes = Orientation
    
    def __init__(self, position, size,orientation,name = "Paddle"):
        '''
        Paddle code is kinda scuffed but its ok ig
        '''
        super().__init__(Rectangle(position, size), dynamic=True, tag="Paddle")

        self.__InitArgs = {
            'position' : position,
            'size' : size
        }
        self.PaddleName = name
        self.Size = size
        self.Orientation = orientation
        self.SetWalls()

    def SetWalls(self):
        w = self.Size.x / 2 # Just some variables to help in finding the virtual wall positions
        h = self.Size.y / 2
        if self.Orientation == Paddle.OrientationTypes.Left:           

            self.Walls = [
                VirtualWall(self.Position + (-w, h), self.Position + (w, h), isHorizontal=True), # The wall on top
                VirtualWall(self.Position + (w,-h), self.Position + (w, h)), # The wall on the right of the rectangle
                VirtualWall(self.Position + (-w, -h), self.Position + (w, -h), isHorizontal=True), # The wall on the bottom
            ]
        elif self.Orientation == Paddle.OrientationTypes.Right:
            self.Walls = [
                VirtualWall(self.Position + (-w, h), self.Position + (w, h), isHorizontal=True), # The wall on top
                VirtualWall(self.Position + (-w,-h), self.Position + (-w, h)), # The wall on the left of the rectangle
                VirtualWall(self.Position + (-w, -h), self.Position + (w, -h), isHorizontal=True), # The wall on the bottom
            ]

    def Reset(self):
        self.Position = self.__InitArgs['position']
        self.Size = self.__InitArgs['size']
        self.Sprite.Size = self.__InitArgs['size']


    def ActiveWalls(self, ball):
        """The ActiveWalls for a ceertain ball."""
        if self.Orientation == Paddle.OrientationTypes.Left:
            if ball.Velocity.Direction.x < 0:
                if ball.Velocity.Direction.y > 0:
                    return self.Walls[1:]
                elif ball.Velocity.Direction.y < 0:
                    return self.Walls[:2]
                else:
                    return self.Walls[1:2]
            else:
                return []
        elif self.Orientation == Paddle.OrientationTypes.Right:
            if ball.Velocity.Direction.x > 0:
                if ball.Velocity.Direction.y > 0:
                    return self.Walls[1:]
                elif ball.Velocity.Direction.y < 0:
                    return self.Walls[:2]
                else:
                    return self.Walls[1:2]
            else:
                return []


    # region Position
    @property
    def Position(self):
        return self.Sprite.Position
    @Position.setter
    def Position(self, NewPosition):
        for wall in self.Walls:
            wall.Displace(NewPosition - self.Position)
        self.Sprite.Position = NewPosition
    # endregion