from typing import List, Tuple, Optional

class Cube:

    def __init__(
        self,
        x_range: Tuple[int, int],
        y_range: Tuple[int, int],
        z_range: Tuple[int, int]
        ) -> None:
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.size = self.get_size()

    def intersection(self, other: 'Cube') -> Optional['Cube']:
        if self.out_of_range(self.x_range, other.x_range):
            return None
        if self.out_of_range(self.y_range, other.y_range):
            return None
        if self.out_of_range(self.z_range, other.z_range):
            return None
        x_range = (max(self.x_range[0], other.x_range[0]),
                min(self.x_range[1], other.x_range[1]))
        y_range = (max(self.y_range[0], other.y_range[0]),
                min(self.y_range[1], other.y_range[1]))
        z_range = (max(self.z_range[0], other.z_range[0]),
                min(self.z_range[1], other.z_range[1]))
        return Cube(x_range, y_range, z_range)

    @staticmethod
    def out_of_range(range1: Tuple[int, int], range2:Tuple[int,int]) -> bool:
        if range1[1] < range2[0]:
            return True
        if range1[0] > range2[1]:
            return True
        return False

    def get_size(self) -> int:
        x_dim = self.x_range[1] - self.x_range[0] + 1
        y_dim = self.y_range[1] - self.y_range[0] + 1
        z_dim = self.z_range[1] - self.z_range[0] + 1
        return x_dim * y_dim * z_dim

class Reactor:

    def __init__(self, file_path: str, range_limit: int=0) -> None:
        self.limit = range_limit
        self.add_cubes = [] # type: List[Cube]
        self.sub_cubes = [] # type: List[Cube]
        self.process_file(file_path)

    def process_file(self, file_path: str) -> None:
        with open(file_path, encoding='UTF-8') as file:
            while line := file.readline():
                line = line.replace('\n', '').strip()
                val_str, coords = line.split(' ')
                val = (val_str == 'on')
                new = self.get_cube(coords)
                if new is not None:
                    self.process_cube(new, val)

    def process_cube(self, cube: Cube, add: bool) -> None:
        new_subs = self.get_intersections(cube, self.add_cubes)
        new_adds = self.get_intersections(cube, self.sub_cubes)
        self.add_cubes += new_adds
        self.sub_cubes += new_subs
        if add:
            self.add_cubes += [cube]

    @staticmethod
    def get_intersections(cube: Cube, previous: List[Cube]) -> List[Cube]:
        output = [] # type: List[Cube]
        for prev_cube in previous:
            intersection = prev_cube.intersection(cube)
            if intersection is not None:
                output.append(intersection)
        return output

    def get_cube(self, coords: str) -> Optional[Cube]:
        x_coords, y_coords, z_coords = coords.split(',')
        x_range = self.process_coords(x_coords)
        if x_range is None:
            return None
        y_range = self.process_coords(y_coords)
        if y_range is None:
            return None
        z_range = self.process_coords(z_coords)
        if z_range is None:
            return None
        return Cube(x_range, y_range, z_range)

    def process_coords(self, coords_str: str) -> Optional[Tuple[int, int]]:
        temp = coords_str.split('=')[1]
        start, end = [int(i) for i in temp.split('..')]
        if self.limit > 0:
            if end < -self.limit or start > self.limit:
                return None
            start = max(start, -self.limit)
            end = min(end, self.limit)
        return start, end

    def get_on_count(self) -> int:
        output = 0
        for cube in self.add_cubes:
            output += cube.size
        for cube in self.sub_cubes:
            output -= cube.size
        return output

R = Reactor('test1.txt')
assert R.get_on_count() == 39

R = Reactor('test2.txt', 50)
assert R.get_on_count() == 590784

R = Reactor('input.txt', 50)
assert R.get_on_count() == 607573
print(R.get_on_count())

R = Reactor('test3.txt')
assert R.get_on_count() == 2758514936282235

R = Reactor('input.txt')
assert R.get_on_count() == 1267133912086024
print(R.get_on_count())
