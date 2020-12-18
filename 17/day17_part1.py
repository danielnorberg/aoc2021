import sys


def shape(grid):
    shape = [[sys.maxsize, -sys.maxsize] for i in range(3)]
    for point in grid.keys():
        for s, v in zip(shape, point):
            s[0] = min(s[0], v)
            s[1] = max(s[1], v + 1)
    return shape


def get_cell(grid, x, y, z):
    return grid.get((x, y, z), '.')


def put_cell(grid, x, y, z, cell):
    if cell == '.':
        grid.pop((x, y, z), None)
    else:
        grid[(x, y, z)] = cell


def print_grid(grid):
    ds = shape(grid)
    print('shape: {}'.format(ds))
    xs, ys, zs = ds
    for z in range(*zs):
        print()
        print('z={}'.format(z))
        for y in range(*ys):
            row = [get_cell(grid, x, y, z) for x in range(*xs)]
            print("".join(row))


def read_grid(f):
    grid = {}
    for y, row in enumerate(f):
        for x, cell in enumerate(row.strip()):
            put_cell(grid, x, y, 0, cell)
    return grid


def expanded_shape(grid):
    ds = shape(grid)
    for d in ds:
        d[0] -= 1
        d[1] += 1
    return ds


def neigbors(grid, cx, cy, cz):
    for dz in (-1, 0, 1):
        z = cz + dz
        for dy in (-1, 0, 1):
            y = cy + dy
            for dx in (-1, 0, 1):
                if dz == dx == dy == 0:
                    continue
                x = cx + dx
                yield get_cell(grid, x, y, z)


def active_neigbors(grid, x, y, z):
    return sum(1 for cell in neigbors(grid, x, y, z) if cell == '#')


def play_grid(grid):
    new_grid = {}
    xs, ys, zs = expanded_shape(grid)
    for z in range(*zs):
        for y in range(*ys):
            for x in range(*xs):
                cell = get_cell(grid, x, y, z)
                active = active_neigbors(grid, x, y, z)
                if cell == '#' and active not in (2, 3):
                    put_cell(new_grid, x, y, z, '.')
                elif cell == '.' and active == 3:
                    put_cell(new_grid, x, y, z, '#')
                else:
                    put_cell(new_grid, x, y, z, cell)
    return new_grid


def main():
    with open('sample_input.txt') as f:
        grid = read_grid(f)

    assert active_neigbors(grid, 0, 0, 0) == 1
    assert active_neigbors(grid, 1, 0, 0) == 1
    assert active_neigbors(grid, 2, 0, 0) == 2
    assert active_neigbors(grid, 0, 1, 0) == 3
    assert active_neigbors(grid, 1, 1, 0) == 5
    assert active_neigbors(grid, 2, 1, 0) == 3
    assert active_neigbors(grid, 0, 2, 0) == 1
    assert active_neigbors(grid, 1, 2, 0) == 3
    assert active_neigbors(grid, 2, 2, 0) == 2

    assert active_neigbors(grid, 0, 0, 1) == 1
    assert active_neigbors(grid, 1, 0, 1) == 2
    assert active_neigbors(grid, 2, 0, 1) == 2
    assert active_neigbors(grid, 0, 1, 1) == 3
    assert active_neigbors(grid, 1, 1, 1) == 5
    assert active_neigbors(grid, 2, 1, 1) == 4
    assert active_neigbors(grid, 0, 2, 1) == 2
    assert active_neigbors(grid, 1, 2, 1) == 4
    assert active_neigbors(grid, 2, 2, 1) == 3

    assert active_neigbors(grid, 0, 0, -1) == 1
    assert active_neigbors(grid, 1, 0, -1) == 2
    assert active_neigbors(grid, 2, 0, -1) == 2
    assert active_neigbors(grid, 0, 1, -1) == 3
    assert active_neigbors(grid, 1, 1, -1) == 5
    assert active_neigbors(grid, 2, 1, -1) == 4
    assert active_neigbors(grid, 0, 2, -1) == 2
    assert active_neigbors(grid, 1, 2, -1) == 4
    assert active_neigbors(grid, 2, 2, -1) == 3

    for i in range(6):
        print()
        print('Cycle', i)
        print('================================================================================')
        print_grid(grid)
        grid = play_grid(grid)

    with open('input.txt') as f:
        grid = read_grid(f)

    for i in range(6):
        print()
        print('Cycle', i)
        print('================================================================================')
        print_grid(grid)
        grid = play_grid(grid)

    print(sum((1 for cell in grid.values() if cell == '#')))


if __name__ == '__main__':
    main()
