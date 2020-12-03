import re

input_pattern = re.compile(r'^(?P<a>\d+)-(?P<b>\d+)\s+(?P<char>\w):\s+(?P<pwd>\w+)\s*$')

valid = 0
with open('input.txt') as f:
    for line in f:
        m = input_pattern.match(line)
        assert m
        pwd = m['pwd']
        a = int(m['a'])
        b = int(m['b'])
        char = m['char']
        if (pwd[a - 1] == char) ^ (pwd[b - 1] == char):
            print('valid: ' + line)
            valid += 1

print('total valid: ' + str(valid))