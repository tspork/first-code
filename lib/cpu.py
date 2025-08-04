import math
from random import Random
from vector2d import V, V_0, V_1, V__1
from timer import Duration
from icecream import ic

EMPTY_TUPLE = ()

class Program:
    def __init__(self, name, isns = []):
        self.name = name
        self.isns = isns
    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"
    __str__ = __repr__

class State:
    def __init__(self):
        self.pos: V = V()
        self.vel: V = V()
        self.dt = None

    def tick(self):
        self.pos += self.vel * self.dt

    def acc(self, a):
        assert isinstance(a, V)
        #print(f"a={a} dp={self.vel}")
        self.vel += a

class Thread:
    def __init__(self, name, state, prog: Program):
        self.name = name
        self.state = state
        self._prog: Program = prog
        self._stack: list = [V_0]
        self._stack_max: int = 32
        self._ip: int = 0
        self._args: tuple = EMPTY_TUPLE
        self._isn: str = None
        self._sleep: float = 0.0
        self._rand: Random = Random()
        self._running: bool = True
        self._result = None
        self._terminated: bool = False
        self.dt: Duration = 0.0

    def __repr__(self):
        return f"CPU | state {self.state} | dt {self.dt} | isn {self._isn} | ip {self._ip} | stack {self._stack[-3:]!r} | wait {self._sleep}"

    def tick(self, dt: Duration):
        self.dt, next_isn = self.sleep_(dt)
        self.state.tick_cpu(self.dt)
        if next_isn and self._running:
            self.exec(self.fetch_isn_())
        # print(self)

    def exec(self, isn):
        # print(f"exec: {id(self.state)} {isn!r}")
        self._isn = isn
        if isinstance(isn, tuple):
            opcode = isn[0]
            self._args = isn
        else:
            opcode = isn
            self._args = EMPTY_TUPLE
        proc = getattr(self, opcode)
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

    def fetch_isn_(self):
        ip = self._ip
        self._ip += 1
        if self._ip >= len(self._prog.isns):
            self._ip = 0
        isn = self._prog.isns[ip]
        return isn

    def jmp_(self, ip):
        self._ip = abs(int(ip % len(self._prog.isns)))

    def top_(self, default = V_0):
        return self._stack[-1] if self._stack else default

    def push_(self, val):
        self._stack.append(val)
        if len(self._stack) > self._stack_max:
            self._stack = self._stack[- self._stack_max:]

    def pop_(self, value):
        if self._stack:
            value = self._stack.pop()
        self._result = value
        return value

    def pop2_(self, default):
        b = self.pop_(default)
        a = self.pop_(default)
        return a, b

    # Instructions:

    # Control Flow:
    def nop(self):
        pass
    def halt(self):
        self._running = False
    def sleep(self):
        self._sleep = self.pop_(V_0).x
    def br(self):
        di = self.fetch_isn_()
        c = self.pop_()
        if c.x > 0:
            self.ip_(self.isn + di.x)
    def jmp(self):
        self.jmp_(self.pop_(V_0).x)

    # Stack:
    def pop(self):
        if self._stack:
            self._stack.pop()
    def push(self):
        self._stack.push(-1, self._result)
    def dup(self):
        if self._stack:
            self._stack.push(-1, self.top_())
    def const(self):
        self.push_(V.coerce(self._args[1]))

    # Arithmetic:
    def rand(self):
        r1 = self.pop_(V__1)
        r2 = self.pop_(V_1)
        r = V.random(r1, r2, self._rand)
        # print(f"r1={r1} r2={r2} r={r}")
        self.push_(r)
    def inv(self):
        arg = self.pop_(self.top_())
        self.push_(- arg)
    def add(self):
        a, b = self.pop2_(V_0)
        self.push_(a + b)
    def sub(self):
        a, b = self.pop2_(V_0)
        self.push_(a - b)
    def mul(self):
        a, b = self.pop2_(V_1)
        self.push_(a * b)
    def div(self):
        a, b = self.pop2_(V_1)
        b_ = V(b.x, b.y)
        if b.x == 0:
            b_.x = 1
        if b.y == 0:
            b_.y = 1
        self.push_(a / b_)
    def abs(self):
        self.push_(abs(self.pop(V_0)))
    def norm(self):
        self.push_(V.coerce(self.pop_(V_0).norm()))
    def normal(self):
        self.push_(self.pop_(V_0).normal())
    def rotate(self):
        v, angle = self.pop_2(V_0)
        self.push_(v.rotate(angle.x))

    # State instructions:
    def call(self):
        # print(f"call: {self.state} {self._args!r}")
        # breakpoint()
        self._result = getattr(self.state, self._args[1])(*self._args[2:])
    # Shorthand:
    def acc(self):
        self._result = self.state.accelerate(self.pop_(V_0))
    # def think(self):
    #    self._result = self.state.think()

class CPU(Thread):
    def __init__(self, state, prog: Program):
        super().__init__(self, state, prog)
        self.threads = {}

    def spawn(self, name, prog):
        self.threads[name] = Thread(name, self.state, prog)
