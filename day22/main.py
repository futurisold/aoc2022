import re


def load_data(path: str):
    *grid, _, path = open(path)

    return (*map(lambda x: x.strip('\n'), grid),
            re.findall(r'(\d+)([RL]?)', path.strip('\n')))


def wrap_around_torus(p: complex, dir: complex, grid: dict[complex, str]):
    match dir:
        # wrap around from right to left
        case 1j:  return complex(p.real, min(map(lambda x: x.imag, filter(lambda x: x.real == p.real, grid.keys()))))
        # wrap around from left to right
        case -1j: return complex(p.real, max(map(lambda x: x.imag, filter(lambda x: x.real == p.real, grid.keys()))))
        # wrap around from bottom to top
        case 1:   return complex(min(map(lambda x: x.real, filter(lambda x: x.imag == p.imag, grid.keys()))), p.imag)
        # wrap around from top to bottom
        case -1:  return complex(max(map(lambda x: x.real, filter(lambda x: x.imag == p.imag, grid.keys()))), p.imag)


def wrap_around_cube(p: complex, dir: complex):
    match dir, p.real//50, p.imag//50:
        case  1j, 0, _: return complex(149-p.real, 99), -1j
        case  1j, 1, _: return complex( 49,p.real+ 50), -1
        case  1j, 2, _: return complex(149-p.real,149), -1j
        case  1j, 3, _: return complex(149,p.real-100), -1
        case -1j, 0, _: return complex(149-p.real,  0),  1j
        case -1j, 1, _: return complex(100,p.real- 50),  1
        case -1j, 2, _: return complex(149-p.real, 50),  1j
        case -1j, 3, _: return complex(  0,p.real-100),  1
        case  1 , _, 0: return complex(  0,p.imag+100),  1
        case  1 , _, 1: return complex(100+p.imag, 49), -1j
        case  1 , _, 2: return complex(-50+p.imag, 99), -1j
        case -1 , _, 0: return complex( 50+p.imag, 50),  1j
        case -1 , _, 1: return complex(100+p.imag,  0),  1j
        case -1 , _, 2: return complex(199,p.imag-100), -1


def decode(r: int, c: int, dir: complex):
    match dir:
        case 1j:  return 1000 * (r + 1) + 4 * (c + 1) + 0
        case 1:   return 1000 * (r + 1) + 4 * (c + 1) + 1
        case -1j: return 1000 * (r + 1) + 4 * (c + 1) + 2
        case -1:  return 1000 * (r + 1) + 4 * (c + 1) + 3


def find_password(data: tuple[tuple, list], fold: bool):
    *grid, path = data
    p, dir = grid[0].index('.') * 1j, 1j
    grid = {(x+y*1j): c
            for x, r in enumerate(grid)
            for y, c in enumerate(r)
            if c in '.#'}

    for step, turn in path:
        for _ in range(int(step)):
            _p, _d = p + dir, dir
            if _p not in grid:
                if fold: _p, _d = wrap_around_cube(_p, _d)
                else: _p = wrap_around_torus(_p, _d, grid)
            if grid[_p] == '.':
                p, dir = _p, _d
        if turn == 'L': dir *= 1j
        elif turn == 'R': dir *= -1j

    return decode(p.real, p.imag, dir)


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert find_password(assert_data, fold=False) == 6032
    assert find_password(assert_data, fold=True)  == 5031

    input_data = load_data('./input.txt')
    # part 1
    print(find_password(input_data, fold=False))
    # part 2
    print(find_password(input_data, fold=True))

