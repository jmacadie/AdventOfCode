from functools import reduce

TOT_AREA = 0
TOT_RIB = 0
for line in open('input.txt'):
    line = line.replace('/n', '').strip()
    dims = sorted([int(x) for x in line.split('x')])

    sides = [dims[0] * dims[1], dims[0] * dims[2], dims[1] * dims[2]]
    min_side = sides[0]
    area = 2 * reduce(lambda a, b: a + b, sides)
    TOT_AREA += area + min_side

    perim = 2 * (dims[0] + dims[1])
    vol = reduce(lambda a, b: a * b, dims)
    TOT_RIB += perim + vol

print(TOT_AREA)
print(TOT_RIB)
