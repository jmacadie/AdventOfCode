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

class Trajectory:

    MIN_X = 117
    MAX_X = 164
    MIN_Y = -140
    MAX_Y = -89

    def __init__(self, init_speed: Point) -> None:
        self.speed = init_speed
        self.position = Point(0, 0)
        self.max_height = 0
        self.valid = self.hits_target()

    def step_speed(self) -> None:
        self.speed = Point(
            max(self.speed.x - 1, 0),
            self.speed.y - 1)

    def step(self) -> None:
        self.position = self.position + self.speed
        self.max_height = max(self.max_height, self.position.y)
        self.step_speed()

    def in_target(self) -> bool:
        return (
            self.position.x >= self.MIN_X and
            self.position.x <= self.MAX_X and
            self.position.y >= self.MIN_Y and
            self.position.y <= self.MAX_Y
        )

    def undershot(self) -> bool:
        return (
            self.position.x < self.MIN_X and
            self.speed.x == 0
        )

    def overshot(self) -> bool:
        return (
            self.position.x > self.MAX_X or
            self.position.y < self.MIN_Y
        )

    def hits_target(self) -> bool:
        while True:
            if self.in_target():
                return True
            if self.undershot() or self.overshot():
                return False
            self.step()

out = 0
max_y = 0
for x in range(170):
    for y in range(-150, 150):
        T = Trajectory(Point(x, y))
        if T.valid:
            out += 1
            max_y = max(max_y, T.max_height)
assert max_y == 9730
print(max_y)
assert out == 4110
print(out)
