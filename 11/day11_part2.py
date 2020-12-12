def count_visible_occupied(grid, y, x, height, width):
    n = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            py = y
            px = x
            while True:
                py += dy
                px += dx
                if py < 0 or py >= height or px < 0 or px >= width:
                    break
                s = grid[py][px]
                if s == '.':
                    continue
                if s == '#':
                    n += 1
                break
    return n


def compute_occupied(f):
    grid1 = [list(l.strip()) for l in f]
    grid2 = [[c for c in r] for r in grid1]
    height = len(grid1)
    width = len(grid1[0])
    changed = True
    while changed:
        # for r in grid1:
        #     print("".join(r))
        # print()
        changed = False
        for y in range(height):
            for x in range(width):
                s = grid1[y][x]
                if s == '.':
                    continue
                n = count_visible_occupied(grid1, y, x, height, width)
                if s == 'L' and n == 0:
                    grid2[y][x] = '#'
                    changed = True
                elif s == '#' and n >= 5:
                    grid2[y][x] = 'L'
                    changed = True
                else:
                    grid2[y][x] = grid1[y][x]
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
