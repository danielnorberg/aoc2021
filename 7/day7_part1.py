import re

from collections import deque

BAGS_PATTERN = re.compile(r'\d+\s(\w+\s+\w+)\s+bags?')


def graph_size(edges, root):
    visited = {root}
    q = deque(edges.get(root, set()))
    while len(q) != 0:
        node = q.pop()
        visited.add(node)
        neighbors = edges.get(node, set())
        q.extend(neighbors - visited)
    return len(visited)


def create_graph(f):
    # key -> contained_by -> value
    edges = {}
    for line in f:
        if 'no other bags' in line:
            continue
        container_bag, contents = line.split(' bags contain ')
        contained_bags = [BAGS_PATTERN.match(s).group(1) for s in contents.split(', ')]
        for bag in contained_bags:
            edges.setdefault(bag, set()).add(container_bag)
    return edges


def main():
    with open('sample_input.txt') as f:
        edges = create_graph(f)
    print(graph_size(edges, 'shiny gold') - 1)

    with open('input.txt') as f:
        edges = create_graph(f)
    print(graph_size(edges, 'shiny gold') - 1)


if __name__ == '__main__':
    main()
