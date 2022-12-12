import re


def load_data(path: str):
    with open(path) as f:
        lines = [s.strip().replace(' ', '') for s in f.readlines()]

    return lines


def get_stacks(crane: list[str]):
    stacks = [[]]
    i = 0
    cur = crane[i]
    while cur:
        stacks.append(list(cur))
        i += 1
        cur = crane[i]

    return stacks


def get_moves(crane: list[str]):
    i = 0
    cur = crane[i]
    while cur:
        i += 1
        cur = crane[i]

    i += 1
    moves = []
    for move in crane[i:]:
        moves.append([int(n) for n in re.findall(r'\d+', move)])

    return moves


def rearrangement_procedure(crane: list[str], cm9001: bool):
    stacks = get_stacks(crane)
    moves = get_moves(crane)

    for move in moves:
        mv, fr, to = move
        stacks[to] = stacks[fr][:mv][::-1] + stacks[to] if not cm9001 else stacks[fr][:mv] + stacks[to]
        del stacks[fr][:mv]

    return ''.join(crates[0] for crates in stacks[1:])


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert rearrangement_procedure(assert_data, cm9001=False) == 'CMZ'
    assert rearrangement_procedure(assert_data, cm9001=True) == 'MCD'

    input_data = load_data('./input.txt')
    # part 1
    print(rearrangement_procedure(input_data, cm9001=False))
    # part 2
    print(rearrangement_procedure(input_data, cm9001=True))

