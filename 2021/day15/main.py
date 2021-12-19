import time
from typing import List, NamedTuple

class Point(NamedTuple):
    x: int
    y: int

    def get_adjacent(self, diag: bool=False) -> List['Point']:
        output = []
        output.append(Point(self.x + 1, self.y))
        output.append(Point(self.x - 1, self.y))
        output.append(Point(self.x, self.y + 1))
        output.append(Point(self.x, self.y - 1))
        if diag:
            output.append(Point(self.x + 1, self.y + 1))
            output.append(Point(self.x - 1, self.y + 1))
            output.append(Point(self.x + 1, self.y - 1))
            output.append(Point(self.x - 1, self.y - 1))
        return output

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Point):
            return NotImplemented
        return self.x == __o.x and self.y == __o.y

class Cavern:

    BIG = 1000000000

    @classmethod
    def get_depth_points(cls, depth: int) -> List[Point]:
        points = []
        for x in range(depth):
            points.append(Point(x, depth))
        for y in range(depth + 1):
            points.append(Point(depth, y))
        return points

    @classmethod
    def increment_map(cls, cavern_map: List[List[int]]) -> List[List[int]]:
        width = len(cavern_map[0])
        height = len(cavern_map)
        tmp = []
        for y in range(height):
            row  = []
            for x in range(width):
                val = cavern_map[y][x] + 1
                val = 1 if val == 10 else val
                row.append(val)
            tmp.append(row)
        return tmp

    def __init__(self, file: str, tile_times: int=0) -> None:
        self.width = 0
        self.height = 0
        self.map = [] # type: List[List[int]]
        self.start = Point(0, 0)
        self.read_file(file)
        self.tile_map(tile_times)
        self.min_cost_map = [] # type: List[List[int]]
        self.init_min_cost_map()
        self.calc_costs()

    def read_file(self, file_path: str) -> None:
        with open(file_path, encoding='UTF-8') as file:
            while line:= file.readline():
                line = line.replace('\n', '').strip()
                if self.width == 0:
                    self.width = len(line)
                row = [int(i) for i in line]
                assert len(row) == self.width
                self.height += 1
                self.map.append(row)

    def tile_map(self, times: int) -> None:
        working_copy = self.map.copy()
        inc_map = working_copy.copy()
        for _ in range(times):
            inc_map = self.increment_map(inc_map)
            working_copy = working_copy + inc_map
        inc_map = working_copy.copy()
        for _ in range(times):
            inc_map = self.increment_map(inc_map)
            tmp = []
            for row1, row2 in zip(working_copy, inc_map):
                tmp.append(row1 + row2)
            working_copy = tmp
        self.map = working_copy
        self.width *= (times + 1)
        self.height *= (times + 1)

    def init_min_cost_map(self) -> None:
        self.min_cost_map = [[self.BIG for _ in range(self.width)] for _ in range(self.height)]

    def get_point_val(self, p: Point) -> int:
        return self.map[p.y][p.x]

    def get_point_min_cost(self, p: Point) -> int:
        return self.min_cost_map[p.y][p.x]

    def set_point_min_cost(self, p: Point, val: int) -> None:
        self.min_cost_map[p.y][p.x] = val

    def in_bounds(self, p: Point) -> bool:
        if p.x < 0 or p.y < 0:
            return False
        if p.x >= self.width or p.y >= self.height:
            return False
        return True

    def get_adjacent_points(self, p: Point) -> List[Point]:
        points = []
        for new_point in p.get_adjacent():
            if self.in_bounds(new_point):
                points.append(new_point)
        return points

    def calc_costs(self) -> None:
        for lim in range(self.width):
            for p in self.get_depth_points(lim):
                if lim == 0:
                    val = 0
                elif p.x == lim:
                    val = self.get_point_min_cost(Point(p.x - 1, p.y)) + self.get_point_val(p)
                else:
                    val = self.get_point_min_cost(Point(p.x, p.y - 1)) + self.get_point_val(p)
                self.update_cost(p, val)

    def update_cost(self, p: Point, val: int) -> None:
        for new_point in self.get_adjacent_points(p):
            val = min(val, self.get_point_min_cost(new_point) + self.get_point_val(p))
        self.set_point_min_cost(p, val)
        for new_point in self.get_adjacent_points(p):
            if self.get_point_min_cost(new_point) < self.BIG:
                new_val = val + self.get_point_val(new_point)
                if self.get_point_min_cost(new_point) > new_val:
                    self.update_cost(new_point, new_val)

    def get_min_path_val(self) -> int:
        return self.get_point_min_cost(Point(self.width - 1, self.height - 1))

start = time.time()

C = Cavern('test.txt')
assert C.get_min_path_val() == 40
C = Cavern('test.txt', 4)
assert C.get_min_path_val() == 315

C = Cavern('input.txt')
assert C.get_min_path_val() == 696
print(C.get_min_path_val())
C = Cavern('input.txt', 4)
assert C.get_min_path_val() == 2952
print(C.get_min_path_val())

print(f'--- {round(time.time() - start, 2)} seconds ---')
