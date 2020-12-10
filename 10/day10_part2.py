def find_paths(adapters, visited, node, target, cache):
    visited.add(node)
    if node == target:
        visited.remove(node)
        return 1
    n = 0
    for next_node in adapters[node]:
        if next_node in visited:
            continue
        if next_node in cache:
            p = cache[next_node]
        else:
            p = find_paths(adapters, visited, next_node, target, cache)
            cache[next_node] = p
        n += p
    visited.remove(node)
    return n


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
    paths = find_paths(adapters, set(),  0, device, {})
    print("paths:", paths)


def main():
    with open('sample_input.txt') as f:
        test_adapters(f)
    with open('input.txt') as f:
        test_adapters(f)


if __name__ == '__main__':
    main()
