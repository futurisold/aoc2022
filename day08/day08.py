import numpy as np


def load_data(path: str):
    with open(path) as f:
        lines = np.array(list(map(int, ''.join([s.strip() for s in f.readlines()]))))
        lines = lines.reshape(int(len(lines)**.5), -1)

    return lines


def get_interior_pos(data: np.ndarray):
    mask = data.copy()
    mask[1:-1, 1: -1] = 1 # interior
    mask[0, :] = 0
    mask[-1, :] = 0
    mask[:, 0] = 0
    mask[:, -1] = 0

    return list(zip(*np.where(mask)))


def viewing_distance(tree: int, nbtrees: np.ndarray):
    dist = 0
    for nbtree in nbtrees:
        if nbtree < tree:
            dist += 1
            continue
        if nbtree >= tree:
            dist += 1
            return dist

    return dist


def count_trees(data: np.ndarray):
    interior_trees_pos = get_interior_pos(data)
    visible_trees = data.size - len(interior_trees_pos)
    for i, j in interior_trees_pos:
        tree = data[i, j]
        left = data[i, :j]
        right = data[i, j+1:]
        top = data[:i, j]
        bottom = data[i+1:, j]
        is_visible = max(left) < tree or max(right) < tree or max(top) < tree or max(bottom) < tree
        if is_visible: visible_trees += 1


    return visible_trees


def scenic_score(data: np.ndarray):
    scores = []
    interior_trees_pos = get_interior_pos(data)
    for i, j in interior_trees_pos:
        tree = data[i, j]
        left = data[i, :j][::-1]
        right = data[i, j+1:]
        top = data[:i, j][::-1]
        bottom = data[i+1:, j]
        scores.append(viewing_distance(tree, left) * viewing_distance(tree, right) * viewing_distance(tree, bottom) * viewing_distance(tree, top))

    return max(scores)

if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert count_trees(assert_data) == 21
    assert scenic_score(assert_data) == 8

    input_data = load_data('./input.txt')
    # part 1
    print(count_trees(input_data))
    # part 2
    print(scenic_score(input_data))

