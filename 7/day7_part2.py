import re

BAGS_PATTERN = re.compile(r'(\d+)\s(\w+\s+\w+)\s+bags?')


def graph_weight(edges, node):
    # Assuming no loops here, and revisiting is ok!
    neighbors = edges.get(node, set())
    w = sum(nn * graph_weight(edges, neighbor) for (neighbor, nn) in neighbors)
    return 1 + w


def create_graph(f):
    # bag -> contains -> (bag, n)
    edges = {}
    for line in f:
        if 'no other bags' in line:
            continue
        container_bag, contents = line.split(' bags contain ')
        contained_bags = [(m.group(2), int(m.group(1))) for m in (BAGS_PATTERN.match(s) for s in contents.split(', '))]
        edges.setdefault(container_bag, []).extend(contained_bags)
    return edges


def main():
    with open('sample_input_2.txt') as f:
        edges = create_graph(f)
    print(graph_weight(edges, 'shiny gold') - 1)

    with open('input.txt') as f:
        edges = create_graph(f)
    print(graph_weight(edges, 'shiny gold') - 1)


if __name__ == '__main__':
    main()
