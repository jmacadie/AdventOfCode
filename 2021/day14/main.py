from collections import Counter
from typing import Tuple, Dict

class Polymer:

    def __init__(self, file_path: str) -> None:
        self.template = ''
        self.rules = {} # type: Dict[str, str]
        self.read_file(file_path)
    
    def read_file(self, file_path: str) -> None:
        template = True
        with open(file_path, encoding='UTF-8') as file:
            while line:= file.readline():
                if line == '\n':
                    template = False
                elif template:
                    self.template  = line.replace('\n', ''). strip()
                else:
                    line = line.replace('\n', '').strip()
                    pair, insertion = line.split(' -> ')
                    self.rules[pair] = insertion

    def add_step(self) -> None:
        tmp_str = ''
        for i in range(len(self.template) - 1):
            pair = self.template[i:i+2]
            insertion = self.rules[pair]
            tmp_str += pair[:1] + insertion
        tmp_str += self.template[-1:]
        self.template = tmp_str

    def get_max_letter(self) -> Tuple[str, int]:
        letters = Counter(self.template)
        letter = max(letters, key=letters.get)
        return (letter, letters[letter])

    def get_min_letter(self) -> Tuple[str, int]:
        letters = Counter(self.template)
        letter =  min(letters, key=letters.get)
        return (letter, letters[letter])
    
    def special(self) -> int:
        max = self.get_max_letter()
        min = self.get_min_letter()
        return max[1] - min[1]

P = Polymer('test.txt')
P.add_step() #1
assert P.template == 'NCNBCHB' 
P.add_step() #2
assert P.template == 'NBCCNBBBCBHCB' 
P.add_step() #3
assert P.template == 'NBBBCNCCNBBNBNBBCHBHHBCHB' 
P.add_step() #4
assert P.template == 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB' 
P.add_step() #5
assert len(P.template) == 97
P.add_step() #6
P.add_step() #7
P.add_step() #8
P.add_step() #9
P.add_step() #10
assert len(P.template) == 3073
assert P.get_max_letter() == ('B', 1749)
assert P.get_min_letter() == ('H', 161)
assert P.special() == 1588

P = Polymer('input.txt')
for i in range(10):
    P.add_step()
assert P.special() == 3284
print(P.special())
