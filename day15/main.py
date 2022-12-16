import re
from dataclasses import dataclass


def load_data(path: str):
    with open(path) as f:
        pattern  = r'[-]?\b\d+\b'
        lines = [[int(i) for i in re.findall(pattern, s.strip())]
                 for s in f.readlines()]

    return lines


@dataclass
class Point:
    x: int
    y: int

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


def consult_report(data: list[list[int]]):
    for dp in data:
        sensor = Point(*dp[:2])
        beacon = Point(*dp[2:])
        dist = sensor - beacon


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    consult_report(assert_data)

    # input_data = load_data('./input.txt')
    # part 1
    # part 2

