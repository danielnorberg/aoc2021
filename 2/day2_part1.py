import re

input_pattern = re.compile(r'^(?P<min>\d+)-(?P<max>\d+)\s+(?P<char>\w):\s+(?P<pwd>\w+)\s*$')

valid = 0
with open('input.txt') as f:
    for line in f:
        m = input_pattern.match(line)
        assert m
        pwd = m['pwd']
        min = int(m['min'])
        max = int(m['max'])
        char = m['char']
        n = pwd.count(char)
        if min <= n <= max:
            print('valid: ' + line)
            valid += 1
        else:
            print('invalid: ' + line)

print('total valid: ' + str(valid))