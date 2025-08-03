# Ideas

## Use a genetic algoritm to train enemies

Instructions

| ISN | ARG | STACK | STACK | COMMENT |
|-----|-----|-------|-------|---------|
| pop | | X | ... |
| dup | | X | ... X X |
| constant | X | ... X | |
| random | | X | ... (-1, 1) | |
| accelerate | | A | ... | change DP by A * dt
| not | | A | ! A |
| add | | A B | A + B
| sub | | A B | A - B
| mul | | A B | A * B
| div | | A B | A / B (A if B zero)
| pause | seconds | ...
| branch | di | A | goto |
| jmp | isn | | | |
| hit_by_player | | RELATIVE_LOCATION |
| see_player | RELATIVE_LOCATION |
