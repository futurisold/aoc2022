import re
from itertools import permutations
import networkx as nx
import matplotlib.pyplot as plt


Scan = list[tuple[list[str], int]]


def load_data(path: str):
    vpat = r'([A-Z]{2})'
    fpat = r'\d+'
    with open(path) as f:
        lines = [l.strip() for l in f.readlines()]
        valves = map(lambda x: re.findall(vpat, x), lines)
        flows = map(lambda x: int(re.findall(fpat, x).pop()), lines)

    return list(zip(valves, flows))



def max_utility_path(scan: Scan):
    g = nx.Graph()
    for valves, rate in scan:
        v, tunnels = valves[0], valves[1:]
        g.add_node(v, rate=rate)
        for t in tunnels:
            g.add_edge(v, t)

    def _utility(path: tuple[str]):
        t = 30
        util = 0
        if path[0] != 'AA': return 0
        for curv, nxv in zip(path[:-1], path[1:]):
            t -= (dists[curv][nxv] + 1)
            if t < 2: break
            util += (g.nodes[nxv]['rate'] * t)
        return util

    dists = nx.floyd_warshall(g)
    valves = set(filter(lambda x: g.nodes[x]['rate'], g.nodes)) | {'AA'}
    # print(max(map(_utility, filter(lambda x: x[0] == 'AA', permutations(valves, len(valves))))))
    print(max(map(_utility, permutations(valves, len(valves)))))
    # print(len(list(paths)))
    # print(max(map(_utility, paths)))

    # nx.draw(g, with_labels=True)
    # plt.show()


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    max_utility_path(assert_data)

    input_data = load_data('./input.txt')
    # part 1
    max_utility_path(input_data)
    # part 2

