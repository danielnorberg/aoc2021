from itertools import islice, takewhile


class Cup:
    __slots__ = 'next', 'label'

    def __init__(self, label):
        self.label = label
        self.next = None

    def __repr__(self):
        return '{} {}'.format(self.label, '->' if self.next is not None else ')')


def remove(head, n):
    cur = head
    prev = None
    for i in range(n):
        prev = cur
        cur = head.next
    prev.next = cur.next
    cur.next = None
    return cur


def insert(head, tail, cup):
    cup.next = head.next
    head.next = cup
    if tail == head:
        tail = cup
        assert tail.next is None
    return cup, tail


def enumerate_labels(head):
    head = head.next
    while head:
        yield head.label
        head = head.next


def print_cups(head):
    return " ".join(str(label) for label in enumerate_labels(head))


def assert_no_loop(head):
    visited = set()
    while head:
        if head in visited:
            assert False
        visited.add(head)
        head = head.next


def assert_has_all_labels(head, labels):
    if set(labels) != set(enumerate_labels(head)):
        raise False


def pop(head):
    cup = head.next
    head.next = cup.next
    cup.next = None
    return cup


def play(labeling, number_cups, moves):
    labels = [int(c) for c in labeling]
    for label in range(max(labels) + 1, number_cups + 1):
        labels.append(label)

    head = Cup(None)
    index = {}
    tail = head
    for label in labels:
        cup = Cup(label)
        index[label] = cup
        tail.next = cup
        tail = cup

    min_label = min(labels)
    max_label = max(labels)

    # assert_no_loop(head)

    for i in range(moves):
        # print(print_cups(head))
        # assert_has_all_labels(head, labels)
        current = pop(head)
        removed_cups = (pop(head), pop(head), pop(head))
        removed_labels = tuple(cup.label for cup in removed_cups)
        # assert_no_loop(head)
        # assert_has_all_labels(head, set(labels) - set(removed_labels))

        destination_label = current.label - 1
        if destination_label < min_label:
            destination_label = max_label
        while destination_label in removed_labels:
            destination_label -= 1
            if destination_label < min_label:
                destination_label = max_label

        destination = index[destination_label]
        for removed_cup in removed_cups:
            destination, tail = insert(destination, tail, removed_cup)
        # assert_no_loop(head)
        # assert_has_all_labels(head, labels)

        # Move first cup to last
        # assert tail.next == None
        tail.next = current
        tail = current
        assert tail.next is None
        # assert_no_loop(head)
        # assert_has_all_labels(head, labels)

        if i % 100000 == 0:
            print('{:.1%}'.format(i / moves))

    # Yield cups after 1
    yield from enumerate_labels(index[1])
    yield from takewhile(lambda l: l != 1, enumerate_labels(head))


def main():
    # part 1
    assert "".join(str(c) for c in play('389125467', 9, 10)) == '92658374'
    assert "".join(str(c) for c in play('389125467', 9, 100)) == '67384529'
    assert "".join(str(c) for c in play('186524973', 9, 100)) == '45983627'

    # part 2
    assert tuple(islice(play('389125467', 10 ** 6, 10 ** 7), 2)) == (934001, 159792)

    cups = tuple(islice(play('186524973', 10 ** 6, 10 ** 7), 2))
    assert cups[0] * cups[1] == 111080192688


if __name__ == '__main__':
    main()
