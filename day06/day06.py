from functools import partial


def load_data(path: str):
    with open(path) as f:
        lines = [s.strip() for s in f.readlines()]

    return lines


def find_marker(datastream: str, buffer_sz: int):
    buffer = []

    i = 0
    while i < len(datastream):
        while i < buffer_sz:
            buffer.append(datastream[i])
            i += 1

        if len(set(buffer[-buffer_sz:])) == buffer_sz: return i

        buffer.append(datastream[i])
        i += 1


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert sum(map(partial(find_marker, buffer_sz=4), assert_data)) == 32
    assert sum(map(partial(find_marker, buffer_sz=14), assert_data)) == 101

    input_data = load_data('./input.txt').pop()
    # part 1
    print(find_marker(input_data, buffer_sz=4))
    # part 2
    print(find_marker(input_data, buffer_sz=14))

