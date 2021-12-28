import time
import heapq
from typing import List, Tuple, Optional

class State:

    MOVE_COST = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
    }

    ROOM_LOCATIONS = {
        'A': 2,
        'B': 4,
        'C': 6,
        'D': 8
    }

    EMPTY = '.'

    def __init__(self, corridor: str, rooms: List[str]) -> None:
        self.corridor = list(corridor)
        self.a_room = list(rooms[0])
        self.b_room = list(rooms[1])
        self.c_room = list(rooms[2])
        self.d_room = list(rooms[3])
        self.depth = len(rooms[0])

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, State):
            return NotImplemented
        return self.to_s() == __o.to_s()

    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, State):
            return NotImplemented
        return self.to_s() < __o.to_s()

    def get_all_moves(self) -> List[Tuple[int, 'State']]:
        output = [] # type: List[Tuple[int, 'State']]
        for i, val in enumerate(self.corridor):
            if val != self.EMPTY:
                room_move = self.__get_to_room_move(i, val)
                if room_move is not None:
                    output.append(room_move)
        for room_val in self.ROOM_LOCATIONS:
            room_move = self.__get_room_to_room_move(room_val)
            if room_move is not None:
                output.append(room_move)
        if not output:
            for room_val in self.ROOM_LOCATIONS:
                output += self.__get_from_room_moves(room_val)
        return output

    @staticmethod
    def __return_state(
        corridor: List[str],
        a_room: List[str],
        b_room: List[str],
        c_room: List[str],
        d_room: List[str]
        ) -> 'State':
        return State(
            ''.join(corridor),
            [''.join(a_room),
            ''.join(b_room),
            ''.join(c_room),
            ''.join(d_room)],
        )

    def __return_updated_state(
        self, corridor: List[str],
        room_val: str, room: List[str],
        room_val2: str, room2: List[str]) -> 'State':
        if room_val == 'A':
            new_a = room
        elif room_val2 == 'A':
            new_a = room2
        else:
            new_a = self.a_room.copy()
        if room_val == 'B':
            new_b = room
        elif room_val2 == 'B':
            new_b = room2
        else:
            new_b = self.b_room.copy()
        if room_val == 'C':
            new_c = room
        elif room_val2 == 'C':
            new_c = room2
        else:
            new_c = self.c_room.copy()
        if room_val == 'D':
            new_d = room
        elif room_val2 == 'D':
            new_d = room2
        else:
            new_d = self.d_room.copy()
        return self.__return_state(corridor, new_a, new_b, new_c, new_d)

    def __get_move_cost(self, moves: int, val: str) -> int:
        return moves * self.MOVE_COST[val]

    def __get_corridor_moves(
        self, posn: int, val: str,
        start_moves: int, room_val: str, room: List[str]
        ) -> List[Tuple[int, 'State']]:
        output = self.__get_1_corridor_moves(
            posn, val, range(posn-1, -1, -1),
            start_moves, room_val, room)
        output += self.__get_1_corridor_moves(
            posn, val, range(posn+1, 11),
            start_moves, room_val, room)
        return output

    def __get_1_corridor_moves(
        self, posn: int, val: str, locs: range,
        start_moves: int, room_val: str, room: List[str]
        ) -> List[Tuple[int, 'State']]:
        output = [] # type: List[Tuple[int, 'State']]
        for new_posn in locs:
            if self.corridor[new_posn] != self.EMPTY:
                break
            if new_posn in self.ROOM_LOCATIONS.values():
                continue
            new_corridor = self.corridor.copy()
            new_corridor[new_posn] = val
            new_corridor[posn] = self.EMPTY
            new_state = self.__return_updated_state(new_corridor, room_val, room.copy(), 'NA', [])
            moves = start_moves + abs(new_posn - posn)
            cost = self.__get_move_cost(moves, val)
            output.append((cost, new_state))
        return output

    def __get_room(self, val: str) -> List[str]:
        if val == 'A':
            room = self.a_room.copy()
        elif val =='B':
            room = self.b_room.copy()
        elif val == 'C':
            room = self.c_room.copy()
        elif val == 'D':
            room = self.d_room.copy()
        return room

    def __room_available(self, val: str) -> bool:
        room = self.__get_room(val)
        for char in room:
            if char not in (val, self.EMPTY):
                return False
        return True

    def __get_next_space(self, room: List[str]) -> Optional[int]:
        for posn, val in enumerate(room):
            if posn == 0 and val != self.EMPTY:
                return None
            if val == self.EMPTY:
                if posn == len(room) - 1 or room[posn+1] != self.EMPTY:
                    return posn
        return None

    def __get_first_val(self, room: List[str]) -> Optional[int]:
        space = self.__get_next_space(room)
        if space is None:
            return 0
        if space == len(room) - 1:
            return None
        return space + 1

    def __get_to_room_move(self, posn: int, val: str) -> Optional[Tuple[int, 'State']]:
        if not self.__room_available(val):
            return None
        target_posn = self.ROOM_LOCATIONS[val]
        if target_posn < posn:
            locs = range(posn-1, target_posn-1, -1)
        else:
            locs = range(posn+1, target_posn+1)
        for new_posn in locs:
            if self.corridor[new_posn] != self.EMPTY:
                return None
        room = self.__get_room(val)
        room_posn = self.__get_next_space(room)
        if room_posn is None:
            return None
        new_corridor = self.corridor.copy()
        new_corridor[posn] = self.EMPTY
        room[room_posn] = val
        new_state = self.__return_updated_state(new_corridor, val, room, 'NA', [])
        moves = abs(target_posn - posn) + room_posn + 1
        cost = self.__get_move_cost(moves, val)
        return cost, new_state

    def __get_room_to_room_move(self, room_val: str) -> Optional[Tuple[int, 'State']]:
        if self.__room_available(room_val):
            return None
        room = self.__get_room(room_val)
        room_posn = self.__get_first_val(room)
        if room_posn is None:
            return None
        val = room[room_posn]
        if val == room_val:
            return None
        if not self.__room_available(val):
            return None
        posn = self.ROOM_LOCATIONS[room_val]
        target_posn = self.ROOM_LOCATIONS[val]
        if target_posn < posn:
            locs = range(posn, target_posn-1, -1)
        else:
            locs = range(posn, target_posn+1)
        for new_posn in locs:
            if self.corridor[new_posn] != self.EMPTY:
                return None
        new_room = self.__get_room(val)
        new_room_posn = self.__get_next_space(new_room)
        if new_room_posn is None:
            return None
        room[room_posn] = self.EMPTY
        new_room[new_room_posn] = val
        state = self.__return_updated_state(self.corridor.copy(), room_val, room, val, new_room)
        moves = room_posn + 1 + abs(posn - target_posn) + new_room_posn + 1
        cost = self.__get_move_cost(moves, val)
        return cost, state

    def __get_from_room_moves(self, room_val: str) -> List[Tuple[int, 'State']]:
        if self.__room_available(room_val):
            return []
        room = self.__get_room(room_val)
        room_posn = self.__get_first_val(room)
        if room_posn is None:
            return []
        val = room[room_posn]
        room[room_posn] = self.EMPTY
        return self.__get_corridor_moves(
            self.ROOM_LOCATIONS[room_val], val, room_posn+1, room_val, room)

    def to_s(self) -> str:
        output = ''.join(self.corridor)
        output += ''.join(self.a_room)
        output += ''.join(self.b_room)
        output += ''.join(self.c_room)
        output += ''.join(self.d_room)
        return output

    def pretty_print(self) -> None:
        print('#############')
        line = '#' + ''.join(self.corridor) + '#'
        print(line)
        first = True
        for a, b, c, d in zip(self.a_room, self.b_room, self.c_room, self.d_room):
            line = '  #' + a + '#' + b + '#' + c + '#' + d + '#  '
            if first:
                line = line.replace(' ', '#')
                first = False
            print(line)
        print('  #########  ')

    def distance_to_solved(self) -> int:
        output = self.__distance_corridor()
        output += self.__distance_blocked_corridor()
        for room_val in self.ROOM_LOCATIONS:
            output += self.__distance_room(room_val)
        output -= self.__distance_space_room()
        return output

    def __distance_corridor(self) -> int:
        output = 0
        for i, val in enumerate(self.corridor):
            if val != self.EMPTY:
                moves = abs(i - self.ROOM_LOCATIONS[val]) + self.depth
                output += self.__get_move_cost(moves, val)
        return output

    def __distance_blocked_corridor(self) -> int:
        output = 0
        for pos1, val1 in enumerate(self.corridor):
            if val1 != self.EMPTY:
                target1 = self.ROOM_LOCATIONS[val1]
                for pos2 in range(pos1+1, len(self.corridor)):
                    val2 = self.corridor[pos2]
                    if val2 != self.EMPTY:
                        target2 = self.ROOM_LOCATIONS[val2]
                        if pos1 > target2 and pos2 < target1:
                            moves = (9 - pos2) * 2
                            output += self.__get_move_cost(moves, val2)
        return output

    def __distance_room(self, room_val: str) -> int:
        output = 0
        room = self.__get_room(room_val)
        for i, val in enumerate(room):
            if val == self.EMPTY:
                continue
            if val == room_val:
                if self.__room_available(room_val):
                    moves = self.depth - 1 - i
                else:
                    moves = self.depth + i + 3
            else:
                moves = (i + 1)
                moves += abs(self.ROOM_LOCATIONS[val] - self.ROOM_LOCATIONS[room_val])
                moves += self.depth
            output += self.__get_move_cost(moves, val)
        return output

    def __distance_space_room(self) -> int:
        output = 0
        triangle_depth = int(self.depth * (self.depth - 1) / 2)
        for room_val in self.ROOM_LOCATIONS:
            output += self.__get_move_cost(triangle_depth, room_val)
        return output

