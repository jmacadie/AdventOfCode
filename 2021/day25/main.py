from typing import NamedTuple


from typing import List

class Point(NamedTuple):
    x: int
    y: int

    def get_right(self, bounds: int) -> 'Point':
        if self.x < (bounds - 1):
            return Point(self.x+1, self.y)
        return Point(0, self.y)

    def get_below(self, bounds: int) -> 'Point':
        if self.y < (bounds - 1):
            return Point(self.x, self.y+1)
        return Point(self.x, 0)

class SeaBed:

    EMPTY = '.'
    EAST = '>'
    SOUTH = 'v'

    def __init__(self, file_path: str) -> None:
        self.__map = [] # type: List[List[str]]
        self.height = 0
        self.width = 0
        self.__read_file(file_path)

    def __read_file(self, file_path: str) -> None:
        first = True
        with open(file_path, encoding='UTF-8') as file:
            while line := file.readline():
                line = line.replace('\n', '').strip()
                if first:
                    self.width = len(line)
                    first = False
                assert len(line) == self.width
                self.height += 1
                self.__map.append(list(line))

    def val(self, p: Point) -> str:
        return self.__map[p.y][p.x]

    def set_val(self, p: Point, val: str) -> None:
        if val not in (self.EMPTY, self.EAST, self. SOUTH):
            raise NotImplementedError
        self.__map[p.y][p.x] = val

    def __right(self, p: Point) -> Point:
        return p.get_right(self.width)

    def __below(self, p: Point) -> Point:
        return p.get_below(self.height)

    def __move(self, p: Point) -> None:
        direction = self.val(p)
        if direction == self.EMPTY:
            return
        move_point = self.__right(p) if direction == self.EAST else self.__below(p)
        if self.val(move_point) != self.EMPTY:
            raise NotImplementedError
        self.set_val(p, self.EMPTY)
        self.set_val(move_point, direction)

    def __is_empty(self, p: Point) -> bool:
        return self.val(p) == self.EMPTY

    def __get_all_cucumbers(self, direction: str) -> List[Point]:
        if direction not in (self.EAST, self. SOUTH):
            raise NotImplementedError
        output = []
        for x in range(self.width):
            for y in range(self.height):
                p = Point(x, y)
                if self.val(p) == direction:
                    output.append(p)
        return output

    def __step_1d(self, direction: str) -> int:
        if direction not in (self.EAST, self. SOUTH):
            raise NotImplementedError
        points = self.__get_all_cucumbers(direction)
        if direction == self.EAST:
            points = [p for p in points if self.__is_empty(self.__right(p))]
        else:
            points = [p for p in points if self.__is_empty(self.__below(p))]
        for p in points:
            self.__move(p)
        return len(points)

    def __step(self) -> int:
        output = self.__step_1d(self.EAST)
        output += self.__step_1d(self.SOUTH)
        return output

    def step_all(self) -> None:
        counter = 0
        moved = 1
        while moved:
            moved = self.__step()
            counter += 1
            print(f'Step {counter} - Moved {moved} cucmbers')

SB = SeaBed('input.txt')
SB.step_all()
