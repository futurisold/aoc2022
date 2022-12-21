import re
from dataclasses import dataclass
from itertools import combinations
from shapely.geometry import Polygon


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

    @property
    def tuple(self): return (self.x, self.y)

    def __sub__(self, other): return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other): return self.x == other.x and self.y == other.y


@dataclass
class Line:
    head: Point
    tail: Point

    def __post_init__(self):
        self.xmin = min(self.head.x, self.tail.x)
        self.ymin = min(self.head.y, self.tail.y)
        self.xmax = max(self.head.x, self.tail.x) + 1
        self.ymax = max(self.head.y, self.tail.y) + 1

    @property
    def xrange(self): return range(self.xmin, self.xmax)

    @property
    def yrange(self): return range(self.ymin, self.ymax)


def coverage_at_row(sensor: Point, dist: int, row: int):
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
        coverage = coverage_at_row(sensor, dist, row)
        if coverage is not None: locs.update(coverage.xrange)
        if beacon.y == row: locs -= {(beacon.x)}

    return locs


def coverage_as_poly(sensor: Point, dist: int):
    return Polygon([
            (sensor.x, sensor.y + dist + 1),
            (sensor.x - dist - 1, sensor.y),
            (sensor.x, sensor.y - dist - 1),
            (sensor.x + dist + 1, sensor.y),
        ]
    )


def search(data: list[list[int]]):
    data = map(lambda dp: (Point(*dp[:2]), Point(*dp[2:])), data)

    sensors, coverage = [], []
    for sensor, beacon in data:
        dist = sensor - beacon
        sensors.append((sensor, dist))
        coverage.append(coverage_as_poly(sensor, dist))

    for p1, p2, p3, p4 in combinations(coverage, 4):
        hull = (p1.intersection(p2).intersection(p3.intersection(p4))).convex_hull
        if hull.geom_type == 'Point':
            p = Point(hull.x, hull.y)
            if all([0 < p.x < 4e6, 0 < p.y < 4e6]):
                if all([p - sensor > dist for sensor, dist in sensors]):
                    return int(p.x * 4e6 + p.y)


if __name__ == '__main__':
    assert_data = load_data('./assert.txt')
    assert len(consult_report(assert_data, row=10)) == 26
    assert search(assert_data) == 56000011

    input_data = load_data('./input.txt')
    # part 1
    print(len(consult_report(input_data, row=2000000)))
    # part 2
    print(search(input_data))

