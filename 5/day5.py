def binary_partition(path, lower_c, upper_c):
    n = len(path)
    k = 1 << (n - 1)
    m = 1 << (n - 1)
    for c in path[:-1]:
        m = m >> 1
        if c == lower_c:
            k -= m
        elif c == upper_c:
            k += m
        else:
            assert c in (lower_c, upper_c)
    c = path[-1]
    if c == lower_c:
        k -= 1
    return k


def seat(boarding_pass):
    r = binary_partition(boarding_pass[:7], 'F', 'B')
    c = binary_partition(boarding_pass[7:], 'L', 'R')
    sid = r * 8 + c
    return r, c, sid


def main():
    with open('sample_input.txt') as input_f:
        with open('sample_output.txt') as output_f:
            for il, ol in zip(input_f, output_f):
                er, ec, esid = [int(s) for s in ol.split(' ')]
                r, c, sid = seat(il.strip())
                assert (r, c, sid) == (er, ec, esid)

    with open('input.txt') as f:
        sids = sorted(seat(l.strip())[2] for l in f)

    print('highest seat id: {}'.format(sids[-1]))

    my_sid = None
    sids = sorted(sids)
    for sid, next_sid in zip(sids[:-1], sids[1:]):
        if sid + 2 == next_sid:
            my_sid = sid + 1
            break

    print('my sid: {}'.format(my_sid))


if __name__ == '__main__':
    main()
