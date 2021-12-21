from typing import List, NamedTuple, Tuple
import math
import time

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

    def __add__(self, __o: object) -> 'Coord':
        if not isinstance(__o, Coord):
            return NotImplemented
        return Coord(self.x + __o.x, self.y + __o.y, self.z + __o.z)

    def __sub__(self, __o: object) -> 'Coord':
        if not isinstance(__o, Coord):
            return NotImplemented
        return Coord(self.x - __o.x, self.y - __o.y, self.z - __o.z)

    def distance(self, __o: object) -> float:
        if not isinstance(__o, Coord):
            return NotImplemented
        x_diff = (self.x - __o.x) ** 2
        y_diff = (self.y - __o.y) ** 2
        z_diff = (self.z - __o.z) ** 2
        return math.sqrt(x_diff + y_diff + z_diff)

    def manhattan_distance(self, __o: object) -> int:
        if not isinstance(__o, Coord):
            return NotImplemented
        x_diff = abs(self.x - __o.x)
        y_diff = abs(self.y - __o.y)
        z_diff = abs(self.z - __o.z)
        return x_diff + y_diff + z_diff

    def rotate_x(self) -> 'Coord':
        return Coord(self.x, self.z, -self.y)

    def rotate_y(self) -> 'Coord':
        return Coord(-self.z, self.y, self.x)

    def rotate_z(self) -> 'Coord':
        return Coord(-self.y, self.x, self.z)

    def all_rotations(self) -> List['Coord']:
        all_rots = [
            (0,0,0),
            (0,0,1),
            (0,0,2),
            (0,0,3),
            (0,1,0),
            (0,1,1),
            (0,1,2),
            (0,1,3),
            (0,2,0),
            (0,2,1),
            (0,2,2),
            (0,2,3),
            (0,3,0),
            (0,3,1),
            (0,3,2),
            (0,3,3),
            (1,0,0),
            (1,0,1),
            (1,0,2),
            (1,0,3),
            (1,2,0),
            (1,2,1),
            (1,2,2),
            (1,2,3),
        ]
        new = self.copy()
        temp = []
        for x, y, z in all_rots:
            new = self.copy()
            for _ in range(x):
                new = new.rotate_x()
            for _ in range(y):
                new = new.rotate_y()
            for _ in range(z):
                new = new.rotate_z()
            temp.append(new)
        return temp

    def out_of_bounds(self, lim: int) -> bool:
        if abs(self.x) > lim:
            return True
        if abs(self.y) > lim:
            return True
        if abs(self.z) > lim:
            return True
        return False

class Scanner:

    RANGE = 1000
    OVERLAP_COUNT = 12

    def __init__(self, coords: List[Coord], name: str) -> None:
        self.coords = coords
        self.name = name
        self.rot_coords = [] # type: List[List[Coord]]
        self.find_rotated_coords()
        self.distances = [] # type: List[float]
        self.find_distances()
        self.location = Coord(0, 0, 0)

    def find_rotated_coords(self) -> None:
        temp = []
        for coord in self.coords:
            temp.append(coord.all_rotations())
        temp = list(map(list, zip(*temp)))
        self.rot_coords = temp

    def find_distances(self) -> None:
        lim = len(self.coords)
        for i in range(lim - 1):
            for j in range(i + 1, lim):
                distance = self.coords[i].distance(self.coords[j])
                self.distances.append(distance)

    def rotate_base(self, rotation: int) -> None:
        self.coords = self.rot_coords[rotation].copy()

    def overlaps(self, other: 'Scanner') -> bool:
        intersection = list(set(self.distances) & set(other.distances))
        target = int((self.OVERLAP_COUNT * (self.OVERLAP_COUNT - 1)) / 2)
        if len(intersection) >= target:
            return True
        return False

    def overlaps_full(self, other: 'Scanner') -> Tuple[bool, Coord, int]:
        index = 0
        for other_coords in other.rot_coords.copy():
            overlapped, delta = self.overlaps_one_rotation(other_coords)
            if overlapped:
                return True, delta, index
            index += 1
        return False, Coord(0,0,0), 0

    def overlaps_one_rotation(self, other: List[Coord]) -> Tuple[bool, Coord]:
        for coord_s in self.coords.copy()[:-self.OVERLAP_COUNT]:
            for coord_o in other.copy():
                delta = coord_s - coord_o
                if self.overlaps_at(other, delta):
                    return True, delta
        return False, Coord(0,0,0)

    def overlaps_at(self, other: List[Coord], delta: Coord) -> bool:
        overlap_count = 0
        index = 0
        for coord_o in other.copy():
            new_coord = coord_o + delta
            if new_coord in self.coords:
                overlap_count += 1
                if overlap_count == self.OVERLAP_COUNT:
                    return True
            elif not new_coord.out_of_bounds(self.RANGE):
                return False
            elif (len(other) - index - 1) < (self.OVERLAP_COUNT - overlap_count):
                return False
            index += 1
        return False

    def get_0_coords(self) -> List[Coord]:
        output = []
        for coord in self.coords:
            output.append(coord + self.location)
        return output

