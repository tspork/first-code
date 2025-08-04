from sprite import Sprite, V, V_ZERO
from timer import Duration

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
        self.pos: V = pos
        self.vel: V = vel
        self.sprite = sprite
        self.acc = V()
        self.game = None
        self.dt: Duration = 0.0
        self.max_speed: float = None
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        self.pos_changed()

    @property
    def rect(self):
        return self.sprite.rect

    def check(self):
        assert isinstance(self.dt, float)
        assert isinstance(self.pos, V)
        assert isinstance(self.vel, V)
        assert isinstance(self.acc, V)
        return
        if self.vel.x or self.vel.y:
            if self.vel.x == self.vel.y:
                print(f"check: {self}")
                breakpoint()

    def pos_changed(self):
        self.sprite.pos = self.pos
        self.check()
        # print(self)
        return self

    @property
    def speed(self):
        return self.vel.norm()

    @speed.setter
    def set_speed(self, s: float):
        self.vel = self.vel * self.normal() * s
        return s

    def get_pos(self):
        return self.pos
    def set_pos(self, pos):
        self.pos = pos
        return self.pos_changed()
    def get_vel(self):
        return self.vel
    def set_vel(self, vel):
        self.vel = vel
        return self.pos_changed()

    def tick(self):
        self.tick_pos(self.dt)

    def tick_cpu(self, dt: Duration):
        self.dt = dt
        self.tick_pos(dt)

    def tick_pos(self, dt: Duration):
        # self.check()
        self.vel += self.acc * 0.99
        if self.max_speed:
            self.limit_speed(self.max_speed)
        self.acc = V() # V_0
        self.pos += self.vel * dt
        self.pos_changed()

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

    def repel_from(self, p, min_distance):
        dp = self.pos - p
        dir, dist = dp.normal_and_norm()
        pen = min_distance - dist
        if pen > 0:
            force = min_distance / pen
            # print(f"repel_from: d={min_distance} dist={dist} pen={pen} force={force}")
            vel = dir * force * 3.0
            self.accelerate(vel)

    def think(self):
        pass

    def draw(self, screen):
        self.sprite.draw(screen)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id}, pos={self.pos}, vel={self.vel}, acc={self.acc}, dt={self.dt})"

