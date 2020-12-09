def load_program(f):
    return [(op, int(arg)) for (op, arg) in (line.split() for line in f)]


def find_loop(program):
    visited = [False for _ in program]
    acc = 0
    i = 0
    while True:
        if visited[i]:
            return acc
        visited[i] = True
        op, arg = program[i]
        if op == 'nop':
            i += 1
        elif op == 'acc':
            acc += arg
            i += 1
        elif op == 'jmp':
            i += arg
        else:
            assert False


def main():
    with open('sample_input.txt') as f:
        program = load_program(f)
    print(find_loop(program))

    with open('input.txt') as f:
        program = load_program(f)
    print(find_loop(program))


if __name__ == '__main__':
    main()
