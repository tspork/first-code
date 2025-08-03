from sprite import Sprite
from cpu import Program, CPU, V

class Enemy():
    def __init__(
            self,
            pos: V,
            vel: V,
            sprite: Sprite,
            program: Program,
        ):
        self.pos = pos
        self.vel = vel
        self.cpu = CPU(self, program)
        self.sprite = sprite
        self.update()

    def update(self):
        self.sprite.pos = self.pos

    def tick(self, dt: float):
        self.cpu.tick(dt)
        self.update()

    def cpu_tick(self, dt: float):
        self.pos += self.vel * dt

    def acc(self, a):
        # print(f"a={a} dp={self.vel}")
        self.vel += a

    def draw(self, screen):
        self.sprite.draw(screen)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Enemy({self.p}, {self.dp})"

