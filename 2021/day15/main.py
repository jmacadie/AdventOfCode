from typing import List, NamedTuple, Dict

class Point(NamedTuple):
    x: int
    y: int

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
            if a.x != b.x or a.y != b.y:
                return False
        return True

    def __init__(self, file: str) -> None:
        self.width = 0
        self.height = 0
        self.map = [] # type: List[List[int]]
        self.start = Point(0, 0)
        self.min_paths = {self.start: [self.start]} # type: Dict[Point, List[Point]]
        self.read_file(file)
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

    def get_point_val(self, p: Point) -> int:
        return self.map[p.y][p.x]

    def in_bounds(self, p: Point) -> bool:
        if p.x < 0 or p.y < 0:
            return False
        if p.x >= self.width or p.y >= self.height:
            return False
        return True

    def get_adjacent_points(self, p: Point) -> List[Point]:
        x = p.x
        y = p.y
        points = []
        for new_point in [
            Point(x + 1, y),
            Point(x - 1, y),
            Point(x, y + 1),
            Point(x, y - 1)]:
            if self.in_bounds(new_point) and new_point in self.min_paths:
                points.append(new_point)
        return points

    def get_path_value(self, path: List[Point]) -> int:
        sum_tmp = 0
        for i in range(1, len(path)):
            sum_tmp += self.get_point_val(path[i])
        return sum_tmp

    def find_min_path_at(self, p: Point) -> List[Point]:
        if p.x == 0 and p.y == 0:
            return [Point(0, 0)]
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
        for depth in range(1, self.width):
            self.find_min_paths_at(depth)

    def get_min_path_val(self) -> int:
        path = self.min_paths[Point(self.width - 1, self.height - 1)]
        return self.get_path_value(path)

C = Cavern('test.txt')
assert C.get_min_path_val() == 40

C = Cavern('input.txt')
assert C.get_min_path_val() == 696
print(C.get_min_path_val())
