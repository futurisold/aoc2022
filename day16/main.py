import re
from collections import defaultdict
from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx


Scan = list[tuple[list[str], int]]


def load_data(path: str):
    vpat = r'([A-Z]{2})'
    fpat = r'\d+'
    with open(path) as f:
        lines = [l.strip() for l in f.readlines()]
        valves = map(lambda x: re.findall(vpat, x), lines)
        flows = map(lambda x: int(re.findall(fpat, x).pop()), lines)

    return list(zip(valves, flows))


def get_paths(scan: Scan, time: int, draw: bool):
    g = nx.Graph()
    for valves, rate in scan:
        v, tunnels = valves[0], valves[1:]
        g.add_node(v, rate=rate)
        for t in tunnels:
            g.add_edge(v, t)

    def _utility(valves, v_cur='AA', t=time, util={}):
        for v_nx in valves:
            t_nx = t - dists[v_cur][v_nx] - 1
            if t_nx < 1: continue
            yield from _utility(valves - {v_nx}, v_nx, t_nx, util | {v_nx: t_nx * g.nodes[v_nx]['rate']})
        yield util

    dists = nx.floyd_warshall(g)
    valves = set(filter(lambda x: g.nodes[x]['rate'], g.nodes))

    if draw:
        nx.draw(g, with_labels=True)
        plt.show()
    else: return _utility(valves)


def get_max_utility(scan: Scan, time: int, help: bool, draw: bool = False):
    if help:
        utilities = defaultdict(int)
        for path in get_paths(scan, time, draw):
            util = sum(path.values())
            key = frozenset(path.keys())
            if util > utilities[key]: utilities[key] = util

        return int(max(u1 + u2
                       for (p1, u1), (p2, u2) in combinations(utilities.items(), 2)
                       if not p1 & p2))

    return int(max(sum(path.values())
                   for path in get_paths(scan, time, draw)))


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert get_max_utility(assert_data, time=30, help=False) == 1651
    assert get_max_utility(assert_data, time=26, help=True) == 1707

    input_data = load_data('./input.txt')
    # part 1
    print(get_max_utility(input_data, time=30, help=False))
    # part 2
    print(get_max_utility(input_data, time=26, help=True))

