from vector2d import V
import pygame

class Rect:
    def __init__(self, pos: V, size: V):
        self.pos = pos
        self.size = size

    def center(self):
        return self.pos + self.size * 0.5

    def move(self, d: V):
        self.pos += d
        return self

    def as_tuple(self):
        return (self.pos.x, self.pos.y, self.size.x, self.size.y)

    def as_Rect(self):
        return pygame.Rect(self.as_tuple())

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"Rect({self.pos}, {self.size})"

BLACK = (0, 0, 0)
WHITE = (256, 256, 128)

class Sprite:
    def __init__(self, size: V, color: tuple = WHITE):
        self.pos = V()
        self.size = size
        self.color = color

    def rect(self):
        half = self.size * 0.5
        return Rect(self.pos - half, self.size)

    def draw(self, screen):
        rect = self.rect()
        pygame.draw.rect(
            screen,
            self.color,
            rect.as_tuple(),
        )
        return self
