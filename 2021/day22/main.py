from typing import NamedTuple, List, Tuple

class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def copy(self) -> 'Coord':
        return Coord(self.x, self.y, self.z)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Coord):
            return NotImplemented
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

class PointVal(NamedTuple):
    loc: Coord
    val: bool

class Cube:

    def __init__(
        self,
        x_start: int, x_end: int,
        y_start: int, y_end: int,
        z_start: int, z_end: int,
        val: bool
        ) -> None:
        self.x_start = x_start
        self.y_start = y_start
        self.z_start = z_start
        self.x = list(range(x_start, x_end + 1))
        self.y = list(range(y_start, y_end + 1))
        self.z = list(range(z_start, z_end + 1))
        self.vals = [] # type: List[List[List[int]]]
        for _ in self.z:
            plane = [] # type: List[List[int]]
            for _ in self.y:
                line = [] # type: List[int]
                for _ in self.x:
                    line.append(val)
                plane.append(line)
            self.vals.append(plane)

    def get_val_at_point(self, loc: Coord) -> int:
        x = loc.x - self.x_start
        y = loc.y - self.y_start
        z = loc.z - self.z_start
        return self.vals[z][y][x]

    def get_all_points(self) -> List[PointVal]:
        points = []
        for x in self.x:
            for y in self.y:
                for z in self.z:
                    point = Coord(x, y, z)
                    val = self.get_val_at_point(point)
                    points.append(PointVal(point, val))
        return points

    def update(self, update: PointVal) -> None:
        if update.loc.x in self.x and update.loc.y in self.y and update.loc.z in self.z:
            self.vals[update.loc.z][update.loc.y][update.loc.x] = update.val

class CubeFactory:

    RANGE = 51

    def __init__(self, line: str) -> None:
        val_str, coords = line.split(' ')
        self.val = (val_str == 'on')
        x_coords, y_coords, z_coords = coords.split(',')
        self.x_start, self.x_end = self.process_coords(x_coords)
        self.y_start, self.y_end = self.process_coords(y_coords)
        self.z_start, self.z_end = self.process_coords(z_coords)

    def process_coords(self, coords_str: str) -> Tuple[int, int]:
        temp = coords_str.split('=')[1]
        start, end = temp.split('..')
        start_i = min(max(int(start), -self.RANGE), self.RANGE)
        end_i = min(max(int(end), -self.RANGE), self.RANGE)
        return start_i, end_i

    def get_cube(self) -> Cube:
        return Cube(
            self.x_start, self.x_end,
            self.y_start, self.y_end,
            self.z_start, self.z_end,
            self.val)

class Reactor:

    RANGE = 50

    def __init__(self) -> None:
        self.map = Cube(
            -self.RANGE, self.RANGE,
            -self.RANGE, self.RANGE,
            -self.RANGE, self.RANGE,
            False)

    def reboot_step(self, cube: Cube) -> None:
        for point in cube.get_all_points():
            self.map.update(point)

    def get_on_count(self) -> int:
        count = 0
        for point in self.map.get_all_points():
            if point.val:
                count += 1
        return count

class RebootFactory:

    def __init__(self, file_path: str) -> None:
        self.reactor = Reactor()
        self.process_file(file_path)

    def process_file(self, file_path: str) -> None:
        with open(file_path, encoding='UTF-8') as file:
            while line := file.readline():
                line = line.replace('\n', '').strip()
                update_cube = CubeFactory(line).get_cube()
                self.reactor.reboot_step(update_cube)

#R = Reactor()
#C = CubeFactory('on x=10..12,y=10..12,z=10..12').get_cube()
#R.reboot_step(C)
#print(R.get_on_count())

RF = RebootFactory('test1.txt')
assert RF.reactor.get_on_count() == 39

RF = RebootFactory('test2.txt')
assert RF.reactor.get_on_count() == 590784

RF = RebootFactory('input.txt')
assert RF.reactor.get_on_count() == 607573
print(RF.reactor.get_on_count())
