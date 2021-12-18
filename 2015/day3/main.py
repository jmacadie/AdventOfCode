from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

    def __add__ (self, other: object) -> 'Point':
        if not isinstance(other, Point):
            return NotImplemented
        return Point(
            self.x + other.x,
            self.y + other.y
        )

    def move(self, direction) -> 'Point':
        if direction == '>':
            return Point(self.x + 1, self.y)
        if direction == '^':
            return Point(self.x, self.y + 1)
        if direction == '<':
            return Point(self.x - 1, self.y)
        if direction == 'V':
            return Point(self.x, self.y - 1)
        return Point(self.x, self.y)

def append_or_add(d: dict)

with open('input.txt', encoding='UTF-8') as file:
    line = file.readline()
line = line.replace('\n', '').strip()
visited = {} # type: dict[Point, int]
P = Point(0, 0)

