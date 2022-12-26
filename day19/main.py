# credits to https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tvzgz/?utm_source=share&utm_medium=web2x&context=3
# solution was way too beautiful. i can't compete with that

import re
from dataclasses import dataclass

import numpy as np


A = lambda *x: np.array(x)


def load_data(path: str):
    pattern = r'\d+'
    with open(path) as f:
        lines = [[int(x) for x in re.findall(pattern, s)] for s in f.readlines()]

    return lines


@dataclass
class Blueprint:
    log: list[str]

    def parse_blueprint(self):
        id, *ores = self.log
        return (id, (A(0, 0, 0, ores[0]), A(0, 0, 0, 1)),
                    (A(0, 0, 0, ores[1]), A(0, 0, 1, 0)),
                    (A(0, 0, ores[3], ores[2]), A(0, 1, 0, 0)),
                    (A(0, ores[5], 0, ores[4]), A(1, 0, 0, 0)),
                    (A(0, 0, 0, 0), A(0, 0, 0, 0)))


def prune(state: tuple[np.array, np.array]):
    key = lambda x: tuple(x[0] + x[1]) + tuple(x[1])
    return sorted({key(x): x for x in state}.values(), key=key)[-1500:]


def simulate_blueprint(blueprint: Blueprint, t: int):
    _, *bprint = blueprint.parse_blueprint()

    stack = [(A(0, 0, 0, 0), A(0, 0, 0, 1))] # current state: we have 0 ores and 1 robot that makes 1 ore/min
    for _ in range(t, 0, -1):
        tmp_stack = []
        for have, make in stack:
            for cost, ores in bprint:
                if all(cost <= have):
                    tmp_stack.append((have - cost + make, ores + make))
        stack = prune(tmp_stack)

    return max(have[0] for have, _ in stack)


def simulation(data: list[str], t: int, naughty_elephants: bool):
    ans = 0 if not naughty_elephants else 1
    for i, blueprint in enumerate(map(Blueprint, data), start=1):
        if not naughty_elephants: ans += simulate_blueprint(blueprint, t) * i
        else:
            if i < 4: ans *= simulate_blueprint(blueprint, t)

    return ans

if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert simulation(assert_data, t=24, naughty_elephants=False) == 33
    assert simulation(assert_data, t=32, naughty_elephants=True) == 3472


    input_data = load_data('./input.txt')
    # part 1
    print(simulation(input_data, t=24, naughty_elephants=False))
    # part 2
    print(simulation(input_data, t=32, naughty_elephants=True))

