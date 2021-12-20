from typing import List, NamedTuple, Tuple

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
        if abs(self.x) > lim or abs(self.y) > lim or abs(self.z):
            return True
        return False

class Scanner:

    RANGE = 1000
    OVERLAP_COUNT = 12

    def __init__(self, coords: List[Coord]) -> None:
        self.coords = coords
        self.rot_coords = [] # type: List[List[Coord]]
        self.find_rotated_coords()

    def find_rotated_coords(self) -> None:
        temp = []
        for coord in self.coords:
            temp.append(coord.all_rotations())
        temp = list(map(list, zip(*temp)))
        self.rot_coords = temp

    def rotate_base(self, rotation: int) -> None:
        self.coords = self.rot_coords[rotation].copy()

    def overlaps(self, other: 'Scanner') -> Tuple[bool, Coord, int]:
        index = 0
        for other_coords in other.rot_coords.copy():
            overlapped, delta = self.overlaps_one_rotation(other_coords)
            if overlapped:
                return True, delta, index
            index += 1
        return False, Coord(0,0,0), 0

    def overlaps_one_rotation(self, other: List[Coord]) -> Tuple[bool, Coord]:
        for coord_s in self.coords.copy():
            for coord_o in other.copy():
                delta = coord_s - coord_o
                if self.overlaps_at(other, delta):
                    return True, delta
        return False, Coord(0,0,0)

    def overlaps_at(self, other: List[Coord], delta: Coord) -> bool:
        overlap_count = 0
        for coord_o in other.copy():
            new_coord = coord_o + delta
            if new_coord in self.coords:
                overlap_count += 1
                if overlap_count == self.OVERLAP_COUNT:
                    return True
            elif not new_coord.out_of_bounds(self.RANGE):
                return False
        return False

class Field:

    def __init__(self, file_path: str) -> None:
        self.scanners = [] # type: List[Scanner]
        self.read_file(file_path)

    def read_file(self, file_path: str) -> None:
        coords = [] # type: List[Coord]
        with open(file_path, encoding='UTF-8') as file:
            while line:= file.readline():
                line = line.replace('\n', '').strip()
                if not line or line[:3] == '---':
                    if coords:
                        new_scanner = Scanner(coords)
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
            new_scanner = Scanner(coords)
            self.scanners.append(new_scanner)

    def align_scanners(self) -> None:
        curr_scanner = self.scanners[0]
        out_scanners = [curr_scanner]
        deltas = [] # type: List[Coord]
        search_scanners = self.scanners[1:].copy()
        while search_scanners:
            index = 0
            for scanner in search_scanners:
                overlapped, delta, rot = curr_scanner.overlaps(scanner)
                if overlapped:
                    scanner.rotate_base(rot)
                    out_scanners.append(scanner)
                    curr_scanner = scanner
                    deltas.append(delta)
                    del search_scanners[index]
                    break
                index += 1

F = Field('test.txt')
F.align_scanners()
print(F.scanners[0].overlaps(F.scanners[1]))
