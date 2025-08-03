from random import Random
from vector2d import Vector2D
import math
from icecream import ic

V = Vector2D
ZERO = V()
NEG_1 = V(-1, -1)
POS_1 = V(1, 1)

class Program:
    def __init__(self, isns = []):
        self.isns = isns

class State:
    def __init__(self):
        self.pos: V = ZERO
        self.vel: V = ZERO

    def tick(self, dt: float):
        self.pos += self.vel * dt

    def acc(self, a):
        print(f"a={a} dp={self.vel}")
        self.vel += a

class CPU:
    def __init__(self, state, prog: Program):
        self.state = state
        self._prog: Program = prog
        self._stack: list = [ZERO]
        self._ip: int = 0
        self._arg: V = ZERO
        self._isn: str = None
        self._sleep: float = 0.0
        self._rand: Random = Random()
        self.dt: float = 0.0

    def __repr__(self):
        return f"CPU | state {self.state} | dt {self.dt} | isn {self._isn} | ip {self._ip} | stack {self._stack[-3:]!r} | wait {self._sleep}"

    def tick(self, dt: float):
        self.dt, next_isn = self.sleep_(dt)
        self.state.cpu_tick(self.dt)
        if next_isn:
            self.exec(self.isn_())
        # print(self)

    def exec(self, isn):
        if isinstance(isn, tuple):
            isn, self._arg = isn
        else:
            self._arg = ZERO
        self._isn = isn
        proc = getattr(self, isn)
        proc()

    # Microcode:
    def sleep_(self, dt):
        next_isn = True
        if self._sleep > 0:
            next_isn = False
            self._sleep -= dt
        if self._sleep <= 0:
            next_isn = True
            dt += self._sleep
            self._sleep = 0
        return dt, next_isn

    def isn_(self):
        ip = self._ip
        self._ip += 1
        if self._ip >= len(self._prog.isns):
            ip = self._ip = 0
        isn = self._prog.isns[ip]
        return isn

    def jmp_(self, ip):
        self._ip = int(abs(math.fmod(ip, len(self._prog.isns))))

    def top_(self, default = ZERO):
        return self._stack[-1] if self._stack else default

    def push_(self, val):
        self._stack.append(val)

    def pop_(self, default):
        if self._stack:
            return self._stack.pop()
        else:
            return default

    def pop2_(self, default):
        b = self.pop_(default)
        a = self.pop_(default)
        return a, b

    # Instructions:
    def pop(self):
        if self._stack:
            self._stack.pop()
    def dup(self):
        if self._stack:
            self._stack.push(-1, self.top_())
    def const(self):
        self.push_(V.coerce(self._arg))
    def rand(self):
        r1 = self.pop_(NEG_1)
        r2 = self.pop_(POS_1)
        r = V.random(r1, r2, self._rand)
        # print(f"r1={r1} r2={r2} r={r}")
        self.push_(r)
    def pos(self):
        self.push_(self.state.pos)
    def vel(self):
        self.push_(self.state.vel)
    def acc(self):
        a = self.pop_(ZERO)
        self.state.acc(a)
    def inv(self):
        arg = self.pop_(self.top_())
        self.push_(- arg)
    def add(self):
        a, b = self.pop2_(ZERO)
        self.push_(a + b)
    def sub(self):
        a, b = self.pop2_(ZERO)
        self.push_(a - b)
    def mul(self):
        a, b = self.pop2_(POS_1)
        self.push_(a * b)
    def div(self):
        a, b = self.pop2_(POS_1)
        b_ = V(b.x, b.y)
        if b.x == 0:
            b_.x = 1
        if b.y == 0:
            b_.y = 1
        self.push_(a / b_)
    def sleep(self):
        self._sleep = self.pop_(ZERO).x
    def br(self):
        di = self.isn_()
        c = self.pop_()
        if c.x > 0:
            self.ip_(self.isn + di.x)
    def jmp(self):
        self.jmp_(self.pop_(ZERO).x)

