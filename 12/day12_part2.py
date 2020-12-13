def rotate(x, y, t):
    t = t % 360
    if t == 90:
        return -y, x
    if t == 180:
        return -x, -y
    if t == 270:
        return y, -x
    assert False


ACTIONS = {
    'n': lambda v, x, y, sx, sy: (x    , y + v     , sx          , sy          ),
    's': lambda v, x, y, sx, sy: (x    , y - v     , sx          , sy          ),
    'e': lambda v, x, y, sx, sy: (x + v, y         , sx          , sy          ),
    'w': lambda v, x, y, sx, sy: (x - v, y         , sx          , sy          ),
    'f': lambda v, x, y, sx, sy: (x    , y         , sx + (x * v), sy + (y * v)),
    'l': lambda v, x, y, sx, sy: (*rotate(x, y,  v), sx          , sy          ),
    'r': lambda v, x, y, sx, sy: (*rotate(x, y, -v), sx          , sy          ),
}


def navigate(f):
    x, y = 10, 1
    sx, sy = 0, 0
    for l in f:
        action = l[0].lower()
        value = int(l[1:])
        x, y, sx, sy = ACTIONS[action](value, x, y, sx, sy)
    print(abs(sx) + abs(sy))


def main():
    with open('sample_input.txt') as f:
        navigate(f)
    with open('input.txt') as f:
        navigate(f)


if __name__ == '__main__':
    main()
