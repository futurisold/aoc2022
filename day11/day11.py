from collections import defaultdict
from math import prod


def load_data(path: str):
    with open(path) as f:
        lines = [s.strip() for s in f.readlines()]

    monkeys = []
    i = 0
    while len(lines):
        while i < len(lines) and lines[i]:
            i += 1
        monkeys.append(lines[:i])
        del lines[:i+1]
        i = 0

    return monkeys


def take_notes(monkeys: list[str]):
    notes = defaultdict(dict)
    for i, monkey in enumerate(monkeys):
        items = list(map(int, monkey[1].split(':')[-1].split(',')))
        notes[i]['items'] = items
        op = monkey[2].split('=')[-1][1:]
        notes[i]['op'] = op
        div = int(monkey[3].split(' ')[-1])
        notes[i]['div'] = div
        true = int(monkey[4].split(' ')[-1])
        false = int(monkey[5].split(' ')[-1])
        notes[i]['true'] = true
        notes[i]['false'] = false

    return notes


def keep_away(monkeys: list[str], rounds: int):
    notes = take_notes(monkeys)
    round = 0

    # keep track of lcm instead of other bigger numbers
    lcm = 1
    for div in map(lambda k: notes[k]['div'], notes.keys()):
        lcm *= (lcm*div)

    while round < rounds:
        for i in range(max(notes.keys())+1):
            while len(notes[i]['items']):
                old = notes[i]['items'][0]
                new = eval(f'{notes[i]["op"]}')
                if rounds == 20: new //= 3
                else: new %= lcm
                if not (new % notes[i]['div']): notes[notes[i]['true']]['items'].append(new)
                elif (new % notes[i]['div']): notes[notes[i]['false']]['items'].append(new)
                if notes[i].get('activity') is None: notes[i]['activity'] = 1
                else: notes[i]['activity'] += 1
                del notes[i]['items'][0]
        round += 1

    return prod(sorted(map(lambda k: notes[k]['activity'], notes.keys()))[-2:])


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert keep_away(assert_data, rounds=20) == 10605
    assert keep_away(assert_data, rounds=10000) == 2713310158

    input_data = load_data('./input.txt')
    # part 1
    print(keep_away(input_data, rounds=20))
    # part 2
    print(keep_away(input_data, rounds=10000))

