def sum_qs(f):
    return sum(len(set.intersection(*(map(set, g.split()))))
               for g in f.read().split('\n\n'))


def main():
    with open('sample_input.txt') as f:
        assert sum_qs(f) == 6

    with open('input.txt') as f:
        print(sum_qs(f))


if __name__ == '__main__':
    main()
