# See: https://scipython.com/books/book2/chapter-4-the-core-python-language-ii/examples/a-2d-vector-class/

import math
from math import pi
from random import Random

M_PI_PER_DEG = pi / 18.0

def lerp(t, x0, x1):
    return x0 * (1 - t) + x1 * t

class Vector2D:
    """A two-dimensional vector with Cartesian coordinates."""

    def __init__(self, x = 0.0, y = None):
        self.x, self.y = float(x), float(y if y is not None else x)

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

    def __bool__(self):
        return not self.x and not self.y

    def __sub__(self, other):
        """Vector subtraction."""
        other = Vector2D.coerce(other)
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """Vector addition."""
        other = Vector2D.coerce(other)
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        """Multiplication of a vector by a scalar."""
        other = Vector2D.coerce(other)
        return Vector2D(self.x * other.x, self.y * other.y)

    def __rmul__(self, scalar):
        """Reflected multiplication so vector * scalar also works."""
        return self.__mul__(scalar)

    def __neg__(self):
        """Negation of the vector (invert through origin.)"""
        return Vector2D(- self.x, - self.y)

    def __truediv__(self, other):
        """True division of the vector by a scalar."""
        other = Vector2D.coerce(other)
        return Vector2D(self.x / other.x, self.y / other.y)

    def __mod__(self, other):
        """One way to implement modulus operation: for each component."""
        other = Vector2D.coerce(other)
        return Vector2D(self.x % other.x, self.y % other.y)

    def __abs__(self):
        """"""
        return Vector2D(abs(self.x), abs(self.y))

    def distance_to(self, other):
        """The distance between vectors self and other."""
        return abs(self - other)

    def to_polar(self):
        """Return the vector's components in polar coordinates."""
        return self.norm(), math.atan2(self.y, self.x)

    def norm(self):
        'The norm (length).'
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normal_and_norm(self):
        norm = self.norm()
        if norm == 0:
            return self, norm
        return self * (1.0 / norm), norm

    def normal(self):
        'The normal vector.'
        return self.normal_and_norm()[0]

    def reflected(self, nn):
        '''Presume nn is normal.'''
        # nn = n.normal()
        return self - 2 * self.dot(nn) * nn

    def rotated(self, deg):
        theta = deg * M_PI_PER_DEG
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        return Vector2D(
            cos_theta * self.x - sin_theta * self.y,
            sin_theta * self.x + cos_theta * self.y)

    @classmethod
    def coerce(cls, x):
        if isinstance(x, cls):
            return x
        if isinstance(x, (tuple, list)):
            return cls(*x)
        # print(f"coerce({x!r})"); jkasldkfjs
        return cls(x, x)

    @classmethod
    def random(cls, x0, x1, rand: Random):
        x0 = cls.coerce(x0)
        x1 = cls.coerce(x1)
        x = lerp(rand.random(), x0.x, x1.x)
        y = lerp(rand.random(), x0.y, x1.y)
        return cls(x, y)

    @classmethod
    def random_in_circle(cls, rand: Random):
        while True:
            p = cls.random(V__1, V_1, rand)
            if p.norm() < 1.0:
                return p

    @classmethod
    def random_on_circle(cls, rand: Random):
        return cls.random_in_circle(rand).normal()

    @classmethod
    def lerp(cls, t, x0, x1):
        x0 = cls.coerce(x0)
        x1 = cls.coerce(x1)
        return lerp(t, x0, x1)

V = Vector2D
V_0 = V_ZERO = Vector2D(0.0, 0.0)
V_1 = V_POS_1 = Vector2D(1.0, 1.0)
V__1 = V_NEG_1 = Vector2D(-1.0, -1.0)

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