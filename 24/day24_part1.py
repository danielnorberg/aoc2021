def flip(floor, path):
    k = walk(path)
    if k in floor:
        floor.discard(k)
    else:
        floor.add(k)


def walk(path):
    c, r = 0, 0
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


def main():
    with open('sample_input.txt') as f:
        floor = lay(f)
        print(len(floor))
    with open('input.txt') as f:
        floor = lay(f)
        print(len(floor))


def lay(f):
    floor = set()
    for l in f:
        path = l.strip()
        flip(floor, path)
    return floor


if __name__ == '__main__':
    main()
