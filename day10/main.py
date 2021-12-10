class ParenLine:

    MATCHED = [
        ('(', ')'),
        ('[', ']'),
        ('{', '}'),
        ('<', '>')]
    OPENING, CLOSING = list(zip(*MATCHED))
    SYNTAX_POINTS = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137}
    AUTO_POINTS = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4}

    def parens_match(self, start, end):
        return ((start, end) in self.MATCHED)

    def get_matching_paren(self, paren):
        matched = self.MATCHED.copy()
        for pair in matched:
            if paren == pair[0]:
                return pair[1]
            if paren == pair[1]:
                return pair[0]
        return False

    def process_char(self, char):
        if char in self.OPENING:
            self.stack.append(char)
        elif char in self.CLOSING:
            open_char = self.stack.pop()
            if not self.parens_match(open_char, char):
                self.bad_char = char
                self.state = 'corrupted'
                return False
        return True

    def __init__(self, line_input):
        self.stack = []
        self.bad_char = ''
        for char in list(line_input):
            if not self.process_char(char):
                return
        if not self.stack:
            self.state = 'complete'
        else:
            self.state = 'incomplete'

    def syntax_error_score(self):
        if self.state == 'corrupted':
            return self.SYNTAX_POINTS[self.bad_char]
        return 0

    def get_autocomplete_string(self):
        openings = self.stack.copy()
        out = ''
        while openings:
            char = openings.pop()
            out += self.get_matching_paren(char)
        return out

    def autocomplete_score(self):
        if self.state == 'incomplete':
            score = 0
            auto = self.get_autocomplete_string()
            for char in auto:
                score *= 5
                score += self.AUTO_POINTS[char]
            return score
        return 0

SUM = 0
S = []
for line in open('input.txt'):
    PL = ParenLine(line.replace('/n', '').strip())
    SUM += PL.syntax_error_score()
    if PL.state == 'incomplete':
        S.append(PL.autocomplete_score())
S.sort()
MID = int((len(S)-1)/2)
assert SUM == 168417
assert S[MID] == 2802519786
print(SUM)
print(S[MID])

