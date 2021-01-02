from collections import deque
from itertools import count, islice


def play_game(f):
    p1, p2 = f.read().split('\n\n')
    p1, p2 = [deque(map(int, p.splitlines()[1:])) for p in (p1, p2)]
    winner, p1, p2 = play_game0(p1, p2, [0])
    print('== Post-game results ==')
    print("Player 1's deck:", ", ".join(map(str, p1)))
    print("Player 2's deck:", ", ".join(map(str, p2)))
    winning_deck = p1 or p2
    winning_score = sum(i * c for i, c in enumerate(reversed(winning_deck), start=1))
    print('Winning score: {}'.format(winning_score))


def play_game0(p1, p2, game_counter):
    game_counter[0] += 1
    game = game_counter[0]
    print()
    print('=== Game {} ==='.format(game))
    print()
    i = 1
    previous_rounds = set()
    for round in count(1):
        key = (tuple(p1), tuple(p2))
        if key in previous_rounds:
            print('Previously observed round, player 1 wins game', game)
            return 1, p1, p2
        previous_rounds.add(key)
        print('-- Round {} (Game {}) --'.format(i, game))
        print("Player 1's deck:", ", ".join(map(str, p1)))
        print("Player 2's deck:", ", ".join(map(str, p2)))
        c1 = p1.popleft()
        c2 = p2.popleft()
        print('Player 1 plays: {}'.format(c1))
        print('Player 2 plays: {}'.format(c2))
        if len(p1) >= c1 and len(p2) >= c2:
            print('Playing a sub-game to determine the winner...')
            round_winner, _, _ = play_game0(deque(islice(p1, 0, c1)), deque(islice(p2, 0, c2)), game_counter)
            print()
            print('...anyway, back to game {}.'.format(game))
        else:
            if c1 > c2:
                round_winner = 1
            else:
                round_winner = 2
            i += 1
        print('Player {} wins round {} of game {}!'.format(round_winner, round, game))
        if round_winner == 1:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
        print()
        if not p1 or not p2:
            winner = 1 if p1 else 2
            print('The winner of game {} is player {}!'.format(game, winner))
            return winner, p1, p2


def main():
    with open('sample_input.txt') as f:
        play_game(f)
    with open('input.txt') as f:
        play_game(f)


if __name__ == '__main__':
    main()
