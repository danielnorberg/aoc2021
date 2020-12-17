example_inputs = [
    ([0, 3, 6], 10, 0),
    ([0, 3, 6], 2020, 436),
    ([1, 3, 2], 2020, 1),
    ([2, 1, 3], 2020, 10),
    ([1, 2, 3], 2020, 27),
    ([2, 3, 1], 2020, 78),
    ([3, 2, 1], 2020, 438),
    ([3, 1, 2], 2020, 1836),

    ([0, 3, 6], 30000000, 175594),
    ([1, 3, 2], 30000000, 2578),
    ([2, 1, 3], 30000000, 3544142),
    ([1, 2, 3], 30000000, 261214),
    ([2, 3, 1], 30000000, 6895259),
    ([3, 2, 1], 30000000, 18),
    ([3, 1, 2], 30000000, 362),
]

problem_input = [10, 16, 6, 0, 1, 17]


# O(n)
def play(numbers, n):
    index = {number: turn for turn, number in enumerate(numbers[:-1])}
    last = numbers[-1]
    for i in range(len(numbers) - 1, n - 1):
        prev = index.get(last, None)
        if prev is None:
            age = 0
        else:
            age = i - prev
        index[last] = i
        last = age
    return age


def main():
    for start, n, expected in example_inputs:
        last = play(start, n)
        print(last)
        assert last == expected

    print()
    print(play(problem_input, 2020))
    print(play(problem_input, 30000000))


if __name__ == '__main__':
    main()
