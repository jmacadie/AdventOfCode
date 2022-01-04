from typing import Counter

class SyntaxChecker:

    BAD = ('ab', 'cd', 'pq', 'xy')
    VOWELS = ('a','e','i','o','u')

    def __init__(self, text: str) -> None:
        self.text = text

    def three_vowels(self) -> bool:
        vowels = [char for char in self.text if char in self.VOWELS]
        return len(vowels) >=3

    def double_letter(self) -> bool:
        pairs = zip(self.text[:-1], self.text[1:])
        for first, second in pairs:
            if first == second:
                return True
        return False

    def bad_seqs(self) -> bool:
        for bad in self.BAD:
            if bad in self.text:
                return True
        return False

    def is_nice1(self) -> bool:
        if not self.three_vowels():
            return False
        if not self.double_letter():
            return False
        if self.bad_seqs():
            return False
        return True

    def triple_letter(self, char: str) -> bool:
        trips = zip(self.text[:-2], self.text[1:-1], self.text[2:])
        trips_eq = [a for a, b, c in trips if a == char and b == char and c == char]
        return len(trips_eq) > 0

    def double_pair(self) -> bool:
        pairs = Counter(zip(self.text[:-1], self.text[1:]))
        multi = [(p, c) for p, c in pairs.items() if c > 1]
        for p, c in multi:
            a, b = p
            if a != b:
                return True
            if c > 2:
                return True
            if not self.triple_letter(a):
                return True
        return False

    def oxo(self) -> bool:
        trips = zip(self.text[:-2], self.text[2:])
        for first, third in trips:
            if first == third:
                return True
        return False

    def is_nice2(self) -> bool:
        if not self.double_pair():
            return False
        if not self.oxo():
            return False
        return True

def checkfile(file_path: str) -> int:
    counter = 0
    with open(file_path, encoding='UTF-8') as file:
        while line:= file.readline():
            line = line.replace('\n', '').strip()
            syn = SyntaxChecker(line)
            if syn.is_nice2():
                counter += 1
    return counter

print(checkfile('input.txt'))
