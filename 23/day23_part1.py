from collections import deque


def play(start_cups, n):
    cups = deque(int(c) for c in start_cups)
    for i in range(n):
        current = cups[0]
        cups.rotate(-1)
        removed = (cups.popleft(), cups.popleft(), cups.popleft())
        cups.rotate(1)
        destination_label = current - 1
        while destination_label in removed:
            destination_label -= 1
        if destination_label not in cups:
            destination_label = max(cups)
        destination = cups.index(destination_label)
        cups.rotate(-(destination + 1))
        cups.extendleft(reversed(removed))
        cups.rotate(destination)
    cups.rotate(-cups.index(1))
    cups.popleft()
    result = "".join(map(str, cups))
    return result


def main():
    print(play('389125467', 10))
    print(play('389125467', 100))
    print(play('186524973', 100))


if __name__ == '__main__':
    main()
