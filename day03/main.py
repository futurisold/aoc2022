def load_data(path: str):
    with open(path) as f:
        lines = [s.strip() for s in f.readlines()]

    return lines


def prioritize(char: str): return ord(char) - 96 if char.islower() else ord(char) - 38


def split_into_compartments(rucksack: str):
    mid = len(rucksack) // 2
    comp1, comp2 = rucksack[:mid], rucksack[mid:]

    return (set(comp1), set(comp2))


def common_item_in_rucksack(rucksack: str):
    comp1, comp2 = split_into_compartments(rucksack)
    common = comp1.intersection(comp2).pop()

    return prioritize(common)


def common_item_in_rucksacks(rucksacks: list[str]):
    ruck1, ruck2, ruck3 = list(map(set, rucksacks))
    common = ruck1.intersection(ruck2).intersection(ruck3).pop()

    return prioritize(common)


def total_score(rucksacks: list[str], safety: bool):
    if safety:
        total, i, j = 0, 0, 1
        while (j*3) <= len(rucksacks):
            group = rucksacks[i*3: j*3]
            total += common_item_in_rucksacks(group)
            i += 1
            j += 1

        return total

    else: return sum(map(common_item_in_rucksack, rucksacks))


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert total_score(assert_data, safety=False) == 157
    assert total_score(assert_data, safety=True) == 70

    input_data = load_data('./input.txt')
    # part 1
    print(total_score(input_data, safety=False))
    # part 2
    print(total_score(input_data, safety=True))

