import sys
from collections import deque
from dataclasses import dataclass


def load_data(path: str):
    [*lines] = open(path)

    return [s.strip('\n') for s in lines]


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self): return hash((self.x, self.y))

    def __eq__(self, other): return self.x == other.x and self.y == other.y

    def __repr__(self): return f'Point({self.x}, {self.y})'

    def __add__(self, other): return Point(self.x + other.x, self.y + other.y)

    @property
    def neighbors(self):
        # neighbors in all directions
        return {
            Point(self.x - 1, self.y),     # north
            Point(self.x + 1, self.y),     # south
            Point(self.x, self.y + 1),     # east
            Point(self.x, self.y - 1),     # west
            Point(self.x - 1, self.y + 1), # northeast
            Point(self.x + 1, self.y + 1), # southeast
            Point(self.x - 1, self.y - 1), # northwest
            Point(self.x + 1, self.y - 1), # southwest
        }


def empty_tiles(grid: set[Point]) -> int:
    top    = min(grid, key=lambda p: p.y).y
    bottom = max(grid, key=lambda p: p.y).y
    left   = min(grid, key=lambda p: p.x).x
    right  = max(grid, key=lambda p: p.x).x
    grid_size = (right - left + 1) * (bottom - top + 1)

    return grid_size - len(grid)


def simulation(data: list, rounds: int, freeze: bool):
    grid = {Point(i, j) for i, r in enumerate(data) for j, c in enumerate(r) if c == '#'}
    dirs = deque([
        (Point(-1, 0), Point(-1, 1), Point(-1, -1)), # N, NE, NW
        (Point(1, 0), Point(1, 1), Point(1, -1)),    # S, SE, SW
        (Point(0, -1), Point(-1, -1), Point(1, -1)), # W, NW, SW
        (Point(0, 1), Point(-1, 1), Point(1, 1))     # E, NE, SE
    ])

    state = grid.copy()
    for _ in range(rounds):
        moves = {} # old : new
        for p in grid:
            if (p.neighbors & grid):
                for dir in dirs:
                    if not any(p + d in grid for d in dir):
                        moves[p] = p + dir[0]
                        break

        for old in moves:
            [*collision] = map(lambda x: x if x != old and moves[x] == moves[old] else None, moves)
            if not any(collision):
                grid -= {old}
                grid |= {moves[old]}

        if not freeze and (_ + 1) == rounds: return empty_tiles(grid)
        if state == grid: return _ + 1

        dirs.append(dirs.popleft())
        state = grid.copy()


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    simulation(assert_data, rounds=10, freeze=False) == 110
    simulation(assert_data, rounds=sys.maxsize, freeze=True) == 20

    input_data = load_data('./input.txt')
    # part 1
    print(simulation(input_data, rounds=10, freeze=False))
    # part 2
    print(simulation(input_data, rounds=sys.maxsize, freeze=True))

