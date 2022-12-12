import pathlib
from collections import defaultdict


def load_data(path: str):
    with open(path) as f:
        lines = [s.strip().split() for s in f.readlines()]

    return lines


def get_total_sz(data: list[str], max_sz: int, free_space: bool):
    path = []
    sizes = defaultdict(int)

    for line in data:
        if line[0] == '$':
            if line[1] == 'cd':
                if line[2] == '..': path.pop()
                else: path.append(line[2])
            elif line[1] == 'ls': continue
        elif line[0].isdigit():
            cur = pathlib.Path(*path)
            sizes[cur] += int(line[0])

            if cur.stem: sizes[pathlib.Path(cur.root)] += int(line[0])

            parent = cur.parent
            while str(parent) != '/':
                sizes[parent] += int(line[0])
                parent = parent.parent

    if free_space: return min(filter(lambda x: x >= sizes[pathlib.Path('/')] - 40_000_000, sizes.values()))
    else: return sum(filter(lambda x: x <= max_sz, sizes.values()))


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert get_total_sz(assert_data, max_sz=100_000, free_space=False) == 95437
    assert get_total_sz(assert_data, max_sz=100_000, free_space=True) == 24933642

    input_data = load_data('./input.txt')
    # part 1
    print(get_total_sz(input_data, max_sz=100_000, free_space=False))
    # part 2
    print(get_total_sz(input_data, max_sz=100_000, free_space=True))

