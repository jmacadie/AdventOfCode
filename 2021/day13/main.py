from typing import List

class Origami:

    MAX = 2000

    def __init__(self, file: str) -> None:
        self.map = [[0 for _ in range(self.MAX)] for _ in range(self.MAX)]
        self.max_x = 0
        self.max_y = 0
        self.fold1_dots = 0
        self.read_file(file)

    def read_file(self, file_path: str) -> None:
        points = []
        folds = []
        points_section = True
        with open(file_path, encoding='UTF-8') as file:
            while line := file.readline():
                if line == '\n':
                    points_section = False
                elif points_section:
                    points.append(line.replace('\n', '').strip())
                else:
                    line = line.replace('\n', '').strip()
                    _, line = line.split('along ')
                    folds.append(line)
        self.add_points(points)
        self.do_folds(folds)

    def add_points(self, points: List[str]) -> None:
        for point in points:
            self.add_point(point)
        self.trim_map()

    def add_point(self, point: str) -> None:
        x, y = [int(i) for i in point.split(',')]
        self.map[y][x] = 1
        self.max_x = max(self.max_x, x + 1)
        self.max_y = max(self.max_y, y + 1)

    def trim_map(self) -> None:
        self.map = self.map[:self.max_y]
        for y in range(self.max_y):
            self.map[y] = self.map[y][:self.max_x]

    def do_folds(self, folds: List[str]) -> None:
        for fold in folds:
            self.do_fold(fold)
            if self.fold1_dots == 0:
                self.fold1_dots = self.count_dots()

    def do_fold(self, fold: str) -> None:
        dim, fold_at_str = fold.split('=')
        fold_at = int(fold_at_str)
        if dim == 'x':
            self.fold_x(fold_at)
        elif dim == 'y':
            self.fold_y(fold_at)
        self.trim_map()

    def fold_x(self, fold_at: int) -> None:
        lower = max(2 * fold_at - self.max_x + 1, 0)
        for x in range(lower, fold_at):
            for y in range(self.max_y):
                self.map[y][x] = min(self.map[y][x] + self.map[y][2 * fold_at - x], 1)
        self.max_x = fold_at

    def fold_y(self, fold_at: int) -> None:
        lower = max(2 * fold_at - self.max_y + 1, 0)
        for x in range(self.max_x):
            for y in range(lower, fold_at):
                self.map[y][x] = min(self.map[y][x] + self.map[2 * fold_at - y][x], 1)
        self.max_y = fold_at

    def count_dots(self) -> int:
        sum_dots = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
                sum_dots += self.map[y][x]
        return sum_dots

    def print_out(self) -> None:
        for y in range(self.max_y):
            line_out = ''
            for x in range(self.max_x):
                if self.map[y][x] == 0:
                    line_out += ' '
                else:
                    line_out += '#'
            print(line_out)

O = Origami('test.txt')
assert O.fold1_dots == 17

O = Origami('input.txt')
assert O.fold1_dots == 655
print(O.fold1_dots)
O.print_out()
