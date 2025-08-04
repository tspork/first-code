from vector2d import V
import pygame

V_ZERO = V(0.0, 0.0)
V_POS_1 = V(1.0, 1.0)
V_NEG_1 = V(-1.0, -1.0)

BLACK = (0, 0, 0)
WHITE = (256, 256, 128)

class Rect:
    def __init__(self, pos: V, size: V):
        self.pos = pos
        self.size = size

    @property
    def width(self):
        return self.size.x
    @property
    def height(self):
        return self.size.y
    @property
    def left(self):
        return self.pos.x
    @property
    def right(self):
        return self.pos.x + self.size.x
    @property
    def top(self):
        return self.pos.y
    @property
    def bottom(self):
        return self.pos.y + self.size.y

    @property
    def center(self):
        return self.pos + self.size * 0.5

    def centered(self):
        half = self.size * 0.5
        return Rect(self.pos - half, self.size)

    def move(self, d: V):
        self.pos += d
        return self

    def contains(self, v):
        return (
            self.left <= v.x and v.x < self.right and
            self.top  <= v.y and v.y < self.bottom
        )

    def as_tuple(self):
        return (self.pos.x, self.pos.y, self.size.x, self.size.y)

    def as_pygame_Rect(self):
        return pygame.Rect(self.as_tuple())

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"Rect({self.pos}, {self.size})"

class Sprite:
    def __init__(self, size: V, color: tuple = WHITE):
        self.pos = V()
        self.size = size
        self.color = color

    @property
    def rect(self):
        return Rect(self.pos, self.size).centered()

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            self.rect.as_tuple(),
        )
        return self
