from collections import deque


def find_path_cover(adapters, remaining, path, node):
    path.append(node)
    remaining.remove(node)
    if not remaining:
        return path
    for next_node in adapters[node]:
        if find_path_cover(adapters, remaining, path, next_node):
            return path
    path.pop()
    remaining.add(node)
    return False


def find_deltas(path):
    deltas = {}
    path = list(path)
    for a, b in zip(path[:-1], path[1:]):
        d = b - a
        deltas[d] = deltas.get(d, 0) + 1
    return deltas


def test_adapters(f):
    adapters = {int(line.strip()): [] for line in f}
    device = max(adapters) + 3
    adapters[0] = []
    adapters[device] = []
    for adapter in adapters:
        for dj in (1, 2, 3):
            next_adapter = adapter + dj
            if next_adapter in adapters:
                adapters[adapter].append(next_adapter)
    print(adapters)
    path = find_path_cover(adapters, set(adapters), deque(), 0)
    print(path)
    deltas = find_deltas(path)
    print(deltas, "result:", deltas[1] * deltas[3])


def main():
    with open('sample_input.txt') as f:
        test_adapters(f)
    print()
    with open('input.txt') as f:
        test_adapters(f)


if __name__ == '__main__':
    main()
