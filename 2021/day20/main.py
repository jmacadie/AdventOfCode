from typing import List

class MapFactory:

    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def get_map(self) -> 'Map':
        start = True
        lines = []
        with open(self.file_path, encoding='UTF-8') as file:
            while line := file.readline():
                line = line.replace('\n', ''). strip()
                if not line:
                    start = False
                elif start:
                    algo = self.convert_line(line)
                else:
                    lines.append(self.convert_line(line))
        return Map(algo, lines)

    def convert_line(self, line: str) -> List[bool]:
        output = []
        for char in line:
            if char == '#':
                output.append(True)
            elif char == '.':
                output.append(False)
        return output

class Map:

    def __init__(self, enhancement_algorithm: List[bool], lines: List[List[bool]]) -> None:
        self.algo = enhancement_algorithm
        self.map = lines
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.boundary_point = False

    def in_bounds(self, x, y) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        return True

    def read_at_point(self, x, y) -> bool:
        if self.in_bounds(x, y):
            return self.map[y][x]
        return self.boundary_point

    def binary_at(self, x, y) -> int:
        binary = ''
        for y_diff in range(-1, 2):
            for x_diff in range (-1, 2):
                if self.read_at_point(x + x_diff, y + y_diff):
                    binary += '1'
                else:
                    binary += '0'
        return int(binary, 2)

    def enhance_point(self, x, y) -> bool:
        index = self.binary_at(x, y)
        return self.algo[index]

    def pad_map(self) -> None:
        self.width += 2
        self.height += 2
        top = [self.boundary_point for _ in range(self.width)]
        bottom = top.copy()
        output = [top]
        for line in self.map:
            line = [self.boundary_point] + line + [self.boundary_point]
            output.append(line)
        output.append(bottom)
        self.map = output

    def enhance(self) -> None:
        self.pad_map()
        output = []
        for y in range(self.width):
            line = []
            for x in range(self.height):
                line.append(self.enhance_point(x, y))
            output.append(line)
        self.map = output
        self.update_boundary_point()

    def update_boundary_point(self) -> None:
        if self.boundary_point and not self.algo[-1]:
            self.boundary_point = False
        elif not self.boundary_point and self.algo[0]:
            self.boundary_point = True

    def print(self) -> None:
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                if self.map[y][x]:
                    line += '#'
                else:
                    line += '.'
            print(line)

    def count_lights(self) -> int:
        output = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x]:
                    output += 1
        return output

M = MapFactory('test.txt').get_map()
for _ in range(2):
    M.enhance()
assert M.count_lights() == 35
for _ in range(48):
    M.enhance()
assert M.count_lights() == 3351

M = MapFactory('input.txt').get_map()
for _ in range(2):
    M.enhance()
assert M.count_lights() == 4968
print(M.count_lights())
for _ in range(48):
    M.enhance()
assert M.count_lights() == 16793
print(M.count_lights())
