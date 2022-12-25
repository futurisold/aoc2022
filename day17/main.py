# credits to Jonathan Paulson: https://www.youtube.com/watch?v=QXTBseFzkW4

def load_data(path: str):
    with open(path) as f:
        lines = f.readlines().pop()

    return lines.strip('\n')


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'


def get_rock_shape(idx: int, y_max: int):
    assert idx < 5
    if idx == 0: return [Point(2, y_max), Point(3, y_max), Point(4, y_max), Point(5, y_max)]
    elif idx == 1: return [Point(3, y_max+2), Point(2, y_max+1), Point(3, y_max+1), Point(4, y_max+1), Point(3, y_max)]
    elif idx == 2: return [Point(2, y_max), Point(3, y_max), Point(4, y_max), Point(4, y_max+1), Point(4, y_max+2)]
    elif idx == 3: return [Point(2, y_max), Point(2, y_max+1), Point(2, y_max+2), Point(2, y_max+3)]
    elif idx == 4: return [Point(2, y_max+1), Point(2, y_max), Point(3, y_max+1), Point(3, y_max)]
    else: raise ValueError


def move_left(rock: list[Point]):
    if any([p.x == 0 for p in rock]): return rock
    return {Point(p.x-1, p.y) for p in rock}


def move_right(rock: list[Point]):
    if any([p.x == 6 for p in rock]): return rock
    return {Point(p.x+1, p.y) for p in rock}


def move_down(rock: list[Point]): return {Point(p.x, p.y-1) for p in rock}


def move_up(rock: list[Point]): return {Point(p.x, p.y+1) for p in rock}


def higher_rock_formation(baseline: set[Point], size: int = 30):
    y_max = max([p.y for p in baseline])
    return frozenset([Point(p.x, y_max-p.y) for p in baseline if y_max - p.y <= size])


def simulate_falling(jet_pattern: str, cycles: int, trust_issues: bool):
    y_max, hrf_y_max = 0, 0
    i, c = 0, 0
    baseline = set([Point(x, 0) for x in range(7)])
    seen ={}
    while c < cycles:
        rock = get_rock_shape(c%5, y_max+4)
        while True:
            jet = jet_pattern[i]
            if jet == '<':
                rock = move_left(rock)
                if rock & baseline: rock = move_right(rock) # undo if collision
            else:
                rock = move_right(rock)
                if rock & baseline: rock = move_left(rock) # undo if collision
            rock = move_down(rock)
            i = (i+1) % len(jet_pattern)
            if rock & baseline:
                rock = move_up(rock) # undo if collision
                baseline |= rock
                y_max = max([p.y for p in baseline])
                cur = (i, c%5, higher_rock_formation(baseline))
                if cur in seen and c > 2021:
                    c_old, hrf_old = seen[cur] # when & what have we seen before
                    dc = c - c_old
                    dy = y_max - hrf_old
                    jump = (cycles - c) // dc # how many cycles to jump
                    hrf_y_max += jump * dy
                    c += jump * dc
                seen[cur] = (c, y_max)
                break

        c += 1
        if not trust_issues and c == cycles: return y_max

    return y_max + hrf_y_max


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert simulate_falling(assert_data, cycles=2022, trust_issues=False) == 3068
    assert simulate_falling(assert_data, 1_000_000_000_000, trust_issues=True) == 1514285714288

    input_data = load_data('./input.txt')
    # part 1
    print(simulate_falling(input_data, cycles=2022, trust_issues=False))
    # part 2
    print(simulate_falling(input_data, cycles=1_000_000_000_000, trust_issues=True))


