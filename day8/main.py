from collections import Counter

class ScrambledNumbers:

    UNSCRAMBLED_MAP = {
        'abcefg': 0,
        'cf': 1,
        'acdeg': 2,
        'acdfg': 3,
        'bcdf': 4,
        'abdfg': 5,
        'abdefg': 6,
        'acf': 7,
        'abcdefg': 8,
        'abcdfg': 9
        }

    def find_unscrambled_letter(self, count, letter, four):
        if count == 4:
            return 'e'
        elif count == 6:
            return 'b'
        elif count == 7:
            if letter in four:
                return 'd'
            return 'g'
        elif count == 8:
            if letter in four:
                return 'c'
            return 'a'
        elif count == 9:
            return 'f'

    def __init__(self, nums):
        arr = nums.split(' ')
        for scrambled_num in arr:
            if len(scrambled_num) == 4:
                four = scrambled_num
                break
        c_nums = Counter(nums)
        self.map = {}
        self.map['a'] = self.find_unscrambled_letter(c_nums['a'], 'a', four)
        self.map['b'] = self.find_unscrambled_letter(c_nums['b'], 'b', four)
        self.map['c'] = self.find_unscrambled_letter(c_nums['c'], 'c', four)
        self.map['d'] = self.find_unscrambled_letter(c_nums['d'], 'd', four)
        self.map['e'] = self.find_unscrambled_letter(c_nums['e'], 'e', four)
        self.map['f'] = self.find_unscrambled_letter(c_nums['f'], 'f', four)
        self.map['g'] = self.find_unscrambled_letter(c_nums['g'], 'g', four)

    def decode(self, number):
        decoded_num = ''
        for char in number:
            decoded_num += self.map[char]
        decoded_num = ''.join(sorted(decoded_num))
        return self.UNSCRAMBLED_MAP[decoded_num]

out = 0
for line in open('input.txt'):
    ls = line.split('|')
    s = ScrambledNumbers(ls[0].strip())
    testNums = ls[1].strip().split(' ')
    temp = 0
    for num in testNums:
        #if s.decode(num) in [1, 4, 7, 8]:
        #    out += 1
        temp = temp * 10 + s.decode(num)
    out += temp
print(out)

