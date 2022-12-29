# credits:  https://www.reddit.com/r/adventofcode/comments/zu28ij/comment/j1hioch/?utm_source=share&utm_medium=web2x&context=3
# nice heap solution
import heapq


def load_data(path: str):
    [*lines] = open(path)

    return [s.strip('\n') for s in lines]


def _search(lines, start, end, time=0):
    end_x, end_y = end
    seen, queue = {(start, time)}, [(0, (start, time))]
    while queue:
        position, time = heapq.heappop(queue)[1]
        if position == end:
            return time
        x, y = position
        time += 1
        for x, y in [(x - 1, y), (x, y - 1), (x, y), (x, y + 1), (x + 1, y)]:
            if y < 0 or y >= len(lines) or x < 1 or x >= len(line := lines[y]) - 1:
                continue
            if y in (0, len(lines) - 1):
                if line[x] != ".":
                    continue
            elif lines[y][(x - 1 + time) % (len(line) - 2) + 1] == "<":
                continue
            elif lines[y][(x - 1 - time) % (len(line) - 2) + 1] == ">":
                continue
            elif lines[(y - 1 + time) % (len(lines) - 2) + 1][x] == "^":
                continue
            elif lines[(y - 1 - time) % (len(lines) - 2) + 1][x] == "v":
                continue
            state = ((x, y), time)
            if state not in seen:
                seen.add(state)
                heapq.heappush(queue, (time + abs(x - end_x) + abs(y - end_y), state))
    raise LookupError()


def exit_blizzard_maze(data: list[str], stupid_elf: bool) -> int:
    S, E = (1, 0), (len(data[-1]) - 2, len(data) - 1)
    return _search(data, S, E) if not stupid_elf else _search(data, S, E, _search(data, E, S, _search(data, S, E)))


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert exit_blizzard_maze(assert_data, stupid_elf=False) == 18
    assert exit_blizzard_maze(assert_data, stupid_elf=True) == 54

    input_data = load_data('./input.txt')
    # part 1
    print(exit_blizzard_maze(input_data, stupid_elf=False))
    # part 2
    print(exit_blizzard_maze(input_data, stupid_elf=True))

