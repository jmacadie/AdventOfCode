from typing import Tuple, Dict

class Polymer:

    def __init__(self, file_path: str) -> None:
        self.template = ''
        self.rules = {} # type: Dict[str, str]
        self.pairs = {} # type: Dict[str, int]
        self.letters = {} # type: Dict[str, int]
        self.read_file(file_path)
        self.template_to_dict()

    def read_file(self, file_path: str) -> None:
        template = True
        with open(file_path, encoding='UTF-8') as file:
            while line:= file.readline():
                if line == '\n':
                    template = False
                elif template:
                    self.template = line.replace('\n', ''). strip()
                else:
                    line = line.replace('\n', '').strip()
                    pair, insertion = line.split(' -> ')
                    self.rules[pair] = insertion

    def template_to_dict(self) -> None:
        for i in range(len(self.template) - 1):
            pair = self.template[i:i+2]
            if pair not in list(self.pairs.keys()):
                self.pairs[pair] = 1
            else:
                self.pairs[pair] = self.pairs[pair] + 1

    def add_step(self) -> None:
        temp = self.pairs.copy()
        for k, v in self.pairs.items():
            temp[k] = temp[k] - v
            for key in self.find_insertion(k):
                if key not in list(temp.keys()):
                    temp[key] = v
                else:
                    temp[key] = temp[key] + v
        self.pairs = temp
        self.calc_letter_freq()

    def calc_letter_freq(self) -> None:
        self.letters.clear()
        for k, v in self.pairs.items():
            self.add_letter(k[0], v)
        self.add_letter(self.template[-1], 1)

    def add_letter(self, letter: str, count: int) -> None:
        if letter not in self.letters:
            self.letters[letter] = count
        else:
            self.letters[letter] = self.letters[letter] + count

    def find_insertion(self, pair: str) -> Tuple[str, str]:
        insert = self.rules[pair]
        return (pair[:1] + insert, insert + pair[-1:])

    def length(self) -> int:
        sum_tmp = 0
        for _, v in self.letters.items():
            sum_tmp += v
        return sum_tmp

    def special(self) -> int:
        return max(self.letters.values()) - min(self.letters.values())

P = Polymer('test.txt')
for _ in range(5):
    P.add_step()
assert P.length() == 97
for _ in range(5):
    P.add_step()
assert P.length() == 3073
#assert P.get_max_letter() == ('B', 1749)
#assert P.get_min_letter() == ('H', 161)
assert P.special() == 1588

P = Polymer('input.txt')
for _ in range(10):
    P.add_step()
assert P.special() == 3284
print(P.special())
for _ in range(30):
    P.add_step()
assert P.special() == 4302675529689
print(P.special())
