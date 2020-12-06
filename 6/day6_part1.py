from itertools import chain


def main():
    with open('sample_input.txt') as input_f, open('sample_output.txt') as output_f:
        groups = input_f.read().split('\n\n')
        sum = 0
        for group, count_s in zip(groups, output_f):
            count = int(count_s)
            qs = set(chain(*group.replace(' ', '').replace('\n', '')))
            sum += len(qs)
            assert len(qs) == count
        assert sum == 11

    with open('input.txt') as f:
        sum = 0
        groups = f.read().split('\n\n')
        for group in groups:
            qs = set(chain(*group.replace(' ', '').replace('\n', '')))
            sum += len(qs)
        print(sum)


if __name__ == '__main__':
    main()
