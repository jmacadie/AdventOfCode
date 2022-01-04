from typing import NamedTuple, Dict
from itertools import cycle

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: object) -> 'Point':
        if not isinstance(other, Point):
            return NotImplemented
        return Point(
            self.x + other.x,
            self.y + other.y
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def move(self, direction: str) -> 'Point':
        if direction == '>':
            return Point(self.x + 1, self.y)
        if direction == '^':
            return Point(self.x, self.y + 1)
        if direction == '<':
            return Point(self.x - 1, self.y)
        if direction == 'v':
            return Point(self.x, self.y - 1)
        return Point(self.x, self.y)

class SantaNetwork:

    def __init__(self, path: str, part1: bool) -> None:
        self.visited = {} # type: Dict[Point, int]
        self.path = path
        self.run_deliveries(part1)

    def run_deliveries(self, part1: bool) -> None:
        santa = Point(0, 0)
        robot = Point(0, 0)
        self.visited[santa] = 1
        visit_type = ['s'] if part1 else ['s', 'r']
        path = zip(list(self.path), cycle(visit_type))
        for char, visitor in path:
            if visitor == 's':
                santa = self.move_and_add(santa, char)
            else:
                robot = self.move_and_add(robot, char)

    def move_and_add(self, p: Point, direction: str) -> Point:
        output = p.move(direction)
        self.add_point(output)
        return output

    def add_point(self, p: Point) -> None:
        if p in self.visited:
            self.visited[p] += 1
        else:
            self.visited[p] = 1

    def get_stops(self) -> int:
        return len(self.visited)

    def get_multi_stops(self) -> int:
        multi = [p for p, v in self.visited.items() if v > 1]
        return len(multi)

with open('input.txt', encoding='UTF-8') as file:
    line = file.readline()
line = line.replace('\n', '').strip()
SN = SantaNetwork(line, True)
print(SN.get_stops())
SN = SantaNetwork(line, False)
print(SN.get_stops())