class Hallway:

    def __init__(self, file_path: str, add_extra: bool) -> None:
        corridor, room_a, room_b, room_c, room_d = self.__read_file(file_path)
        if add_extra:
            room_a = room_a[0] + 'DD' + room_a[1]
            room_b = room_b[0] + 'CB' + room_b[1]
            room_c = room_c[0] + 'BA' + room_c[1]
            room_d = room_d[0] + 'AC' + room_d[1]
        self.initial_state = State(corridor, [room_a, room_b, room_c, room_d])
        self.frontier = [] # type: List[Tuple[int, int, State, int]]
        heapq.heapify(self.frontier)
        self.visited = [] # type: List[str]
        self.target = '...........'
        self.target += ''.join(['A' for _ in range(len(room_a))])
        self.target += ''.join(['B' for _ in range(len(room_a))])
        self.target += ''.join(['C' for _ in range(len(room_a))])
        self.target += ''.join(['D' for _ in range(len(room_a))])

    @staticmethod
    def __read_file(file_path: str) -> Tuple[str, str, str, str, str]:
        first_line = True
        room_a = ''
        room_b = ''
        room_c = ''
        room_d = ''
        with open(file_path, encoding='UTF-8') as file:
            while line := file.readline():
                line = line.replace('\n', '').strip().replace('#', '')
                if line:
                    if first_line:
                        corridor = line
                        first_line = False
                    else:
                        room_a += line[0]
                        room_b += line[1]
                        room_c += line[2]
                        room_d += line[3]
        return (corridor, room_a, room_b, room_c, room_d)

    def find_min_distance(self) -> int:
        state = self.initial_state
        states = [] # type: List[Tuple[int, State, int, int]]
        self.visited.append(state.to_s())
        cost = 0
        counter = 0
        while state.to_s() != self.target:
            moves = state.get_all_moves()
            for move in moves:
                new_cost, new_state = move
                new_state_s = new_state.to_s()
                if new_state_s not in self.visited:
                    self.visited.append(new_state_s)
                    new_cost += cost
                    heuristic = new_cost + new_state.distance_to_solved()
                    heapq.heappush(self.frontier, (heuristic, new_cost, new_state, counter))
            _, cost, state, from_iter = heapq.heappop(self.frontier)
            counter += 1
            states.append((counter, state, cost, from_iter))
        last_iter = counter
        solve_path = [] # type: List[Tuple[State, int]]
        while states:
            counter, state, cost, from_iter = states.pop()
            if counter == last_iter:
                solve_path.append((state, cost))
                last_iter = from_iter
        last_cost = 0
        while solve_path:
            state, cost = solve_path.pop()
            state.pretty_print()
            print(f'cost: {cost} ({cost - last_cost})\n')
            last_cost = cost
        return cost

start = time.time()

H = Hallway('input.txt', True)
print(H.find_min_distance())

print(f'--- {round(time.time() - start, 2)} seconds ---')