class Field:

    def __init__(self, file_path: str) -> None:
        self.scanners = [] # type: List[Scanner]
        self.read_file(file_path)
        self.align_scanners()
        self.beacons = [] # type: List[Coord]
        self.get_beacons()

    def read_file(self, file_path: str) -> None:
        coords = [] # type: List[Coord]
        with open(file_path, encoding='UTF-8') as file:
            while line:= file.readline():
                line = line.replace('\n', '').strip()
                if not line or line[:3] == '---':
                    if line[:3] == '---':
                        name = line
                    if coords:
                        new_scanner = Scanner(coords, name)
                        self.scanners.append(new_scanner)
                        coords = []
                else:
                    posn = 0
                    num1, num2, num3 = '', '', ''
                    for char in line:
                        if char == ',':
                            posn += 1
                        elif posn == 0:
                            num1 += char
                        elif posn == 1:
                            num2 += char
                        elif posn == 2:
                            num3 += char
                    coords.append(Coord(int(num1), int(num2), int(num3)))
        if coords:
            new_scanner = Scanner(coords, name)
            self.scanners.append(new_scanner)

    def align_scanners(self) -> None:
        out_scanners = [self.scanners[0]]
        search_scanners = self.scanners[1:].copy()
        while search_scanners:
            for curr_scanner in out_scanners:
                index = 0
                found = False
                for scanner in search_scanners:
                    overlapped = curr_scanner.overlaps(scanner)
                    if overlapped:
                        found = True
                        overlapped, delta, rot = curr_scanner.overlaps_full(scanner)
                        scanner.rotate_base(rot)
                        scanner.location = curr_scanner.location + delta
                        out_scanners.append(scanner)
                        del search_scanners[index]
                        print(f'Found {scanner.name} at {delta}, {len(search_scanners)} remaining')
                        break
                    index += 1
                if found:
                    break
        self.scanners = out_scanners

    def get_beacons(self) -> None:
        beacons = [] # type: List[Coord]
        for scanner in self.scanners:
            beacons = list(set(beacons) | set(scanner.get_0_coords()))
        self.beacons = beacons

    def get_max_distance(self) -> int:
        lim = len(self.scanners)
        maximum = 0
        for i in range(lim - 1):
            for j in range(i + 1, lim):
                a = self.scanners[i].location
                b = self.scanners[j].location
                dist = a.manhattan_distance(b)
                if dist > maximum:
                    maximum = dist
        return maximum

F = Field('test.txt')
assert len(F.beacons) == 79
assert F.get_max_distance() == 3621

start = time.time()

F = Field('input.txt')
assert len(F.beacons) == 465
print(len(F.beacons))
assert F.get_max_distance() == 12149
print(F.get_max_distance())

print(f'--- {round(time.time() - start, 2)} seconds ---')
