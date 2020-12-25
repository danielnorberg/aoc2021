from functools import cache, cached_property, reduce
from itertools import permutations, product
from math import sqrt

from enum import Enum
from operator import mul


class Flips(Enum):
    NONE = 1
    HORIZONTAL = 2
    VERTICAL = 3


class Rotations(Enum):
    R0 = 1
    R90 = 2
    R180 = 3
    R270 = 4


def parse_tile(s):
    id_text, tile_text = s.split(':', 2)
    id = int(id_text.split()[1])
    rows = tile_text.strip().split()
    return id, rows


def print_tile(tile, tr=(Flips.NONE, Rotations.R0)):
    n = len(tile[0])
    for y in range(n):
        print("".join(get_transformed(tile, tr, y, x) for x in range(n)))


def get_transformed(t, tr, y, x):
    n = len(t[0])
    f, r = tr
    if f == Flips.HORIZONTAL:
        x = n - x - 1
    elif f == Flips.VERTICAL:
        y = n - y - 1
    else:
        assert f == Flips.NONE
    if r == Rotations.R0:
        return t[y][x]
    elif r == Rotations.R90:
        return t[x][n - y - 1]
    elif r == Rotations.R180:
        return t[n - y - 1][n - x - 1]
    elif r == Rotations.R270:
        return t[n - x - 1][y]
    else:
        raise False


def fit_lr(a, tra, b, trb):
    n = len(a[0])
    for i in range(n):
        ac = get_transformed(a, tra, i, n - 1)
        bc = get_transformed(b, trb, i, 0)
        if ac != bc:
            return False
    return True


def fit_tb(a, tra, b, trb):
    n = len(a[0])
    for i in range(n):
        if get_transformed(a, tra, n - 1, i) != get_transformed(b, trb, 0, i):
            return False
    return True


def tile_borders(tile):
    n = len(tile[0])
    top = tile[0]
    bottom = tile[n - 1]
    right = "".join(tile[y][n - 1] for y in range(n))
    left = "".join(tile[y][0] for y in range(n))
    borders = [top, bottom, right, left]
    borders = borders + [border[::-1] for border in borders]
    return borders


def get_right_border(tile, tr):
    n = len(tile[0])
    return "".join(get_transformed(tile, tr, y, n - 1) for y in range(n))


def get_left_border(tile, tr):
    n = len(tile[0])
    return "".join(get_transformed(tile, tr, y, 0) for y in range(n))


def get_top_border(tile, tr):
    n = len(tile[0])
    return "".join(get_transformed(tile, tr, 0, x) for x in range(n))


def get_bottom_border(tile, tr):
    n = len(tile[0])
    return "".join(get_transformed(tile, tr, n - 1, x) for x in range(n))


class Tiles:

    def __init__(self, s):
        tiles_text = s.strip().split('\n\n')
        self.tiles = dict(parse_tile(s) for s in tiles_text)
        self.d = int(sqrt(len(tiles_text)))
        self.n = len(next(iter(self.tiles.values()))[0])
        self.tile_borders = {tid: tile_borders(tile) for tid, tile in self.tiles.items()}
        self.borders = {}
        self.canonical_borders = {}
        for tid, borders in self.tile_borders.items():
            for border in borders:
                self.borders.setdefault(border, set()).add(tid)
                self.borders.setdefault(border, set()).add(tid)
                canonical_border = min(border, border[::-1])
                self.canonical_borders.setdefault(canonical_border, set()).add(tid)

        unique_borders = {}
        for border, tids in self.canonical_borders.items():
            if len(tids) == 1:
                tid = next(iter(tids))
                unique_borders[tid] = unique_borders.get(tid, 0) + 1
        self.corner_tiles = [tid for tid, n in unique_borders.items() if n == 2]

        print()
        print('corner tiles: {}'.format(self.corner_tiles))

    def print(self):
        print('Grid: {}x{}'.format(self.d, self.d))
        for id, tile in self.tiles.items():
            print()
            print('Tile {}:'.format(id))
            print_tile(tile)

    def print_board(self, board):
        def g(by, bx, y, x):
            bc = (bx, by)
            if bc not in board:
                return ' '
            tid, tr = board[bc]
            tile = self.tiles[tid]
            return get_transformed(tile, tr, y, x)

        for by in range(self.d):
            for y in range(self.n):
                rs = ["".join(g(by, bx, y, x) for x in range(self.n)) for bx in range(self.d)]
                print(*rs)
            print()

        for by in range(self.d):
            print(" ".join(str(board[(bx, by)][0]) for bx in range(self.d)))

    def print_map(self, board):
        def g(by, bx, y, x):
            bc = (bx, by)
            if bc not in board:
                return ' '
            tid, tr = board[bc]
            tile = self.tiles[tid]
            return get_transformed(tile, tr, y, x)

        rows = []
        for by in range(self.d):
            for y in range(1, self.n - 1):
                row = []
                for bx in range(self.d):
                    for x in range(1, self.n - 1):
                        row.append(g(by, bx, y, x))
                rows.append("".join(row))

        expected_width = self.d * (self.n - 2)
        assert len(rows) == expected_width
        assert all(len(row) == expected_width for row in rows)
        print("\n".join(rows))


    @cache
    def fit_lr(self, a, ra, b, rb):
        return fit_lr(self.tiles[a], ra, self.tiles[b], rb)

    @cache
    def fit_tb(self, a, ra, b, rb):
        return fit_tb(self.tiles[a], ra, self.tiles[b], rb)

    @property
    def ids(self):
        return self.tiles.keys()

    def find_fit(self):
        board = {}
        placed = set()
        for top_left in self.corner_tiles:
            for tr in product(Flips, Rotations):
                board[(0, 0)] = (top_left, tr)
                placed.add(top_left)
                fit_board = self._find_fit(board, placed, 1, 0, 1)
                if fit_board:
                    return fit_board
                placed.remove(top_left)

    def _find_fit(self, board, placed, i, y, x):
        # No more tiles? Done!
        if i == len(self.tiles):
            return dict(board)
        # Choose a tile with a border that might match the top and left neighbor
        candidates = []
        left_border = None
        top_border = None
        if x > 0:
            left_tile, left_tile_tr = board[(x - 1, y)]
            left_border = self.get_right_border(left_tile, left_tile_tr)
            left_candidates = self.borders[left_border]
            candidates.append(left_candidates)
        if y > 0:
            top_tile, top_tile_tr = board[(x, y - 1)]
            top_border = self.get_bottom_border(top_tile, top_tile_tr)
            top_candidates = self.borders[top_border]
            candidates.append(top_candidates)
        if candidates:
            candidates = set.intersection(*candidates)
        else:
            candidates = self.tiles
        for tile in candidates:
            if tile in placed:
                continue

            placed.add(tile)

            # Rotate it and check if it fits with the top and left neighbor
            transforms = []
            for tr in product(Flips, Rotations):
                if left_border:
                    border = self.get_left_border(tile, tr)
                    if left_border != border:
                        continue
                if top_border:
                    border = self.get_top_border(tile, tr)
                    if top_border != border:
                        continue
                transforms.append(tr)

            for tr in transforms:
                # Tile fits, move on to next tile
                nx, ny = next_slot(self.d, x, y)
                c = x, y
                board[c] = (tile, tr)
                fit_board = self._find_fit(board, placed, i + 1, ny, nx)
                if fit_board:
                    return fit_board
                del board[c]

            placed.remove(tile)
        return False

    @cache
    def get_left_border(self, tile, tr):
        return get_left_border(self.tiles[tile], tr)

    @cache
    def get_top_border(self, tile, tr):
        return get_top_border(self.tiles[tile], tr)

    @cache
    def get_right_border(self, tile, tr):
        return get_right_border(self.tiles[tile], tr)

    @cache
    def get_bottom_border(self, tile, tr):
        return get_bottom_border(self.tiles[tile], tr)

    def calc_corners(self, board):
        edges = (0, self.d - 1)
        return reduce(mul, (board[(x, y)][0] for x, y in product(edges, edges)))


