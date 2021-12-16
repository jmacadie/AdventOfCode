import time
from typing import List, NamedTuple, Dict

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

    @classmethod
    def get_depth_points(cls, depth: int) -> List[Point]:
        points = []
        for x in range(depth + 1):
            points.append(Point(x, depth))
        for y in range(depth):
            points.append(Point(depth, y))
        return points

    @classmethod
    def same_path(cls, path1: List[Point], path2: List[Point]) -> bool:
        if len(path1) != len(path2):
            return False
        for a, b in zip(path1, path2):
            if a != b:
                return False
        return True

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
        self.min_paths = {} # type: Dict[Point, List[Point]]
        self.read_file(file)
        self.tile_map(tile_times)
        self.find_min_paths()

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

    def get_point_val(self, p: Point) -> int:
        return self.map[p.y][p.x]

    def in_bounds(self, p: Point) -> bool:
        if p.x < 0 or p.y < 0:
            return False
        if p.x >= self.width or p.y >= self.height:
            return False
        return True

    def get_adjacent_points(self, p: Point) -> List[Point]:
        points = []
        for new_point in p.get_adjacent():
            if self.in_bounds(new_point) and new_point in self.min_paths:
                points.append(new_point)
        return points

    def get_path_value(self, path: List[Point]) -> int:
        sum_tmp = 0
        for i in range(1, len(path)):
            sum_tmp += self.get_point_val(path[i])
        return sum_tmp

    def find_min_path_at(self, p: Point) -> List[Point]:
        if p == self.start:
            return [self.start]
        min_path_val = 0
        for next_p in self.get_adjacent_points(p):
            path = self.min_paths[next_p].copy()
            path.append(p)
            val = self.get_path_value(path)
            if min_path_val == 0 or val < min_path_val:
                min_path_val = val
                min_path = path
        return min_path

    def check_adjacent(self, p: Point) -> None:
        for next_p in self.get_adjacent_points(p):
            new_min = self.find_min_path_at(next_p)
            if not self.same_path(new_min, self.min_paths[next_p]):
                self.min_paths[next_p] = new_min
                self.check_adjacent(next_p)

    def find_min_paths_at(self, depth: int) -> None:
        for p in self.get_depth_points(depth):
            self.min_paths[p] = self.find_min_path_at(p)
            self.check_adjacent(p)

    def find_min_paths(self) -> None:
        for depth in range(self.width):
            self.find_min_paths_at(depth)

    def get_min_path_val(self) -> int:
        path = self.min_paths[Point(self.width - 1, self.height - 1)]
        return self.get_path_value(path)

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