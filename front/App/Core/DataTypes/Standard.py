class Vector:
    '''
    A 2D vector with x,y
    '''    
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def normalized(self):
        '''returns normalized vector'''
        l = self / Vector(0,0)
        return Vector(self.x / l, self.y / l)

    def normalize(self):
        '''normalizes the vector itself, returns old value'''
        old = Vector(self.x, self.y)
        l = old / Vector(0,0)
        self.x /= l
        self.y /= l
        return old

    def __eq__(self, other): # Vector == other
        t = type(other)

        if t == Vector: # If other is also a vector just compare x and y
            return self.x == other.x and self.y == other.y
        elif (t == tuple or t == list) and len(other) == 2: # if other is a tuple or list with two elems, like (x, y) then compare those two
            return self.x == other[0] and self.y == other[1]
        else: # if its none of these types then just say its not equal
            return False

    def __repr__(self): # Representation of our vector as a string
        return f"Vector({self.x}, {self.y})"

    def __str__(self): # str(Vector)
        return f"({self.x}, {self.y})"

    def __add__(self,other): # Vector + other
        try:
            t = type(other)
            if t == Vector:
                return Vector(self.x + other.x, self.y + other.y)
            elif (t == tuple or t == list) and len(other) == 2:
                return Vector(self.x + other[0], self.y + other[1])
            else:
                raise TypeError(f"Type error : vector cannot be added with type : {t}")
        except Exception:
            raise TypeError(f"Type error : vector cannot be added with : {other}")
            

    def __sub__(self, other): # Vector - other
        try:
            t = type(other)
            if t == Vector:
                return Vector(self.x - other.x, self.y - other.y)
            elif (t == tuple or t == list) and len(other) == 2:
                return Vector(self.x - other[0], self.y - other[1])
            else:
                raise TypeError(f"Type error : vector cannot be subtracted by type : {t}")
        except Exception:
            raise TypeError(f"Type error : vector cannot be subtracted by : {other}")
    
    def __mul__(self, other): # Vector * other
        t = type(other)
        if t == float or t == int:
            return Vector(other * self.x, other * self.y)
        else:
            raise TypeError(f"Cannot multiply vector and : {t}")
    
    def __truediv__(self, other): # I am using VectorA / VectorB = Distance bw VectorA and VectorB
        t = type(other)
        if t == float or t == int:
            return Vector(self.x / other, self.y / other)
        if t == Vector:
            return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        else:
            raise TypeError(f"Cannot divide vector and : {t}")

    def __gt__(self, other): # Vector > other
        t = type(other)
        if t == Vector:
            return self / Vector(0,0) > other / Vector(0,0)
        elif t == int or t == float:
            return self / Vector(0,0) > other
        else:
            raise TypeError("Cannot find dist")

    def __lt__(self, other): # Vector < other
        t = type(other)
        if t == Vector:
            return self / Vector(0,0) < other / Vector(0,0)
        elif t == int or t == float:
            return self / Vector(0,0) < other
        else:
            raise TypeError("Cannot find dist")

    def __le__(self,other): # Vector <= other
        t = type(other)
        if t == Vector:
            return self / Vector(0,0) <= other / Vector(0,0)
        elif t == int or t == float:
            return self / Vector(0,0) <= other
        else:
            raise TypeError("Cannot find dist")

    def __ge__(self, other): # Vector >= other
        t = type(other)
        if t == Vector:
            return self / Vector(0,0) >= other / Vector(0,0)
        elif t == int or t == float:
            return self / Vector(0,0) >= other
        else:
            raise TypeError("Cannot find dist")
