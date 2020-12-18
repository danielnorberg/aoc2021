example_expressions = [
    ('1 + (2 * 3) + (4 * (5 + 6))', 51),
    ('2 * 3 + (4 * 5)', 46),
    ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
    ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
    ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340),
]


def find_closing_paren(s):
    l = 0
    for i, c in enumerate(s):
        if c == '(':
            l += 1
        elif c == ')':
            l -= 1
        if l == 0:
            return i
    assert False


def read_number(s):
    for i, c in enumerate(s):
        if not c.isdigit():
            return int(s[:i]), s[i:]
    return int(s), ''


def read_operator(s):
    return s[0], s[1:]


def evaluate(s):
    s = s.replace(' ', '')
    r = 0
    op = '+'
    while s:
        # Iterate for +
        if op == '+':
            if s[0] == '(':
                end = find_closing_paren(s)
                v = evaluate(s[1:end].strip())
                s = s[end + 1:].strip()
            else:
                v, s = read_number(s)
            r += v
        # Recurse for *
        elif op == '*':
            r *= evaluate(s)
            s = ''
        else:
            assert False

        if not s:
            break

        # Read next operator
        op, s = read_operator(s)

    return r


if __name__ == '__main__':
    for expression, expected_result in example_expressions:
        assert evaluate(expression) == expected_result

    with open('input.txt') as f:
        r = 0
        for expression in f:
            r += evaluate(expression)
        print(r)
