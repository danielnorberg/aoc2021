from itertools import islice

from sortedcontainers import SortedDict


def play(labeling, number_cups, moves):
    labels = [int(c) for c in labeling]
    max_label = max(labels)
    labels.extend(range(max_label + 1, number_cups + 1))
    index = {l: tuple(int(c) for c in '{:07}'.format(i)) for i, l in enumerate(labels)}
    cups = SortedDict((k, l) for l, k in index.items())
    for label, key in index.items():
        v = cups[key]
        assert v == label, "{} != {}".format(v, label)
    min_label = min(labels)
    max_label = max(labels)
    del labels

    for i in range(moves):
        current_key, current_cup = cups.peekitem(0)
        removed_cups = (cups.popitem(1)[1], cups.popitem(1)[1], cups.popitem(1)[1])

        # Look up destination label
        destination_label = current_cup - 1
        if destination_label < min_label:
            destination_label = max_label
        while destination_label in removed_cups:
            destination_label -= 1
            if destination_label < min_label:
                destination_label = max_label

        # decrement right key
        # 0 8
        # 0 8 -3  <--
        # 0 8 -2  <--
        # 0 8 -1  <--
        # 0 8 0

        # Increment left key
        # 0 1
        # 0 2    <--
        # 0 3    <--
        # 0 4    <--
        # 0 5

        # extend left key
        # 0 1
        # 0 1 0   <--
        # 0 1 1   <--
        # 0 1 2   <--
        # 0 2

        # increment prev suffix
        # 0 1 2
        # 0 1 3   <--
        # 0 1 4   <--
        # 0 1 5   <--
        # 0 2

        # Compute the appropriate keys to insert into the sorted list right after the "destination" cup
        left_key = index[destination_label]
        left_index = cups.index(left_key)
        right_index = left_index + 1
        if right_index == len(cups):
            # destination is at end of list - increment left key
            insert_keys = [left_key[:-1] + (left_key[-1] + d,) for d in (1, 2, 3)]
        else:
            # insert between two cups
            right_key = cups.peekitem(left_index + 1)[0]
            if len(left_key) < len(right_key):
                # left key is shorter, decrement right key
                insert_keys = [right_key[:-1] + (right_key[:-1] + d,) for d in (-3, -2, -1)]
            elif len(left_key) == len(right_key):
                # Keys are same length
                if left_key[:-1] == right_key[:-1]:
                    # Keys have same prefix
                    ls = left_key[-1]
                    rs = right_key[-1]
                    if rs - ls < 4:
                        # There is not space enough between the two key vectors to simply increment,
                        # create new keys by extending the left one
                        insert_keys = [left_key + (d,) for d in (0, 1, 2)]
                    else:
                        # There is space enough between the two key vectors - increment the left key
                        insert_keys = [left_key[:-1] + (left_key[-1] + d,) for d in (1, 2, 3)]
                else:
                    # Keys have differing prefix - increment the left key
                    insert_keys = [left_key[:-1] + (left_key[-1] + d,) for d in (1, 2, 3)]
            elif len(left_key) > len(right_key):
                # Keys have different length - increment the left key
                insert_keys = [left_key[:-1] + (left_key[-1] + d,) for d in (1, 2, 3)]
            else:
                assert False

        for removed_cup, key in zip(removed_cups, insert_keys):
            cups[key] = removed_cup
            index[removed_cup] = key

        # Move first cup to last
        cups.popitem(0)
        last_key = cups.peekitem(len(cups) - 1)[0]
        next_last_key = last_key[:-1] + (last_key[-1] + 1,)
        cups[next_last_key] = current_cup
        index[current_cup] = next_last_key

    one_key = index[1]
    one_index = cups.index(one_key)
    for i in range(one_index + 1, len(cups)):
        yield cups.peekitem(i)[1]
    for i in range(0, one_index):
        yield cups.peekitem(i)[1]


def main():
    # part 1
    assert "".join(str(c) for c in play('389125467', 9, 10)) == '92658374'
    assert "".join(str(c) for c in play('389125467', 9, 100)) == '67384529'
    assert "".join(str(c) for c in play('186524973', 9, 100)) == '45983627'

    # part 2
    assert tuple(islice(play('389125467', 10 ** 6, 10 ** 7), 2)) == (934001, 159792)

    cups = tuple(islice(play('186524973', 10 ** 6, 10 ** 7), 2))
    print(cups)


if __name__ == '__main__':
    main()
