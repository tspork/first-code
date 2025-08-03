# See: https://scipython.com/books/book2/chapter-4-the-core-python-language-ii/examples/a-2d-vector-class/

import math
from random import Random

def lerp(t, x0, x1):
    return x0 * (1.0 - t) + x1 * t

class Vector2D:
    """A two-dimensional vector with Cartesian coordinates."""

    def __init__(self, x = 0.0, y = 0.0):
        self.x, self.y = float(x), float(y)

    def __str__(self):
        """Human-readable string representation of the vector."""
        return self.__repr__()

    def __repr__(self):
        """Unambiguous string representation of the vector."""
        return repr((self.x, self.y))

    def pair(self):
        """Return a tuple."""
        return (self.x, self.y)

    def dot(self, other):
        """The scalar (dot) product of self and other. Both must be vectors."""
        other = Vector2D.coerce(other)
        return self.x * other.x + self.y * other.y
    # Alias the __matmul__ method to dot so we can use a @ b as well as a.dot(b).
    __matmul__ = dot

    def __sub__(self, other):
        """Vector subtraction."""
        other = Vector2D.coerce(other)
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """Vector addition."""
        other = Vector2D.coerce(other)
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """Multiplication of a vector by a scalar."""
        if not isinstance(scalar, Vector2D):
            return Vector2D(self.x * scalar, self.y * scalar)
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __rmul__(self, scalar):
        """Reflected multiplication so vector * scalar also works."""
        return self.__mul__(scalar)

    def __neg__(self):
        """Negation of the vector (invert through origin.)"""
        return Vector2D(- self.x, - self.y)

    def __truediv__(self, scalar):
        """True division of the vector by a scalar."""
        return Vector2D(self.x / scalar, self.y / scalar)

    def __mod__(self, other):
        """One way to implement modulus operation: for each component."""
        other = Vector2D.coerce(other)
        return Vector2D(self.x % other.x, self.y % other.y)

    def __abs__(self):
        """Absolute value (magnitude) of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_to(self, other):
        """The distance between vectors self and other."""
        return abs(self - other)

    def to_polar(self):
        """Return the vector's components in polar coordinates."""
        return self.__abs__(), math.atan2(self.y, self.x)

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normal(self):
        norm = self.norm()
        if norm == 0:
            return self
        norm = 1 / norm
        return Vector2D(self.x * norm, self.y * norm)

    def reflect(self, nn):
        '''Presume nn is normal.'''
        # nn = n.normal()
        return self - 2 * self.dot(nn) * nn

    @classmethod
    def coerce(cls, x):
        if isinstance(x, Vector2D):
            return x
        return Vector2D(x, x)

    @classmethod
    def random(cls, x0, x1, rand: Random):
        x0 = cls.coerce(x0)
        x1 = cls.coerce(x1)
        x = lerp(rand.random(), x0.x, x1.x)
        y = lerp(rand.random(), x0.y, x1.y)
        return cls(x, y)

    @classmethod
    def lerp(cls, t, x0, x1):
        x0 = cls.coerce(x0)
        x1 = cls.coerce(x1)
        return lerp(t, x0, x1)

V = Vector2D

if __name__ == '__main__':
    v1 = Vector2D(2, 5/3)
    v2 = Vector2D(3, -1.5)
    print('v1 = ', v1)
    print('repr(v2) = ', repr(v2))
    print('v1 + v2 = ', v1 + v2)
    print('v1 - v2 = ', v1 - v2)
    print('abs(v2 - v1) = ', abs(v2 - v1))
    print('-v2 = ', -v2)
    print('v1 * 3 = ', v1 * 3)
    print('7 * v2 = ', 7 * v1)
    print('v2 / 2.5 = ', v2 / 2.5)
    print('v1 % 1 = ', v1 % 1)
    print('v1.dot(v2) = v1 @ v2 = ', v1 @ v2)
    print('v1.distance_to(v2) = ',v1.distance_to(v2))
    print('v1 as polar vector, (r, theta) =', v1.to_polar())

'''
The output should be:

v1 =  2i + 1.66667j
repr(v2) =  (3, -1.5)
v1 + v2 =  5i + 0.166667j
v1 - v2 =  -1i + 3.16667j
abs(v2 - v1) =  3.3208098075285464
-v2 =  -3i + 1.5j
v1 * 3 =  6i + 5j
7 * v2 =  14i + 11.6667j
v2 / 2.5 =  1.2i + -0.6j
v1 % 1 =  0i + 0.666667j
v1.dot(v2) = v1 @ v2 =  3.5
v1.distance_to(v2) =  3.3208098075285464
v1 as polar vector, (r, theta) = (2.6034165586355518, 0.6947382761967033)
Learning Scientific Programming with Python © 2025 Christian Hill
The content on this page is licensed under CC-BY 4.0 unless otherwise stated.
'''