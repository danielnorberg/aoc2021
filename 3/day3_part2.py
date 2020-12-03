
with open('input.txt') as f:
    grid = [line.strip() for line in f]

height = len(grid)
width = len(grid[0])

# delta x, y
strides = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]

multrees = 1
trees = 0
x = 0
y = 0
for stride in strides:
    y = 0
    x = 0
    trees = 0
    dx, dy = stride
    while y < height:
        row = grid[y]
        if row[x] == '#':
            trees += 1
        x = (x + dx) % width
        y += dy
    print('stride: {} {}'.format(*stride))
    print('trees: {}'.format(trees))
    multrees *= trees

print(multrees)
