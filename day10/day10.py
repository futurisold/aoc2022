def load_data(path: str):
    with open(path) as f:
        lines = [s.strip() for s in f.readlines()]

    return lines


def run_program(instructions: list[str], render: bool):
    ts=range(20, 260, 40)
    t = -1
    x = 1
    signal_strengths = 0
    pixel_idx = 0
    screen = [['?' for _ in range(40)] for _ in range(6)]

    for instruction in instructions:
        if instruction.startswith('noop'):
            t += 1
            screen[t//40][t%40] = ('#' if x-(t%40) in [-1, 0, 1] else ' ')
            if t in ts: signal_strengths += (t * x)

        elif instruction.startswith('addx'):
            t += 1
            screen[t//40][t%40] = ('#' if x-(t%40) in [-1, 0, 1] else ' ')
            if t in ts: signal_strengths += (t * x)
            t += 1
            screen[t//40][t%40] = ('#' if x-(t%40) in [-1, 0, 1] else ' ')
            if t in ts: signal_strengths += (t * x)
            x += int(instruction.split()[-1])

    if render:
        for i in range(6):
            print(''.join(screen[i]))

    return signal_strengths


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    run_program(assert_data, render=False) == 13140
    run_program(assert_data, render=True)

    input_data = load_data('./input.txt')
    # part 1
    print(run_program(input_data, render=False))
    # part 2
    print(run_program(input_data, render=True))

