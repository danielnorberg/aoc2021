from collections import deque


def find_sum(ns, x):
    for i in range(len(ns)):
        n = ns[i]
        comp = x - n
        for j in range(i + 1, len(ns)):
            if ns[j] == comp:
                return True
    return False


def find_mismatch(f, window_length):
    window = deque()
    for i in range(window_length):
        n = int(f.readline().strip())
        window.append(n)
    for l in f:
        n = int(l)
        if not find_sum(window, n):
            return n
        window.append(n)
        window.popleft()


def main():
    with open('sample_input.txt') as f:
        print(find_mismatch(f, 5))
    with open('input.txt') as f:
        print(find_mismatch(f, 25))


if __name__ == '__main__':
    main()
