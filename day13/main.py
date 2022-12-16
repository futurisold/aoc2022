from functools import cmp_to_key


def load_data(path: str):
    with open(path) as f:
        lines = list(map(eval, [s.strip() for s in f.readlines() if s.strip()]))

    return list(zip(lines[::2], lines[1::2]))


def compare(left: list | int, right: list | int):
    if isinstance(left, int) and isinstance(right, int):
        if left < right: return 1
        elif left == right: return 0
        else: return -1
    if isinstance(left, list) and isinstance(right, list):
        i = 0
        while i < len(left) and i < len(right):
            res = compare(left[i], right[i])
            if res == -1: return -1
            if res == 1: return 1
            i += 1
        if i == len(left) and i < len(right): return 1
        elif i < len(left) and i == len(right): return -1
        else: return 0
    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    else: return 0


def decode_signal(data: list[tuple[list, list]], decoder_key: bool):
    decoded_packets = []
    raw_packets = []
    for packet in data:
        left, right = packet
        decoded_packets.append(compare(left, right))
        raw_packets.extend([left, right])

    if decoder_key:
        raw_packets.extend([[[2]], [[6]]])
        ordered_packets = sorted(raw_packets, key=cmp_to_key(lambda left, right: compare(left, right)), reverse=True)
        total = 1
        for i, packet in enumerate(ordered_packets, start=1):
            if packet == [[2]] or packet == [[6]]: total *= i

        return total

    else:
        total = 0
        for i, packet in enumerate(decoded_packets, start=1):
            if packet == 1: total += i

        return total


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert decode_signal(assert_data, decoder_key=False) == 13
    assert decode_signal(assert_data, decoder_key=True) == 140

    input_data = load_data('./input.txt')
    # part 1
    print(decode_signal(input_data, decoder_key=False))
    # part 2
    print(decode_signal(input_data, decoder_key=True))

