DIRECTIONS = {
    0:   'e',
    90:  'n',
    180: 'w',
    270: 's',
}

ACTIONS = {
    'n': lambda v, x, y, t: (x    , y + v, t            ),
    's': lambda v, x, y, t: (x    , y - v, t            ),
    'e': lambda v, x, y, t: (x + v, y    , t            ),
    'w': lambda v, x, y, t: (x - v, y    , t            ),
    'l': lambda v, x, y, t: (x    , y    , (t + v) % 360),
    'r': lambda v, x, y, t: (x    , y    , (t - v) % 360),
    'f': lambda v, x, y, t: ACTIONS[DIRECTIONS[t]](v, x, y, t),
}


def navigate(f):
    x, y, t = 0, 0, 0
    for l in f:
        action = l[0].lower()
        value = int(l[1:])
        x, y, t = ACTIONS[action](value, x, y, t)
    print(abs(x) + abs(y))


def main():
    with open('sample_input.txt') as f:
        navigate(f)
    with open('input.txt') as f:
        navigate(f)


if __name__ == '__main__':
    main()
