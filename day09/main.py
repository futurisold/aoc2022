from collections import defaultdict
from itertools import repeat


def load_data(path: str):
    with open(path) as f:
        lines = [s.strip() for s in f.readlines()]

    return lines


def update(h: tuple[int], t: tuple[int]):
    dr = abs(h[0] - t[0])
    dc = abs(h[1] - t[1])
    if dr <= 1 and dc <= 1: pass
    elif dr >= 2 and dc >= 2:
        t = (h[0] - 1 if t[0] < h[0] else h[0] + 1,
             h[1] - 1 if t[1] < h[1] else h[1] + 1)
    elif dr >= 2:
        t = (h[0] - 1 if t[0] < h[0] else h[0] + 1,
             h[1])
    elif dc >= 2:
        t = (h[0],
             h[1] - 1 if t[1] < h[1] else h[1] + 1)

    return t

def recurrent_tail_positions(moves: list[str], knots: int):
    # h == head, t == tail, d == direction, s == steps
    h = (0, 0)
    t = [h for _ in range(knots-1)] if knots == 10 else h
    dr = {'L':0, 'R':0, 'U':-1, 'D':1}
    dc = {'L':-1, 'R':1, 'U':0, 'D':0}
    tpos = set()

    if knots == 10: tpos.add(t[-1])
    else: tpos.add(t)

    for move in moves:
        d = move[0]
        s = int(move[1:])
        for _ in range(s):
            h = (h[0] + dr[d], h[1] + dc[d])
            if knots == 10:
                t[0] = update(h, t[0])
                for i in range(1, knots-1):
                    t[i] = update(t[i-1], t[i])
                tpos.add(t[-1])
            else:
                t = update(h, t)
                tpos.add(t)

    return len(tpos)

if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert recurrent_tail_positions(assert_data, knots=2) == 13
    assert recurrent_tail_positions(assert_data, knots=10) == 1

    input_data = load_data('./input.txt')
    # part 1
    print(recurrent_tail_positions(input_data, knots=2))
    # part 2
    print(recurrent_tail_positions(input_data, knots=10))

