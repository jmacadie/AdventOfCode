import re

class BingoBoard:
    def __init__(self, line1, line2, line3, line4, line5):
        self.board = []
        l = re.split(r'\s+', line1)
        self.board.append(l)
        l = re.split(r'\s+', line2)
        self.board.append(l)
        l = re.split(r'\s+', line3)
        self.board.append(l)
        l = re.split(r'\s+', line4)
        self.board.append(l)
        l = re.split(r'\s+', line5)
        self.board.append(l)

        self.called = []
        self.called.append([0,0,0,0,0])
        self.called.append([0,0,0,0,0])
        self.called.append([0,0,0,0,0])
        self.called.append([0,0,0,0,0])
        self.called.append([0,0,0,0,0])

    def call(self, num):
        for row in range(0, 5):
            for col in range(0, 5):
                if self.board[row][col] == num:
                    self.called[row][col] = 1

    def isBingo(self):
        for row in range(0, 5):
            sum = 0
            for num in self.called[row]:
                sum += num
            if sum == 5:
                return True
        for col in range (0, 5):
            sum = 0
            for row in range(0, 5):
                sum += self.called[row][col]
            if sum == 5:
                return True
        return False

    def score(self):
        sum = 0
        for row in range(0, 5):
            for col in range(0, 5):
                if self.called[row][col] == 0:
                    sum += int(self.board[row][col])
        return sum

    def show(self):
        print(self.board)
        print(self.called)

from pathlib import Path

moves_txt = Path('moves.txt').read_text()
moves_txt = moves_txt.replace('\n', '')
moves = moves_txt.split(",")

p = Path('boards.txt')
boards = []
lines = []
with p.open() as f:
    while line := f.readline():
        if len(line) > 3:
            lines.append(line.lstrip().replace('\n', ''))
        if len(lines) == 5:
            b = BingoBoard(lines[0], lines[1], lines[2], lines[3], lines [4])
            boards.append(b)
            lines = []

#for m in moves:
#    for b in boards:
#        b.call(m)
#        if b.isBingo():
#            print(m)
#            print(b.score())
#            print(int(m) * b.score())
#            break
#        else:
#            continue
#        break
#    else:
#        continue
#    break

for m in moves:
    for b in list(boards):
        b.call(m)
        if b.isBingo():
            if len(boards) == 1:
                print(m)
                print(b.score())
                print(int(m) * b.score())
                break
            else:
                boards.remove(b)
                continue
            break
        else:
            continue
        break
    else:
        continue
    break
