from collections import Counter
import string

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

    def find_unscrambled_letter(self, count, letter):
        if count == 4:
            return 'e'
        if count == 6:
            return 'b'
        if count == 7:
            if letter in self.four:
                return 'd'
            return 'g'
        if count == 8:
            if letter in self.four:
                return 'c'
            return 'a'
        if count == 9:
            return 'f'

    def __init__(self, nums):
        arr = nums.split(' ')
        for scrambled_num in arr:
            if len(scrambled_num) == 4:
                self.four = scrambled_num
                break
        c_nums = Counter(nums)
        self.map = {}
        for char in list(string.ascii_lowercase[0:7]):
            self.map[char] = self.find_unscrambled_letter(c_nums[char], char)

    def decode_one(self, number):
        decoded_num = ''
        for char in number:
            decoded_num += self.map[char]
        decoded_num = ''.join(sorted(decoded_num))
        return self.UNSCRAMBLED_MAP[decoded_num]

    def count_easy(self, nums):
        out = 0
        for num in nums:
            if self.decode_one(num) in [1, 4, 7, 8]:
                out += 1
        return out

    def decode(self, nums):
        temp = 0
        for num in nums:
            temp = temp * 10 + self.decode_one(num)
        return temp


OUT1 = 0
OUT2 = 0
for line in open('input.txt'):
    source, test = line.split('|')
    s = ScrambledNumbers(source.strip())
    test = test.strip().split(' ')
    OUT1 += s.count_easy(test)
    OUT2 += s.decode(test)
print(OUT1)
print(OUT2)

