
with open('input.txt') as f:
    grid = [line.strip() for line in f]

print('rows: ' + str(len(grid)))
width = len(grid[0])

trees = 0
pos = 0
for row in grid:
    if row[pos] == '#':
        trees += 1
    pos = (pos + 3) % width

print(trees)