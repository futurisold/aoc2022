def load_data(path: str):
    [*lines] = open(path)

    return [s.strip('\n') for s in lines]


def decode_snafu(n: str) -> int:
    sn = 0
    for i, d in enumerate(n[::-1]):
        match d:
            case '2': sn += (2 * 5 ** i)
            case '1': sn += (1 * 5 ** i)
            case '0': sn += (0 * 5 ** i)
            case '-': sn += (-1 * 5 ** i)
            case '=': sn += (-2 * 5 ** i)

    return sn


def encode_snafu(n: int) -> str:
    sn = ''
    while True:
        div, mod = divmod(n+2, 5)
        n = div
        match mod:
            case 0: sn += '='
            case 1: sn += '-'
            case 2: sn += '0'
            case 3: sn += '1'
            case 4: sn += '2'
        if div == 0: return sn[::-1]


def console_input(data: list[str]) -> int:
    return encode_snafu(sum(decode_snafu(n) for n in data))


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert console_input(assert_data) == '2=-1=0'

    input_data = load_data('./input.txt')
    # part 1
    print(console_input(input_data))
    # part 2
