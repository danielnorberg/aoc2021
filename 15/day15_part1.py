from collections import deque

example_inputs = [
    ([0, 3, 6], 10, 0),
    ([0, 3, 6], 2020, 436),
    ([1, 3, 2], 2020, 1),
    ([2, 1, 3], 2020, 10),
    ([1, 2, 3], 2020, 27),
    ([2, 3, 1], 2020, 78),
    ([3, 2, 1], 2020, 438),
    ([3, 1, 2], 2020, 1836),
]

problem_input = [10, 16, 6, 0, 1, 17]


# O(n^2)
def play(numbers, n):
    numbers = deque(numbers)
    n -= len(numbers)
    for i in range(n):
        last = numbers[-1]
        age = None
        for j in reversed(range(len(numbers) - 1)):
            if numbers[j] == last:
                age = len(numbers) - j - 1
                break
        age = age or 0
        numbers.append(age)
    return age


def main():
    for start, n, expected in example_inputs:
        assert play(start, n) == expected
    print(play(problem_input, 2020))


if __name__ == '__main__':
    main()
