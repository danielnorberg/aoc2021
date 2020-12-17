MAX = 0xfffffffff


def run_program(f):
    mem = {}
    for l in f:
        if 'mask' in l:
            mask = l.strip().split()[-1].lower()
        else:
            op, _, val = l.strip().split()
            val = int(val)
            addr = int(op[4:-1])
            for i, bit in enumerate(mask):
                if bit == 'x':
                    continue
                elif bit == '0':
                    val &= (MAX ^ (1 << (35 - i)))
                elif bit == '1':
                    val |= 1 << (35 - i)
            mem[addr] = val
    return sum(mem.values())


def main():
    with open('sample_input.txt') as f:
        result = run_program(f)
        print(result)
    with open('input.txt') as f:
        result = run_program(f)
        print(result)


if __name__ == '__main__':
    main()
