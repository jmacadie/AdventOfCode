import time
from typing import List, Tuple, Optional, Dict

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

    def __init__(self, corridor: str, a_room: str, b_room: str, c_room: str, d_room: str) -> None:
        self.corridor = list(corridor)
        self.a_room = list(a_room)
        self.b_room = list(b_room)
        self.c_room = list(c_room)
        self.d_room = list(d_room)

    def get_all_moves(self) -> List[Tuple['State', int]]:
        output = []
        for i, val in enumerate(self.corridor):
            if val != self.EMPTY:
                room_move = self.get_to_room_move(i, val)
                if room_move is not None:
                    output.append(room_move)
        if not output:
            for i, val in enumerate(self.corridor):
                if val != self.EMPTY:
                    output += self.get_corridor_moves(i, val, 0, 'NA', [])
            for room_val in self.ROOM_LOCATIONS:
                output += self.get_from_room_moves(room_val)
        return output

    @staticmethod
    def return_state(
        corridor: List[str],
        a_room: List[str],
        b_room: List[str],
        c_room: List[str],
        d_room: List[str]
        ) -> 'State':
        return State(
            ''.join(corridor),
            ''.join(a_room),
            ''.join(b_room),
            ''.join(c_room),
            ''.join(d_room),
        )

    def return_updated_state(self, corridor: List[str], room_val: str, room: List[str]) -> 'State':
        new_a = room if room_val == 'A' else self.a_room.copy()
        new_b = room if room_val == 'B' else self.b_room.copy()
        new_c = room if room_val == 'C' else self.c_room.copy()
        new_d = room if room_val == 'D' else self.d_room.copy()
        return self.return_state(corridor, new_a, new_b, new_c, new_d)

    def get_move_cost(self, moves: int, val: str) -> int:
        return moves * self.MOVE_COST[val]

    def get_corridor_moves(
        self, posn: int, val: str,
        start_moves: int, room_val: str, room: List[str]
        ) -> List[Tuple['State', int]]:
        output = self.get_1_corridor_moves(
            posn, val, range(posn-1, -1, -1),
            start_moves, room_val, room)
        output += self.get_1_corridor_moves(
            posn, val, range(posn+1, 11),
            start_moves, room_val, room)
        return output

    def get_1_corridor_moves(
        self, posn: int, val: str, locs: range,
        start_moves: int, room_val: str, room: List[str]
        ) -> List[Tuple['State', int]]:
        output = [] # type: List[Tuple['State', int]]
        for new_posn in locs:
            if self.corridor[new_posn] != self.EMPTY:
                break
            if new_posn in self.ROOM_LOCATIONS.values():
                continue
            new_corridor = self.corridor.copy()
            new_corridor[new_posn] = val
            new_corridor[posn] = self.EMPTY
            new_state = self.return_updated_state(new_corridor, room_val, room.copy())
            moves = start_moves + abs(new_posn - posn)
            cost = self.get_move_cost(moves, val)
            output.append((new_state, cost))
        return output

    def get_room(self, val: str) -> List[str]:
        if val == 'A':
            room = self.a_room.copy()
        elif val =='B':
            room = self.b_room.copy()
        elif val == 'C':
            room = self.c_room.copy()
        elif val == 'D':
            room = self.d_room.copy()
        return room

    def room_available(self, val: str) -> bool:
        room = self.get_room(val)
        for char in room:
            if char not in (val, self.EMPTY):
                return False
        return True

    def get_next_space(self, room: List[str]) -> Optional[int]:
        for posn, val in enumerate(room):
            if posn == 0 and val != self.EMPTY:
                return None
            if val == self.EMPTY:
                if posn == len(room) - 1 or room[posn+1] != self.EMPTY:
                    return posn
        return None

    def get_first_val(self, room: List[str]) -> Optional[int]:
        space = self.get_next_space(room)
        if space is None:
            return 0
        if space == len(room) - 1:
            return None
        return space + 1

    def get_to_room_move(self, posn: int, val: str) -> Optional[Tuple['State', int]]:
        if not self.room_available(val):
            return None
        target_posn = self.ROOM_LOCATIONS[val]
        if target_posn < posn:
            locs = range(posn-1, target_posn-1, -1)
        else:
            locs = range(posn+1, target_posn+1)
        for new_posn in locs:
            if self.corridor[new_posn] != self.EMPTY:
                return None
        room = self.get_room(val)
        room_posn = self.get_next_space(room)
        if room_posn is None:
            return None
        new_corridor = self.corridor.copy()
        new_corridor[posn] = self.EMPTY
        room[room_posn] = val
        new_state = self.return_updated_state(new_corridor, val, room)
        moves = abs(target_posn - posn) + room_posn + 1
        cost = self.get_move_cost(moves, val)
        return new_state, cost

    def get_from_room_moves(self, room_val: str) -> List[Tuple['State', int]]:
        if self.room_available(room_val):
            return []
        room = self.get_room(room_val)
        room_posn = self.get_first_val(room)
        if room_posn is None:
            return []
        val = room[room_posn]
        room[room_posn] = self.EMPTY
        return self.get_corridor_moves(
            self.ROOM_LOCATIONS[room_val], val, room_posn+1, room_val, room)

    def to_s(self) -> str:
        output = ''.join(self.corridor)
        output += ''.join(self.a_room)
        output += ''.join(self.b_room)
        output += ''.join(self.c_room)
        output += ''.join(self.d_room)
        return output

class Hallway:

    def __init__(self, file_path: str) -> None:
        self.states = {} # type: Dict[str, int]
        self.read_file(file_path)
        self.add_or_update(self.initial_state.to_s(), 0)

    def read_file(self, file_path: str) -> None:
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
        self.initial_state = State(corridor, room_a, room_b, room_c, room_d)

    def add_or_update(self, state: str, cost: int) -> bool:
        if state not in self.states:
            self.states[state] = cost
            return True
        if self.states[state] > cost:
            self.states[state] = cost
            return True
        return False

    def find_min_states(self) -> None:
        self.find_min_states_int(self.initial_state, 0, 0.0, 1.0)

    def find_min_states_int(self, state: State, curr_cost: int, pcnt_from: float, pcnt_to: float) -> None:
        moves = state.get_all_moves()
        pcnt_inc = (pcnt_to - pcnt_from)/max(len(moves), 1)
        pcnt = pcnt_from
        for move in moves:
            new_state, cost = move
            cost += curr_cost
            if self.add_or_update(new_state.to_s(), cost):
                print(f'{new_state.to_s()} - {round(pcnt * 100, 0)} % done')
                self.find_min_states_int(new_state, cost, pcnt, pcnt+pcnt_inc)
            pcnt += pcnt_inc

start = time.time()

H = Hallway('input.txt')
H.find_min_states()
print(H.states['...........AABBCCDD'])

print(f'--- {round(time.time() - start, 2)} seconds ---')
