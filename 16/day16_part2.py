import re
from functools import reduce
from itertools import chain

RULE_PATTERN = re.compile(r'^([^:]+):\s*(\d+)-(\d+)(?:\s+or\s+(\d+)-(\d+))*$')


def find_fields(rules, values):
    for name, ranges in rules.items():
        if all(valid_value(value, ranges) for value in values):
            yield name


def calculate_departure(f):
    rules, ticket, nearby_tickets = f.read().split('\n\n')
    rules = {m.group(1): list(zip(map(int, m.groups()[1::2]), map(int, m.groups()[2::2])))
             for m in (RULE_PATTERN.match(rule) for rule in rules.splitlines())}
    my_ticket = [int(d) for d in ticket.strip().splitlines()[1].split(',')]
    nearby_tickets = [[int(d) for d in t.split(',')] for t in nearby_tickets.strip().splitlines()[1:]]
    valid_tickets = [ticket for ticket in nearby_tickets if valid_ticket(rules, ticket)]
    field_candidates = [list(find_fields(rules, field_values)) for field_values in zip(*valid_tickets)]
    field_names = [None for c in field_candidates]

    # Assign field with only one candidate, scrub from other candidate lists, repeat until finished
    assigned = True
    while assigned:
        assigned = False
        for i, names in enumerate(field_candidates):
            if field_names[i] is not None:
                continue
            if len(names) == 1:
                field_name = names.pop()
                field_names[i] = field_name
                assigned = True
                for rc in field_candidates:
                    if field_name in rc:
                        rc.remove(field_name)
                break

    # Check that all fields were named
    assert (all(field_names))

    departure_values = [my_ticket[i] for i, name in enumerate(field_names) if name.startswith('departure ')]
    result = reduce(lambda x, y: x * y, departure_values)
    print(result)


def valid_value(value, ranges):
    for a, b in ranges:
        if a <= value <= b:
            return True
    return False


def valid_ticket(rules, ticket):
    for value in ticket:
        if not valid_value(value, chain(*rules.values())):
            return False
    return True


def main():
    # with open('sample_input2.txt') as f:
    #     calculate_departure(f)
    with open('input.txt') as f:
        calculate_departure(f)


if __name__ == '__main__':
    main()
