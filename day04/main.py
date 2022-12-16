def load_data(path: str):
    with open(path) as f:
        lines = [s.strip() for s in f.readlines()]

    return lines


def get_ranges(pair: str):
    elf1_id, elf2_id = pair.split(',')
    elf1_interval = tuple([int(n) for n in elf1_id.split('-')])
    elf2_interval = tuple([int(n) for n in elf2_id.split('-')])

    return elf1_interval, elf2_interval


def full_overlap(ranges: tuple[tuple]):
    pair1 = set(range(ranges[0][0], ranges[0][1]+1))
    pair2 = set(range(ranges[1][0], ranges[1][1]+1))
    interval = pair1.intersection(pair2)

    return len(interval) == len(pair1) or len(interval) == len(pair2)


def partial_overlap(ranges: tuple[tuple]):
    pair1 = set(range(ranges[0][0], ranges[0][1]+1))
    pair2 = set(range(ranges[1][0], ranges[1][1]+1))
    interval = pair1.intersection(pair2)

    return bool(len(interval))


def total_overlaps(pairs: list[str], partial: bool):
    if partial: return sum(map(partial_overlap, map(get_ranges, pairs)))
    else: return sum(map(full_overlap, map(get_ranges, pairs)))


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert total_overlaps(assert_data, partial=False) == 2
    assert total_overlaps(assert_data, partial=True) == 4

    input_data = load_data('./input.txt')
    # part 1
    print(total_overlaps(input_data, partial=False))
    # part 2
    print(total_overlaps(input_data, partial=True))

