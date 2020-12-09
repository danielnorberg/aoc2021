def load_program(f):
    return [[op, int(arg)] for (op, arg) in (line.split() for line in f)]


def fix_loop(program):
    for i in range(len(program)):
        op, arg = program[i]
        if op == 'nop':
            new_op = 'jmp'
        elif op == 'jmp':
            new_op = 'nop'
        else:
            continue
        program[i][0] = new_op
        result = run_program(program)
        if result is not None:
            return result
        program[i][0] = op
    raise False


def main():
    with open('sample_input.txt') as f:
        program = load_program(f)
    print(fix_loop(program))

    with open('input.txt') as f:
        program = load_program(f)
    print(fix_loop(program))


def run_program(program):
    visited = [False for _ in program]
    acc = 0
    i = 0
    while True:
        if i == len(program):
            return acc
        if visited[i]:
            return None
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


if __name__ == '__main__':
    main()
