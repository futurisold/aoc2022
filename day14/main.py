def load_data(path: str):
    with open(path) as f:
        lines = [s.strip().split(' -> ') for s in f.readlines()]

    return lines


def simulation(data: list[list[str]], floor: bool):
    # render scan
    rightlb = min(map(lambda x: min([int(p.split(',')[0]) for p in x]), data))
    rightrb = max(map(lambda x: max([int(p.split(',')[0]) for p in x]), data))
    downtb = min(map(lambda x: min([int(p.split(',')[1]) for p in x]), data))
    downbb = max(map(lambda x: max([int(p.split(',')[1]) for p in x]), data))
    rightm = {x: i for i, x in enumerate(range(rightlb, rightrb+1))}
    downm = {x: x for x in range(downbb+1) if x >= downtb}
    if floor:
        # make a floor big enough
        scan = [['.' for _ in range(len(rightm))]*10 for _ in range(len(downm)+downtb+2)]
        scan[-1] = ['#' for _ in scan[-1]]
        # try to center the source
        rightm[500] = len(rightm)*10 // 2
        for k in rightm:
            if k != 500:
                off = 500 - k
                if off > 0: rightm[k] = rightm[500] - off
                else: rightm[k] = rightm[500] + (-off)
    else:
        scan = [['.' for _ in range(len(rightm))] for _ in range(len(downm)+downtb)]
    src = (0, rightm[500])
    scan[src[0]][src[1]] = '+'

    for rock_path in data:
        i = 0
        while i+2 <= len(rock_path):
            a, b = rock_path[i:i+2]
            awhole, afrac = a.split(',')
            bwhole, bfrac = b.split(',')
            if awhole == bwhole:
                mn = min(downm[int(afrac)], downm[int(bfrac)])
                mx = max(downm[int(afrac)], downm[int(bfrac)]) + 1
                for x in range(mn, mx):
                    scan[x][rightm[int(awhole)]] = '#'
            elif afrac == bfrac:
                mn = min(rightm[int(awhole)], rightm[int(bwhole)])
                mx = max(rightm[int(awhole)], rightm[int(bwhole)]) + 1
                for x in range(mn, mx):
                    scan[downm[int(afrac)]][x] = '#'
            i += 1

    # render sand
    def neighbourhood(p: tuple[int, int], grid: list[list[str]]):
        i, j = p
        while i+1 < len(grid) and j+1 < len(grid[0]):
            if grid[i+1][j] == 'o' or grid[i+1][j] == '#':
                if grid[i+1][j-1] == 'o' or grid[i+1][j-1] == '#':
                    if grid[i+1][j+1] == 'o' or grid[i+1][j+1] == '#':
                        grid[i][j] = 'o'
                        return (i, j)
                    else:
                        return neighbourhood((i+1, j+1), grid)
                else:
                    return neighbourhood((i+1, j-1), grid)
            else:
                return neighbourhood((i+1, j), grid)

    i = 0 if floor else 1
    rest = False
    cells = set()
    while not rest:
        cell = neighbourhood((src[0]+i, src[1]), scan)
        if cell in cells or cell is None or cell == -1: rest = True
        else: cells.add(cell)

    if not floor:
        for row in scan: print(''.join(row))

    return len(cells)


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert simulation(assert_data, floor=False) == 24
    assert simulation(assert_data, floor=True) == 93

    input_data = load_data('./input.txt')
    # part 1
    print(simulation(input_data, floor=False))
    # part 2
    print(simulation(input_data, floor=True))

