import sys
from itertools import product
from operator import add


def shape(grid):
    n = len(next(iter(grid.keys())))
    shape = [[sys.maxsize, -sys.maxsize] for i in range(n)]
    for c in grid.keys():
        for s, v in zip(shape, c):
            s[0] = min(s[0], v)
            s[1] = max(s[1], v + 1)
    return shape


def get_cell(grid, c):
    return grid.get(c, '.')


def put_cell(grid, c, cell):
    if cell == '.':
        grid.pop(c, None)
    else:
        grid[c] = cell


def print_grid(grid):
    ds = shape(grid)
    print('shape: {}'.format(ds))
    for d in product(*(range(*d) for d in ds[2:])):
        print()
        print('hyper={}'.format(d))
        for y in range(*ds[1]):
            row = [get_cell(grid, (x, y) + tuple(d)) for x in range(*ds[0])]
            print("".join(row))


def read_grid(f, n):
    grid = {}
    for y, row in enumerate(f):
        for x, state in enumerate(row.strip()):
            c = (x, y) + tuple(0 for _ in range(n - 2))
            put_cell(grid, c, state)
    return grid


def expanded_shape(grid):
    ds = shape(grid)
    for d in ds:
        d[0] -= 1
        d[1] += 1
    return ds


def neigbors(grid, c):
    ds = [(-1, 0, 1) for _ in c]
    for dc in product(*ds):
        if not any(dc):
            continue
        nc = tuple(map(add, c, dc))
        yield get_cell(grid, nc)


def active_neigbors(grid, c):
    return sum(1 for cell in neigbors(grid, c) if cell == '#')


def play_grid(grid):
    new_grid = {}
    ds = [range(*d) for d in expanded_shape(grid)]
    for c in product(*ds):
        cell = get_cell(grid, c)
        active = active_neigbors(grid, c)
        if cell == '#' and active not in (2, 3):
            put_cell(new_grid, c, '.')
        elif cell == '.' and active == 3:
            put_cell(new_grid, c, '#')
        else:
            put_cell(new_grid, c, cell)
    return new_grid


def main():
    with open('sample_input.txt') as f:
        grid = read_grid(f, 4)

    assert active_neigbors(grid, (0, 0, 0, 0)) == 1
    assert active_neigbors(grid, (1, 0, 0, 0)) == 1
    assert active_neigbors(grid, (2, 0, 0, 0)) == 2
    assert active_neigbors(grid, (0, 1, 0, 0)) == 3
    assert active_neigbors(grid, (1, 1, 0, 0)) == 5
    assert active_neigbors(grid, (2, 1, 0, 0)) == 3
    assert active_neigbors(grid, (0, 2, 0, 0)) == 1
    assert active_neigbors(grid, (1, 2, 0, 0)) == 3
    assert active_neigbors(grid, (2, 2, 0, 0)) == 2

    assert active_neigbors(grid, (0, 0, 1, 0)) == 1
    assert active_neigbors(grid, (1, 0, 1, 0)) == 2
    assert active_neigbors(grid, (2, 0, 1, 0)) == 2
    assert active_neigbors(grid, (0, 1, 1, 0)) == 3
    assert active_neigbors(grid, (1, 1, 1, 0)) == 5
    assert active_neigbors(grid, (2, 1, 1, 0)) == 4
    assert active_neigbors(grid, (0, 2, 1, 0)) == 2
    assert active_neigbors(grid, (1, 2, 1, 0)) == 4
    assert active_neigbors(grid, (2, 2, 1, 0)) == 3

    assert active_neigbors(grid, (0, 0, -1, 0)) == 1
    assert active_neigbors(grid, (1, 0, -1, 0)) == 2
    assert active_neigbors(grid, (2, 0, -1, 0)) == 2
    assert active_neigbors(grid, (0, 1, -1, 0)) == 3
    assert active_neigbors(grid, (1, 1, -1, 0)) == 5
    assert active_neigbors(grid, (2, 1, -1, 0)) == 4
    assert active_neigbors(grid, (0, 2, -1, 0)) == 2
    assert active_neigbors(grid, (1, 2, -1, 0)) == 4
    assert active_neigbors(grid, (2, 2, -1, 0)) == 3

    for i in range(6):
        print()
        print('Cycle', i)
        print('================================================================================')
        print_grid(grid)
        grid = play_grid(grid)

    with open('input.txt') as f:
        grid = read_grid(f, 4)

    for i in range(6):
        print()
        print('Cycle', i)
        print('================================================================================')
        print_grid(grid)
        grid = play_grid(grid)

    print(sum((1 for cell in grid.values() if cell == '#')))


if __name__ == '__main__':
    main()
