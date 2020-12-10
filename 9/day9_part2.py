def find_sum_series(f, n):
    numbers = [int(l) for l in f]
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if sum(numbers[i:j]) == n:
                return numbers[i:j]
    assert False


def main():
    with open('sample_input.txt') as f:
        print(find_sum_series(f, 127))
    with open('input.txt') as f:
        series = find_sum_series(f, 21806024)
        print(series)
        print(min(series) + max(series))


if __name__ == '__main__':
    main()
