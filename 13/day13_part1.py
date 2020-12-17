import sys


def main():
    with open('sample_input.txt') as f:
        best_bus, wait = find_best_bus(f)
        print(wait * best_bus)
    with open('input.txt') as f:
        best_bus, wait = find_best_bus(f)
        print(wait * best_bus)


def find_best_bus(f):
    earliest_departure = int(f.readline().strip())
    buses = [int(bus.strip()) for bus in f.readline().strip().split(',') if bus.strip() != 'x']
    best_bus = -1
    best_bus_departure = sys.maxsize
    for bus in buses:
        d = earliest_departure // bus
        m = earliest_departure % bus
        if m > 0:
            d += 1
        departure = d * bus
        if departure < best_bus_departure:
            best_bus_departure = departure
            best_bus = bus
        # print(bus, departure)
    wait = best_bus_departure - earliest_departure
    return best_bus, wait


if __name__ == '__main__':
    main()