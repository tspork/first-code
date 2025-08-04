import math
from sprite import Sprite, V, V_ZERO
from timer import Duration

DEGREE_PER_RADIAN = 180 / math.pi
RADIAN_PER_DEGREE = math.pi / 180

class Entity():
    id = 0
    def __init__(
            self,
            pos: V,
            vel: V,
            sprite: Sprite,
            **kwargs
        ):
        self.kwargs = kwargs
        Entity.id += 1
        self.id = Entity.id
        self._pos: V = pos
        self._vel: V = vel
        self._angle: float = None
        self._angle_last: float = None
        self._speed: float = None
        self.sprite = sprite
        self.acc = V()
        self.game = None
        self.dt: Duration = 0.0
        self.max_speed: float = None
        self.friction = 0.0
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def rect(self):
        return self.sprite.rect

    def check(self):
        assert isinstance(self._pos, V)
        assert isinstance(self._vel, V)
        assert isinstance(self.acc, V)
        assert isinstance(self.dt, float)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos: V):
        self.sprite.pos = self._pos = pos

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, vel: V):
        self._vel = vel
        self._speed = self._angle = None

    @property
    def speed(self):
        if self._speed is None:
            self._speed = self._vel.norm()
        return self._speed

    @speed.setter
    def speed(self, s: float):
        self._speed = self._angle = None
        self._vel = self._vel.normal() * s
        return s

    @property
    def angle(self):
        if self._angle is None:
            if self.pos.x or self.pos.y:
                self._angle_last = math.atan2(self.vel.y, self.vel.x) * DEGREE_PER_RADIAN
            self._angle = self._angle_last
        return self._angle

    @angle.setter
    def angle(self, angle: float):
        rad = angle * RADIAN_PER_DEGREE
        spd = self.speed
        self.vel = V(math.cos(rad) * spd, math.sin(rad) * spd)
        return angle

    @property
    def direction(self):
        return self.vel.normal()

    def tick(self):
        self.tick_pos(self.dt)

    def tick_cpu(self, dt: Duration):
        self.dt = dt
        self.tick_pos(dt)

    def tick_pos(self, dt: Duration):
        # self.check()
        self.vel += self.acc * 0.99
        self.acc = V() # V_0
        if self.friction:
            self.vel -= self.vel * (self.friction * dt)
        if self.max_speed:
            self.limit_speed(self.max_speed)
        self.pos += self.vel * dt

    def limit_speed(self, max_speed):
        dir, speed = self.vel.normal_and_norm()
        if speed > max_speed:
            self.vel = dir * max_speed

    def accelerate(self, a: V):
        assert isinstance(a, V)
        self.acc += a

    def set_vel(self, v: V):
        self.accelerate(v - self.vel)

    def move_toward(self, p, force = 1.0):
        direction, distance = (p - self.pos).normal_and_norm()
        vel = direction * (self.speed * force)
        self.accelerate(vel)

    def avoid_point(self, p, r0, r1):
        # print(f"avoid_point {self} {r0} {r1}")
        v = self.pos - p
        dir, norm = v.normal_and_norm()
        if r0 <= norm and norm < r1 and self.vel.dot(dir) < 0:
            vel = self.vel.reflected(dir) * 1.2
            # print(f"avoid_point {p} {r0} {r1} {vel}")
            self.set_vel(vel)
            return True
        return False

    def repel_from_pos(self, p, min_distance):
        dp = self.pos - p
        dir, dist = dp.normal_and_norm()
        pen = min_distance - dist
        if pen > 0:
            force = min_distance / pen
            # print(f"repel_from: d={min_distance} dist={dist} pen={pen} force={force}")
            vel = dir * force * 3.0
            self.accelerate(vel)

    def repel(self, other, min_distance):
        dp = self.pos - other.pos
        dir, dist = dp.normal_and_norm()
        pen = min_distance - dist
        if pen > 0:
            force = min_distance / pen
            force *= 0.99
            vel = dir * force
            self.accelerate(vel)
            other.accelerate(- vel)

    def think(self):
        pass

    def draw(self, screen):
        self.sprite.draw(screen)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id}, pos={self.pos}, vel={self.vel}, acc={self.acc}, dt={self.dt})"

