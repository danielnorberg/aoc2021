import re
from itertools import chain

RULE_PATTERN = re.compile(r'^([^:]+):\s*(\d+)-(\d+)(?:\s+or\s+(\d+)-(\d+))*$')


def sum_invalid(f):
    rules, ticket, nearby_tickets = f.read().split('\n\n')
    rules = {m.group(1): list(zip(map(int, m.groups()[1::2]), map(int, m.groups()[2::2])))
             for m in (RULE_PATTERN.match(rule) for rule in rules.splitlines())}
    ticket = [int(d) for d in ticket.strip().splitlines()[1].split(',')]
    nearby_tickets = [[int(d) for d in t.split(',')] for t in nearby_tickets.strip().splitlines()[1:]]
    invalid = 0
    for value in chain(*nearby_tickets):
        valid = False
        for a, b in chain(*rules.values()):
            if a <= value <= b:
                valid = True
                break
        if not valid:
            invalid += value
    print(invalid)


def main():
    with open('sample_input.txt') as f:
        sum_invalid(f)
    with open('input.txt') as f:
        sum_invalid(f)


if __name__ == '__main__':
    main()
