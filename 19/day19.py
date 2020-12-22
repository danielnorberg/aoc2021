def match_sub_rule(rules, s, i, sub_rule, ri):
    assert ri <= len(sub_rule)
    assert i <= len(s)
    if ri == len(sub_rule):
        yield i
        return
    if i == len(s):
        return
    r = sub_rule[ri]
    if type(r) == int:
        for ni in match_rule(rules, s, i, r):
            yield from match_sub_rule(rules, s, ni, sub_rule, ri + 1)
    else:
        c = s[i]
        if c == r:
            yield from match_sub_rule(rules, s, i + 1, sub_rule, ri + 1)


def match_rule(rules, s, i, rid):
    rule = rules[rid]
    for sub_rule in rule:
        yield from match_sub_rule(rules, s, i, sub_rule, 0)


def match(rules, s):
    return any(i == len(s) for i in match_rule(rules, s, 0, 0))


def parse_sub_rule(s: str):
    return [int(c) if c.isdigit() else c.strip('"') for c in s.split()]


def parse_rule(s):
    return [parse_sub_rule(r.strip()) for r in s.split('|')]


def main():
    # Part 1
    with open('sample_input.txt') as f:
        print(count_matching_messages(f))
    with open('input.txt') as f:
        print(count_matching_messages(f))

    # Part 2
    extra_rules = '\n11: 42 31 | 42 11 31' + \
                  '\n8: 42 | 42 8'
    with open('sample_input2.txt') as f, open('expected_matches2.txt') as ef:
        print(count_matching_messages(f, ef, extra_rules=extra_rules))
    with open('input2.txt') as f:
        print(count_matching_messages(f, extra_rules=extra_rules))


def count_matching_messages(f, ef=None, extra_rules=''):
    rules_text, messages_text = f.read().split('\n\n')
    rules_text += extra_rules
    rules = {int(i.strip()): parse_rule(s.strip()) for i, s in (l.split(':') for l in rules_text.splitlines())}
    messages = messages_text.splitlines()
    expected_matches = ef.read().splitlines() if ef else []
    for m in expected_matches:
        assert match(rules, m), 'not matched: {}'.format(m)
    n = sum(1 for m in messages if match(rules, m))
    return n


if __name__ == '__main__':
    main()
