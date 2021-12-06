from pathlib import Path

class School:

    def __init__(self, startTxt):
        self.state = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
        initialSchool = startTxt.split(',')
        for i in initialSchool:
            self.state[int(i)] = self.state[int(i)] + 1

    def addDay(self):
        temp = dict(self.state)
        self.state[8] = temp[0]
        self.state[7] = temp[8]
        self.state[6] = temp[0] + temp[7]
        self.state[5] = temp[6]
        self.state[4] = temp[5]
        self.state[3] = temp[4]
        self.state[2] = temp[3]
        self.state[1] = temp[2]
        self.state[0] = temp[1]

    def size(self):
        return self.state[8] + self.state[7] + self.state[6] + self.state[5] + self.state[4] + self.state[3] + self.state[2] + self.state[1] + self.state[0]

    def show(self):
        print(self.state)

startTxt = Path('input.txt').read_text()
startTxt = startTxt.lstrip().replace('\n', '')

s = School(startTxt)
for i in range(256):
    s.addDay()
s.show()
print(s.size())
