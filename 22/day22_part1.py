from collections import deque


def main():
    with open('sample_input.txt') as f:
        play_game(f)
    with open('input.txt') as f:
        play_game(f)


def play_game(f):
    p1, p2 = f.read().split('\n\n')
    p1, p2 = [deque(map(int, p.splitlines()[1:])) for p in (p1, p2)]
    print(p1, p2)
    i = 1
    while p1 and p2:
        print('-- Round {} --'.format(i))
        print("Player 1's deck:", ", ".join(map(str, p1)))
        print("Player 2's deck:", ", ".join(map(str, p2)))
        c1 = p1.popleft()
        c2 = p2.popleft()
        print('Player 1 plays: {}'.format(c1))
        print('Player 2 plays: {}'.format(c2))
        if c1 > c2:
            print('Player 1 wins the round!')
            p1.append(c1)
            p1.append(c2)
        else:
            print('Player 2 wins the round!')
            p2.append(c2)
            p2.append(c1)
        i += 1
        print()
    print('== Post-game results ==')
    print("Player 1's deck:", ", ".join(map(str, p1)))
    print("Player 2's deck:", ", ".join(map(str, p2)))
    winning_deck = p1 or p2
    winning_score = sum(i * c for i, c in enumerate(reversed(winning_deck), start=1))
    print('Winning score: {}'.format(winning_score))


if __name__ == '__main__':
    main()
