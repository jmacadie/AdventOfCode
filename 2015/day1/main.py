FLOOR = 0
FIRST_BASEMENT = 0
POS = 0
for char in list(open('input.txt').read().strip()):
    POS += 1
    if char == '(':
        FLOOR += 1
    elif char == ')':
        FLOOR -= 1
        if FLOOR == -1 and FIRST_BASEMENT == 0:
            FIRST_BASEMENT = POS
print(FLOOR)
print(FIRST_BASEMENT)
