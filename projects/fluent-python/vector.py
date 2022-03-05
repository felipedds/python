# Special methods 
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def __add__(self, otherVector):
        x = self.x + otherVector.x
        y = self.y + otherVector.y
        return Vector(x, y)

    def __mul__(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        return Vector(x, y)    
    
v1 = Vector(2, 4)
v2 = Vector(3, 7)

print(v1.__repr__)
print(v1, v2)
print(v1 + v2)
print(v1 * 3)
