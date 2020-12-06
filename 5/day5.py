def parse_binary(s, zero, one):
    return int(s.replace(zero, '0').replace(one, '1'), 2)


def seat(boarding_pass):
    r = parse_binary(boarding_pass[:7], 'F', 'B')
    c = parse_binary(boarding_pass[7:], 'L', 'R')
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
