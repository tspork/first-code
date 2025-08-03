from cpu import Program, V, CPU

prog = Program(
    [
        ('const', V(-5.0, -5.0)),
        ('const', V(5.0, 5.0)),
        'rand',
        'acc',
        ('const', 0.03),
        'sleep',
    ]
)

cpu = CPU(prog)

t0, t1 = 0.0, 10.0
t = t0
dt = 0.01
while t < t1:
    t += dt
    cpu.tick(dt)
    print(cpu)
