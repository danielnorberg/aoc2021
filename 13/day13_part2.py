def solve_modulo_equation_system(equations):
    p, d = equations[0]
    for n, r in equations[1:]:
        while True:
            d += p
            if d % n == r:
                p *= n
                break
    return d


def find_sequential_departures(f):
    f.readline()
    buses = [(n := int(bus.strip()), (n - i) % n)
             for i, bus in enumerate(f.readline().strip().split(',')) if bus.strip() != 'x']
    return solve_modulo_equation_system(buses)


def main():
    with open('sample_input.txt') as f:
        ts = find_sequential_departures(f)
        print(ts)
    with open('input.txt') as f:
        ts = find_sequential_departures(f)
        print(ts)


if __name__ == '__main__':
    main()
