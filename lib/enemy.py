from timer import Duration
from entity import Entity, Duration, V
from cpu import CPU

class Enemy(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cpu: CPU = CPU(self, self.programs)

    def tick(self):
        self.cpu.tick(self.dt)
        # if self.avoid_bullets():

    def tick_cpu(self, dt: Duration):
        self.tick_pos(dt)

    def think(self):
        'Change direction to player.'
        self.move_toward_player()

    def avoid_bullets(self):
        # print(f"avoid_bullets: {self}")

        def distance(bullet):
            return (bullet.pos - self.pos).norm()

        for bullet in sorted(self.game.bullets, key=distance):
            # print(f"avoid_bullets: {bullet}")
            r0 = self.sprite.size.x
            r1 = r0 * 3
            if self.avoid_point(bullet.pos, r0, r1):
                return True
        return False

    def move_toward_player(self):
        self.move_toward(self.player.pos, 0.5)