def next_slot(d, x, y):
    assert x < d
    assert y < d
    nx = x + 1
    ny = y
    if nx == d:
        nx = 0
        ny += 1
    return nx, ny


def main():
    with open('sample_input.txt') as f:
        tiles = Tiles(f.read())

        if "test fit_lr":
            ts = list(tiles.tiles.values())
            a = ts[0]
            b = [r[::-1] for r in a]
            assert fit_lr(a, (Flips.NONE, Rotations.R0), b, (Flips.NONE, Rotations.R0))
            assert not fit_lr(a, (Flips.NONE, Rotations.R90), b, (Flips.NONE, Rotations.R90))
            assert fit_lr(a, (Flips.NONE, Rotations.R180), b, (Flips.NONE, Rotations.R180))
            assert not fit_lr(a, (Flips.NONE, Rotations.R270), b, (Flips.NONE, Rotations.R270))
            assert fit_lr(a, (Flips.NONE, Rotations.R270), b, (Flips.NONE, Rotations.R90))
            assert fit_lr(a, (Flips.NONE, Rotations.R90), b, (Flips.NONE, Rotations.R270))

            assert fit_lr(a, (Flips.NONE, Rotations.R0), a, (Flips.HORIZONTAL, Rotations.R0))
            assert fit_lr(a, (Flips.HORIZONTAL, Rotations.R180), b, (Flips.VERTICAL, Rotations.R0))

        if "test fit_tb":
            ts = list(tiles.tiles.values())
            a = ts[0]
            b = list(reversed(a))
            assert fit_tb(a, (Flips.NONE, Rotations.R0), b, (Flips.NONE, Rotations.R0))
            assert not fit_tb(a, (Flips.NONE, Rotations.R90), b, (Flips.NONE, Rotations.R90))
            assert fit_tb(a, (Flips.NONE, Rotations.R180), b, (Flips.NONE, Rotations.R180))
            assert not fit_tb(a, (Flips.NONE, Rotations.R270), b, (Flips.NONE, Rotations.R270))
            assert fit_tb(a, (Flips.NONE, Rotations.R270), b, (Flips.NONE, Rotations.R90))
            assert fit_tb(a, (Flips.NONE, Rotations.R90), b, (Flips.NONE, Rotations.R270))

            assert fit_tb(a, (Flips.NONE, Rotations.R0), a, (Flips.VERTICAL, Rotations.R0))
            assert fit_tb(a, (Flips.HORIZONTAL, Rotations.R180), b, (Flips.VERTICAL, Rotations.R0))

        board = tiles.find_fit()
        tiles.print_board(board)
        print()
        print(tiles.calc_corners(board))

    with open('input.txt') as f:
        tiles = Tiles(f.read())
        board = tiles.find_fit()
        tiles.print_board(board)
        print()
        print(tiles.calc_corners(board))
        print()
        tiles.print_map(board)


if __name__ == '__main__':
    main()
