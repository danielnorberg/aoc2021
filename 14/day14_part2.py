MAX = 0xfffffffff


def write(mem, val, addr, mask, i=0):
    if i >= 36:
        mem[int("".join(addr), 2)] = val
        return
    bit = mask[i]
    if bit == 'X':
        addr[i] = '0'
        write(mem, val, addr, mask, i + 1)
        addr[i] = '1'
        write(mem, val, addr, mask, i + 1)
    else:
        if bit == '1':
            addr[i] = '1'
        write(mem, val, addr, mask, i + 1)


def run_program(f):
    mem = {}
    for l in f:
        if 'mask' in l:
            mask = l.strip().split()[-1]
        else:
            op, _, val = l.strip().split()
            val = int(val)
            addr = list(format(int(op[4:-1]), '036b'))
            write(mem, val, addr, mask)
    return sum(mem.values())


def main():
    with open('sample_input2.txt') as f:
        result = run_program(f)
        print(result)
    with open('input.txt') as f:
        result = run_program(f)
        print(result)


if __name__ == '__main__':
    main()
