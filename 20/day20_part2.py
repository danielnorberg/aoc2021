from enum import Enum
from itertools import product


class Flips(Enum):
    NONE = 1
    HORIZONTAL = 2
    VERTICAL = 3


class Rotations(Enum):
    R0 = 1
    R90 = 2
    R180 = 3
    R270 = 4


def parse_tile(s):
    id_text, tile_text = s.split(':', 2)
    id = int(id_text.split()[1])
    rows = tile_text.strip().split()
    return id, rows


def print_tile(tile, tr=(Flips.NONE, Rotations.R0)):
    n = len(tile[0])
    for y in range(n):
        print("".join(get_transformed(tile, tr, y, x) for x in range(n)))


def get_transformed(t, tr, y, x):
    ty, tx = transformed_coord(t, tr, y, x)
    return t[ty][tx]


def set_transformed(t, tr, y, x, v):
    ty, tx = transformed_coord(t, tr, y, x)
    t[ty][tx] = v


def transformed_coord(t, tr, y, x):
    n = len(t[0])
    f, r = tr
    if f == Flips.HORIZONTAL:
        x = n - x - 1
    elif f == Flips.VERTICAL:
        y = n - y - 1
    else:
        assert f == Flips.NONE
    if r == Rotations.R0:
        return y, x
    elif r == Rotations.R90:
        return x, n - y - 1
    elif r == Rotations.R180:
        return n - y - 1, n - x - 1
    elif r == Rotations.R270:
        return n - x - 1, y
    else:
        raise False


def shape(o):
    w = max(len(r) for r in o)
    h = len(o)
    return w, h


def match(pattern, map, tr, y, x):
    for py, row in enumerate(pattern):
        for px, p in enumerate(row):
            if p == '#':
                c = get_transformed(map, tr, y + py, x + px)
                if p != c:
                    return False
    return True


def find(map, pattern):
    n = len(map)
    pw, ph = shape(pattern)
    sh = n - ph + 1
    sw = n - pw + 1
    assert all(n == len(r) for r in map)
    for tr in product(Flips, Rotations):
        for y in range(sh):
            for x in range(sw):
                if match(pattern, map, tr, y, x):
                    yield tr, y, x


def mark(map, pattern, tr, y, x):
    for py, row in enumerate(pattern):
        for px, p in enumerate(row):
            if p == '#':
                set_transformed(map, tr, y + py, x + px, 'O')


def main():
    with open('sea_monster.txt') as mf:
        monster = [s.replace('\n', '') for s in mf]
        assert shape(monster) == (20, 3)

    with open('sample_map.txt') as f:
        compute_roughness(f, monster)

    with open('map.txt') as f:
        compute_roughness(f, monster)


def compute_roughness(f, monster):
    map = [list(s.strip()) for s in f]
    w, h = shape(map)
    assert w == h
    trs = set()
    for tr, y, x in find(map, monster):
        trs.add(tr)
        print(tr, y, x)
        mark(map, monster, tr, y, x)

    print()
    for tr in trs:
        for y in range(w):
            print("".join(get_transformed(map, tr, y, x) for x in range(w)))

    print()
    roughness = sum(c == '#' for row in map for c in row)
    print('roughness:', roughness)


if __name__ == '__main__':
    main()
