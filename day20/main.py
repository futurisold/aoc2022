from collections import deque


def load_data(path: str):
    with open(path) as f:
        lines = [int(x) for x in f.readlines()]

    return lines


def decrypt_file(file: list[int], key: int | None, niter: int):
    file = [x * key for x in file] if key is not None else file
    file = deque(enumerate(file))

    for _ in range(niter):
        for i in range(len(file)):
            for j in range(len(file)):
                if file[j][0] == i: break # when j == i, we have the index

            while file[0][0] != i: file.rotate(-1) # left shift until we reach the index

            val = file.popleft()
            rng = val[1] % len(file) # get a range based on the value
            file.rotate(-rng)        # left shift the deque to the left
            file.append(val)

    for j in range(len(file)):
        if file[j][1] == 0: break

    return sum(file[(j+c)%len(file)][1] for c in [1000, 2000, 3000])


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert decrypt_file(assert_data, key=None, niter=1) == 3
    assert decrypt_file(assert_data, key=811589153, niter=10) == 1623178306

    input_data = load_data('./input.txt')
    # part 1
    print(decrypt_file(input_data, key=None, niter=1))
    # part 2
    print(decrypt_file(input_data, key=811589153, niter=10))

