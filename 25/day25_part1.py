from itertools import count

CEILING = 20201227
INITIAL_SUBJECT = 7

PUBLIC_KEYS = (
    11349501,
    5107328
)


def compute_key(subject, loop_size):
    v = 1
    for i in range(loop_size):
        v *= subject
        v = v % CEILING
    return v


def search_loop_size(public_key):
    v = 1
    for i in count(1):
        v *= INITIAL_SUBJECT
        v = v % CEILING
        if v == public_key:
            return i


def main():
    assert search_loop_size(5764801) == 8
    assert search_loop_size(17807724) == 11

    assert compute_key(17807724, 8) == 14897079
    assert compute_key(5764801, 11) == 14897079

    loop_sizes = [search_loop_size(k) for k in PUBLIC_KEYS]
    assert compute_key(INITIAL_SUBJECT, loop_sizes[0]) == PUBLIC_KEYS[0]
    assert compute_key(INITIAL_SUBJECT, loop_sizes[1]) == PUBLIC_KEYS[1]

    encryption_key1 = compute_key(PUBLIC_KEYS[1], loop_sizes[0])
    encryption_key2 = compute_key(PUBLIC_KEYS[0], loop_sizes[1])
    assert encryption_key1 == encryption_key2

    encryption_key = encryption_key1
    print('encryption key:', encryption_key)


if __name__ == '__main__':
    main()
