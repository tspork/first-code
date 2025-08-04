from timer import Duration
from entity import Entity, Duration, V
from cpu import CPU

class Enemy(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.player = kwargs['player']
        # self.programs: list = kwargs['programs']
        self.cpus: list = [CPU(self, prog) for prog in self.programs]
        # print(f"cpus={self.cpus!r}")

    def tick(self):
        for cpu in self.cpus:
            cpu.tick(self.dt)
        # if self.avoid_bullets():

    def tick_cpu(self, dt: Duration):
        self.tick_pos(dt)

    def think(self):
        'Change direction to player.'
        self.move_toward_player()

    def avoid_bullets(self):
        # print(f"avoid_bullets: {self}")
        for bullet in self.game.bullets:
            # print(f"avoid_bullets: {bullet}")
            r0 = self.sprite.size.x
            r1 = r0 * 2
            if self.avoid_point(bullet.pos, r0, r1):
                return True
        return False

    def move_toward_player(self):
        self.move_toward(self.player.pos, 0.5)
