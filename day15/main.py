import re
from dataclasses import dataclass
import tqdm


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

    def __sub__(self, other): return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other): return self.x == other.x and self.y == other.y


@dataclass
class Line:
    head: Point
    tail: Point

    def range(self): return range(self.head.x, self.tail.x + 1)


def coverage(sensor: Point, dist: int, row: int):
    if not ((sensor.y - dist) <= row <= (sensor.y + dist)): return
    for i in range(dist):
        if (sensor.y + i) == row:
            head = Point(sensor.x - dist + i, sensor.y + i)
            tail = Point(sensor.x + dist - i, sensor.y + i)
            return Line(head, tail)
        elif (sensor.y - i) == row:
            head = Point(sensor.x - dist + i, sensor.y - i)
            tail = Point(sensor.x + dist - i, sensor.y - i)
            return Line(head, tail)
        else: continue


def consult_report(data: list[list[int]], row: int):
    locs = set()
    for dp in data:
        sensor = Point(*dp[:2])
        beacon = Point(*dp[2:])
        dist = sensor - beacon
        cov = coverage(sensor, dist, row)
        if cov is not None: locs.update(cov.range())
        if beacon.y == row: locs -= {beacon.x}
    print(locs)
    return len(locs)


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert consult_report(assert_data, row=10) == 26

    input_data = load_data('./input.txt')
    # part 1
    # print(consult_report(input_data, row=2000000))
    # part 2

