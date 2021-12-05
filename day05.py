from collections import defaultdict
from dataclasses import dataclass

from base import BaseSolution


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def parse(cls, input_str):
        return cls(*(int(value) for value in input_str.split(",")))


@dataclass(frozen=True)
class LineSegment:
    p1: Point
    p2: Point

    @classmethod
    def parse(cls, input_str):
        return cls(*(Point.parse(point_str) for point_str in input_str.split(" -> ")))

    @property
    def is_diagonal(self):
        return self.p1.x != self.p2.x and self.p1.y != self.p2.y

    def __iter__(self):
        dx = self.p2.x - self.p1.x
        x_step = dx / abs(dx) if dx else 0
        dy = self.p2.y - self.p1.y
        y_step = dy / abs(dy) if dy else 0
        point = self.p1
        while point != self.p2:
            yield point
            point = Point(x=point.x + x_step, y=point.y + y_step)
        yield self.p2


class Solution(BaseSolution):
    def load_data(self, input):
        return [LineSegment.parse(line) for line in input.splitlines()]

    def part1(self, data):
        return self.count_overlaps(
            segment for segment in data if not segment.is_diagonal
        )

    def part2(self, data):
        return self.count_overlaps(data)

    def count_overlaps(self, data):
        covered = defaultdict(int)
        for segment in data:
            for point in segment:
                covered[point] += 1
        return sum(value > 1 for value in covered.values())
