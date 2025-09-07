import sys
import logging
from random import Random
from vector2d import V, V_0, V_1, V__1
from timer import Duration
from icecream import ic

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, encoding='utf-8', level=logging.DEBUG)

EMPTY_TUPLE = ()

def to_float(x):
    if isinstance(x, V):
        return x.x
    return float(x)


class Program:
    def __init__(self, name, isns = []):
        self.name = name
        self.isns = self.prepare_instructions(isns)
        self.labels = {}

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"

    __str__ = __repr__

    def prepare_instructions(self, isns):
        result = []
        ip = 0

        def emit(isn):
            result.append(isn)
            ip += 1

        for isn in isns:
            if not isinstance(isn, tuple):
                isn = (isn,)
            if isn[0] == 'label':
                self.labels[isn[1]] = ip + 1
            elif isn[0] not in ('const', 'call') and len(isn) > 1:
                for arg in reversed(isn[1:]):
                    result.append(('const', arg))
                isn = (isn[0],)
            result.append(isn)
        ic(result)
        return result

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

class CPU:
    def __init__(self, state, progs):
        self.state = state
        self.progs = progs
        self.thread_queue = []
        self.thread_by_name = {
            prog.name: Thread(prog.name, state, prog)
            for prog in self.progs
        }
        self.threads = list(self.thread_by_name.values())
        for thread in self.threads:
            thread.cpu = self
        self.thread_queue = self.threads.copy()

    def tick(self, dt: Duration):
        for thread in self.threads:
            if thread.running:
                thread.tick(dt)

    def thread_get(self, x):
        if isinstance(x, Thread):
            return x
        if isinstance(x, str):
            return self.thread_by_name[x]
        return self.threads[int(x)]

    def thread_current(self):
        return self.thread_queue.first

    def thread_next(self):
        return self.thread_queue[1] if self.thread_queue.size > 1 else self.thread_current()

    def thread_yield(self, from_thread):
        self.thread_yield_to(from_thread, self.thread_next())

    def thread_yield_to(self, from_thread, to_thread):
        to_thread = self.thread_get(to_thread)
        self.thread_queue.remove(from_thread)
        self.thread_queue.remove(to_thread)
        self.thread_queue.insert(0, to_thread)
        self.thread_queue.append(from_thread)
        from_thread.pause()
        to_thread.resume()

class Thread:
    def __init__(self, name, state, prog: Program):
        self.name = name
        self.state = state
        self._prog: Program = prog
        self._stack: list = [V_0]
        self._stack_max: int = 128
        self._ip: int = 0
        self._args: tuple = EMPTY_TUPLE
        self._isn: str = None
        self._sleep: float = 0.0
        self._rand: Random = Random()
        self._result = None
        self.running: bool = True
        self.halted: bool = False
        self.dt: Duration = 0.0

    @property
    def active(self):
        return self.running and not self.halted

    def __repr__(self):
        return f"{type(self).__name__} | state {self.state} | dt {self.dt} | isn {self._isn} | ip {self._ip} | stack {self._stack[-3:]!r} | wait {self._sleep}"

    def tick(self, dt: Duration):
        self.dt, next_isn = self.sleep_(dt)
        self.state.tick_cpu(self.dt)
        if next_isn and self.active:
            self.exec(self.fetch_isn_())
        # print(self)

    def exec(self, isn):
        # print(f"exec: {id(self.state)} {isn!r}")
        self._isn = isn
        self._args = isn
        opcode = isn[0]
        try:
            print(f"{self.name} : {self._prog.name} : {self._ip} : {isn}")
            if not isinstance(isn, tuple):
                breakpoint()
            assert isinstance(isn, tuple)
            assert isinstance(opcode, str)
            microcode = getattr(self, opcode)
            assert microcode is not None
        except (AttributeError, AssertionError) as exe:
            logger.error("%s", f"invalid ins {isn!r}")
            raise exe
        microcode()

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
        isn = self._prog.isns[ip]
        return isn

    def jmp_(self, ip_or_label):
        if isinstance(ip_or_label, str):
            self._ip = self.program.labels[ip_or_label]
        else:
            self._ip = abs(int(ip_or_label) % len(self._prog.isns))

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
    def label(self):
        pass
    def pause(self):
        self.running = False
    def resume(self):
        self.running = True
    def halt(self):
        self.running = False
        self.halted = True
    def repeat(self):
        self._ip = 0
    def br(self):
        loc = self.pop_()
        c = self.pop_()
        if to_float(c)> 0:
            self.ip_(loc)
    def jmp(self):
        self.jmp_(self.pop_())
    def thread_yield(self):
        self.cpu.thread_yield(self)
    def thread_yield_to(self):
        self.cpu.thread_yield_to(self, self._args[1])
    def sleep(self):
        self._sleep = to_float(self.pop_(V_0))

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
        self.push_(self._args[1])

    # Arithmetic:
    def rand(self):
        r2 = self.pop_(V__1)
        r1 = self.pop_(V_1)
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
        self.push_(self.pop_(V_0).norm())
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

