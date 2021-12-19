from typing import Tuple
import math

class Snailfish:

    MAX_DEPTH = 4
    MAX_VAL = 9

    def __init__(self, inp: str) -> None:
        self.string = inp
        self.nested_index = 0
        self.big_index_start = 0
        self.big_index_end = 0

    def __add__(self, other) -> 'Snailfish':
        if not isinstance(other, Snailfish):
            return NotImplemented
        new_str = '[' + self.string + ',' + other.string + ']'
        new = Snailfish(new_str)
        new.reduce()
        return new

    def too_nested(self) -> bool:
        count = 0
        index = 0
        for char in self.string:
            if char == '[':
                count += 1
                if count > self.MAX_DEPTH:
                    self.nested_index = index
                    return True
            elif char == ']':
                count -= 1
            index += 1
        return False

    def explode(self) -> None:
        start = self.nested_index
        index = start
        for char in self.string[start:]:
            if char == ',':
                mid = index
            elif char == ']':
                end = index
                break
            index += 1
        left_start, left_end = self.find_num_left(start)
        right_start, right_end = self.find_num_right(end)
        if left_start > 0:
            left_num = int(self.string[left_start:left_end+1])
            left_num += int(self.string[start+1:mid].strip())
            new = self.string[:left_start] + str(left_num) + self.string[left_end+1:start]
        else:
            new = self.string[:start]
        new += '0'
        if right_end > 0:
            right_num = int(self.string[right_start:right_end+1])
            right_num += int(self.string[mid+1:end].strip())
            new += self.string[end+1:right_start] + str(right_num) + self.string[right_end+1:]
            #s = self.string[right_end+1:]
            #new += self.string[right_end+1:]
            #new += self.string[end+1:right_start] + str(right_num) + self.string[right_end+1:]
        else:
            new += self.string[end+1:]
        self.string = new

    def find_num_left(self, start) -> Tuple[int, int]:
        index = start
        num_start, num_end = 0, 0
        while index > 0:
            index -= 1
            if self.string[index].isdigit() and num_end == 0:
                num_end = index
            if not self.string[index].isdigit() and num_end != 0:
                num_start = index + 1
                break
        return (num_start, num_end)

    def find_num_right(self, start) -> Tuple[int, int]:
        index = start
        num_start, num_end = 0, 0
        while index < len(self.string) - 1:
            index += 1
            if self.string[index].isdigit() and num_start == 0:
                num_start = index
            if not self.string[index].isdigit() and num_start != 0:
                num_end = index - 1
                break
        return (num_start, num_end)

    def too_big(self) -> bool:
        num_start, num_end = 0, 0
        index = 0
        for char in self.string:
            if char.isdigit() and num_start == 0:
                num_start = index
            if not char.isdigit() and num_start != 0:
                num_end = index - 1
                num = int(self.string[num_start:num_end+1])
                if num > self.MAX_VAL:
                    self.big_index_start = num_start
                    self.big_index_end = num_end
                    return True
                else:
                    num_start, num_end = 0, 0
            index += 1
        return False

    def split(self) ->None:
        num = int(self.string[self.big_index_start:self.big_index_end+1])
        part1 = math.floor(num / 2)
        part2 = math.ceil(num / 2)
        new = self.string[:self.big_index_start]
        new += '[' + str(part1) + ',' + str(part2) + ']'
        new += self.string[self.big_index_end+1:]
        self.string = new

    def reduce(self) -> None:
        while self.too_nested():
            self.explode()
        if self.too_big():
            self.split()
            self.reduce()

SN = Snailfish('[[[[[9,8],1],2],3],4]')
if SN.too_nested():
    SN.explode()
assert SN.string == '[[[[0,9],2],3],4]'

SN = Snailfish('[7,[6,[5,[4,[3,2]]]]]')
if SN.too_nested():
    SN.explode()
assert SN.string == '[7,[6,[5,[7,0]]]]'

SN = Snailfish('[[6,[5,[4,[3,2]]]],1]')
if SN.too_nested():
    SN.explode()
assert SN.string == '[[6,[5,[7,0]]],3]'

SN = Snailfish('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
if SN.too_nested():
    SN.explode()
assert SN.string == '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'

SN = Snailfish('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
if SN.too_nested():
    SN.explode()
assert SN.string == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'

SN1 = Snailfish('[[[[4,3],4],4],[7,[[8,4],9]]]')
SN2 = Snailfish('[1,1]')
SN = SN1 + SN2
assert SN.string == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

SN1 = Snailfish('[1,1]')
SN2 = Snailfish('[2,2]')
SN3 = Snailfish('[3,3]')
SN4 = Snailfish('[4,4]')
SN = SN1 + SN2 + SN3 + SN4
assert SN.string == '[[[[1,1],[2,2]],[3,3]],[4,4]]'

SN1 = Snailfish('[1,1]')
SN2 = Snailfish('[2,2]')
SN3 = Snailfish('[3,3]')
SN4 = Snailfish('[4,4]')
SN5 = Snailfish('[5,5]')
SN = SN1 + SN2 + SN3 + SN4 + SN5
assert SN.string == '[[[[3,0],[5,3]],[4,4]],[5,5]]'

SN1 = Snailfish('[1,1]')
SN2 = Snailfish('[2,2]')
SN3 = Snailfish('[3,3]')
SN4 = Snailfish('[4,4]')
SN5 = Snailfish('[5,5]')
SN6 = Snailfish('[6,6]')
SN = SN1 + SN2 + SN3 + SN4 + SN5 + SN6
assert SN.string == '[[[[5,0],[7,4]],[5,5]],[6,6]]'

SN1 = Snailfish('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]')
SN2 = Snailfish('[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]')
SN3 = Snailfish('[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]')
SN4 = Snailfish('[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]')
SN5 = Snailfish('[7,[5,[[3,8],[1,4]]]]')
SN6 = Snailfish('[[2,[2,2]],[8,[8,1]]]')
SN7 = Snailfish('[2,9]')
SN8 = Snailfish('[1,[[[9,3],9],[[9,0],[0,7]]]]')
SN9 = Snailfish('[[[5,[7,4]],7],1]')
SN10 = Snailfish('[[[[4,2],2],6],[8,7]]')
SN = SN1 + SN2 + SN3 + SN4 + SN5 + SN6 + SN7 + SN8 + SN9 + SN10
assert SN.string == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
