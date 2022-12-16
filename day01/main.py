def load_data(path: str):
    with open(path, 'r') as f:
        lines = f.readlines() + ['\n']

    i = 0
    seq = []
    buffer = []
    while i < len(lines):
        cur = lines[i]
        if cur != '\n': buffer.append(int(cur.strip()))
        else:
            seq.append(buffer)
            buffer = []
        i += 1

    return seq


def top_elf(calories: list[int]):
    return max(map(sum, calories))


def top3_elves(calories: list[int]):
    return sum(sorted(map(sum, calories), reverse=True)[:3])

if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert top_elf(assert_data) == 24_000
    assert top3_elves(assert_data) == 45_000

    input_data = load_data('./input.txt')
    # part 1
    print(top_elf(input_data))
    # part 2
    print(top3_elves(input_data))

