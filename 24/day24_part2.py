def flip(floor, path):
    k = walk(path)
    if k in floor:
        floor.discard(k)
    else:
        floor.add(k)


def walk(path, origin=(0, 0)):
    c, r = origin
    i = 0
    while i < len(path):

        d = path[i]
        i += 1
        if d in ('s', 'n'):
            assert i < len(path)
            d += path[i]
            i += 1

        if d == 'e':
            c += 1
        elif d == 'se':
            if r % 2 == 1:
                c += 1
            r += 1
        elif d == 'sw':
            if r % 2 == 0:
                c -= 1
            r += 1
        elif d == 'w':
            c -= 1
        elif d == 'nw':
            if r % 2 == 0:
                c -= 1
            r -= 1
        elif d == 'ne':
            if r % 2 == 1:
                c += 1
            r -= 1
        else:
            assert False, d
    k = (c, r)
    return k


assert walk('neneseseww') == (0, 0)
assert walk('esew') == (0, 1)
assert walk('nwwswee') == (0, 0)


def lay(f):
    floor = set()
    for l in f:
        path = l.strip()
        flip(floor, path)
    return floor


DIRECTIONS = ('e', 'se', 'sw', 'w', 'nw', 'ne')


def count_neighbors(f, tile):
    neighbors = set(walk(d, origin=tile) for d in DIRECTIONS)
    return len(neighbors & f)


def gol_round(f):
    nf = set()
    for tile in f:
        neighbors = [walk(d, origin=tile) for d in DIRECTIONS]
        for neighbor in neighbors:
            n = count_neighbors(f, neighbor)
            if neighbor in f:  # black
                if n == 0 or n > 2:
                    pass  # flip to white
                else:
                    nf.add(neighbor)
            else:  # white
                if n == 2:
                    nf.add(neighbor)  # flip to black
    return nf


def gol(floor, n):
    for i in range(n):
        floor = gol_round(floor)
    return floor


def main():
    with open('sample_input.txt') as f:
        floor = lay(f)
        floor = gol(floor, 100)
        print(len(floor))

    with open('input.txt') as f:
        floor = lay(f)
        floor = gol(floor, 100)
        print(len(floor))


if __name__ == '__main__':
    main()
