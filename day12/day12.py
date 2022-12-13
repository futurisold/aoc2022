from collections import deque
from string import ascii_lowercase


def load_data(path: str):
    with open(path) as f:
        lines = [list(s.strip()) for s in f.readlines()]

    return lines


def shortest_path(grid: list[list[int]], start: str):
    heights = {chr: i for i, chr in enumerate('S' + ascii_lowercase + 'E')}
    all_paths = []
    queue = deque()
    r, c = len(grid), len(grid[0])
    for i in range(r):
            for j in range(c):
                if grid[i][j] == start:
                    queue.append(((i, j), 0))
                    visited = {(i, j)}
                    while queue:
                        (i, j), steps = queue.popleft()
                        height = heights[grid[i][j]]
                        if grid[i][j] == 'E': all_paths.append(steps)

                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            ni, nj = i + di, j + dj
                            if (ni, nj) in visited: continue
                            if any([ni < 0, ni >= len(grid), nj < 0, nj >= len(grid[0])]): continue
                            if (heights[grid[ni][nj]] - height) > 1: continue
                            if (heights[grid[ni][nj]] - height) < 0: queue.append(((ni, nj), steps-1))
                            else: queue.append(((ni, nj), steps+1))

                            visited.add((ni, nj))

    return min(all_paths)


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert shortest_path(assert_data, 'S') == 31

    input_data = load_data('./input.txt')
    # part 1
    print(shortest_path(input_data, 'S'))
    # part 2
    print(shortest_path(input_data, 'a'))

