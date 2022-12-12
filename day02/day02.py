SHAPE = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

GUESS_STRATEGY = {
    ('A', 'X'): 3,
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('C', 'Y'): 0,
    ('C', 'Z'): 3,
}

ACTUAL_STRATEGY = {
    ('A', 'X'): 0 + SHAPE['Z'],
    ('A', 'Y'): 3 + SHAPE['X'],
    ('A', 'Z'): 6 + SHAPE['Y'],
    ('B', 'X'): 0 + SHAPE['X'],
    ('B', 'Y'): 3 + SHAPE['Y'],
    ('B', 'Z'): 6 + SHAPE['Z'],
    ('C', 'X'): 0 + SHAPE['Y'],
    ('C', 'Y'): 3 + SHAPE['Z'],
    ('C', 'Z'): 6 + SHAPE['X'],
}


def load_data(path: str):
    with open(path, 'r') as f:
        lines = [tuple(s.strip().replace(' ', ''))
                 for s in f.readlines()]

    return lines


def strategy_guide(rounds: list[str], guess: bool):
    total = 0
    for round in rounds:
        _, me = round
        if guess: total += GUESS_STRATEGY[round] + SHAPE[me]
        else: total += ACTUAL_STRATEGY[round]

    return total


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert strategy_guide(assert_data, guess=True) == 15
    assert strategy_guide(assert_data, guess=False) == 12

    input_data = load_data('./input.txt')
    # part 1
    print(strategy_guide(input_data, guess=True))
    # part 2
    print(strategy_guide(input_data, guess=False))
