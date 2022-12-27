import re


def load_data(path: str):
    with open(path) as f:
        *grid, _, path = open(path)

    return (*map(lambda x: x.strip('\n'), grid),
            re.findall(r'(\d+)([RL]?)', path.strip('\n')))


def wrap(p: complex, dir: complex, grid: dict[complex, str]):
    match dir:
        # wrap around from right to left
        case 1j:  return complex(p.real, min(map(lambda x: x.imag, filter(lambda x: x.real == p.real, grid.keys()))))
        # wrap around from left to right
        case -1j: return complex(p.real, max(map(lambda x: x.imag, filter(lambda x: x.real == p.real, grid.keys()))))
        # wrap around from bottom to top
        case 1:   return complex(min(map(lambda x: x.real, filter(lambda x: x.imag == p.imag, grid.keys()))), p.imag)
        # wrap around from top to bottom
        case -1:  return complex(max(map(lambda x: x.real, filter(lambda x: x.imag == p.imag, grid.keys()))), p.imag)


def decode(r: int, c: int, dir: complex):
    match dir:
        case 1j:  return 1000 * (r + 1) + 4 * (c + 1) + 0
        case 1:   return 1000 * (r + 1) + 4 * (c + 1) + 1
        case -1j: return 1000 * (r + 1) + 4 * (c + 1) + 2
        case -1:  return 1000 * (r + 1) + 4 * (c + 1) + 3


def find_password(data: tuple[tuple, list]):
    *grid, path = data
    p, dir = grid[0].index('.') * 1j, 1j
    grid = {(x+y*1j): c
            for x, r in enumerate(grid)
            for y, c in enumerate(r)
            if c in '.#'}

    for step, turn in path:
        if not turn: break
        for _ in range(int(step)):
            p += dir
            if p not in grid:
                p -= dir
                tmp = wrap(p, dir, grid)
                if grid[tmp] == '#':
                    break
                p = tmp
            if grid[p] == '#':
                p -= dir
                break
        if turn == 'L': dir *= 1j
        elif turn == 'R': dir *= -1j

    return decode(p.real, p.imag, dir)


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert find_password(assert_data) == 6032

    input_data = load_data('./input.txt')
    # part 1
    print(find_password(input_data))
    # part 2

