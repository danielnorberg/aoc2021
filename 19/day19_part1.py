# 8: 42 | 42 8
# 8: 42+

# 11: 42 31 | 42 11 31
# 11: (42 31)+


def match_sub_rule(rules, s, i, sub_rule):
    for r in sub_rule:
        if type(r) == int:
            i = match_rule(rules, s, i, r)
            if not i:
                return False
        else:
            if i >= len(s):
                return False
            c = s[i]
            if c != r:
                return False
            i += 1
    return i


def match_rule(rules, s, i, rid):
    rule = rules[rid]
    for sub_rule in rule:
        ni = match_sub_rule(rules, s, i, sub_rule)
        if ni:
            return ni
    return False


def match(rules, s):
    i = match_rule(rules, s, 0, 0)
    return i == len(s)


def parse_sub_rule(s):
    return [int(c) if c.isdigit() else c.strip('"') for c in s.split()]


def parse_rule(s):
    return [parse_sub_rule(r.strip()) for r in s.split('|')]


def main():
    with open('sample_input.txt') as f:
        print(count_matching_messages(f))
    with open('input.txt') as f:
        print(count_matching_messages(f))


def count_matching_messages(f, ef=None):
    rules_text, messages_text = f.read().split('\n\n')
    rules = {int(i.strip()): parse_rule(s.strip()) for i, s in (l.split(':') for l in rules_text.splitlines())}
    messages = messages_text.splitlines()
    if ef:
        expected_matches = ef.readlines()
        for m in expected_matches:
            assert match(rules, m), 'not matched: {}'.format(m)

    n = sum(1 for m in messages if match(rules, m))
    return n


if __name__ == '__main__':
    main()
