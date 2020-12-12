def count_adjacent_occupied(grid, y, x):
    return grid[y - 1][x - 1:x + 2].count('#') + \
           grid[y + 0][x - 1:x + 2:2].count('#') + \
           grid[y + 1][x - 1:x + 2].count('#')


def compute_occupied(f):
    grid1 = [[]] + [list([' '] + list(l.strip()) + [' ']) for l in f] + [[]]
    grid1[0] = [' ' for _ in grid1[1]]
    grid1[-1] = [' ' for _ in grid1[1]]
    grid2 = [[c for c in r] for r in grid1]
    changed = True
    while changed:
        changed = False
        for y in range(1, len(grid1) - 1):
            for x in range(1, len(grid1[1]) - 1):
                s = grid1[y][x]
                if s == '.':
                    continue
                n = count_adjacent_occupied(grid1, y, x)
                if s == 'L' and n == 0:
                    grid2[y][x] = '#'
                    changed = True
                elif s == '#' and n >= 4:
                    grid2[y][x] = 'L'
                    changed = True
                else:
                    grid2[y][x] = grid1[y][x]
        # for r in grid2:
        #     print("".join(r))
        # print()
        grid1, grid2 = grid2, grid1
    occupied = sum(r.count('#') for r in grid1)
    return occupied


def main():
    with open('sample_input.txt') as f:
        print(compute_occupied(f))
    with open('input.txt') as f:
        print(compute_occupied(f))


if __name__ == '__main__':
    main()
