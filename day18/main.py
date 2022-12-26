from copy import deepcopy
from dataclasses import dataclass


def load_data(path: str):
    with open(path) as f:
        lines = [Cube(*[int(x) for x in s.strip().split(',')]) for s in f.readlines()]

    return set(lines)


@dataclass
class Cube:
    x: int
    y: int
    z: int

    def __hash__(self): return hash((self.x, self.y, self.z))

    def __eq__(self, other): return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self): return f'Cube({self.x}, {self.y}, {self.z})'

    @property
    def tuple(self): return self.x, self.y, self.z


def side_intersection(c1: Cube, c2: Cube):
    return (c1.x == c2.x and c1.y == c2.y and abs(c1.z - c2.z) == 1) or \
           (c1.x == c2.x and c1.z == c2.z and abs(c1.y - c2.y) == 1) or \
           (c1.y == c2.y and c1.z == c2.z and abs(c1.x - c2.x) == 1)


def get_adjacent_cubes(c: Cube):
    return set(map(lambda x: Cube(*x), ((c.x+1, c.y, c.z),
                                        (c.x-1, c.y, c.z),
                                        (c.x, c.y+1, c.z),
                                        (c.x, c.y-1, c.z),
                                        (c.x, c.y, c.z+1),
                                        (c.x, c.y, c.z-1))))


def surface_area(cubes: set[Cube], holes: bool) -> int:
    if not holes:
        # part 1
        surface = 0
        for cube in cubes:
            for adjcube in get_adjacent_cubes(cube):
                if adjcube not in cubes:
                    surface += 1
        return surface

    # part 2
    # flood fill algo
    seen = set()
    lb = -1 # lower bound
    ub = max(max(c.tuple) for c in cubes) + 1 # upper bound
    stack = [Cube(*(lb, lb, lb))]
    while stack:
        cube = stack.pop()
        stack += [adjcube for adjcube in (get_adjacent_cubes(cube) - cubes - seen) if all(-1 <= s <= ub for s in adjcube.tuple)]
        seen.add(cube)

    return sum((adjcube in seen) for cube in cubes for adjcube in get_adjacent_cubes(cube))


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert surface_area(assert_data, holes=False) == 64
    assert surface_area(assert_data, holes=True) == 58

    input_data = load_data('./input.txt')
    # part 1
    print(surface_area(input_data, holes=False))
    # part 2
    print(surface_area(input_data, holes=True))

