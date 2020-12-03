

with open('input.txt') as f:
    numbers = set(int(line.strip()) for line in f)

for n1 in numbers:
    for n2 in numbers:
        complement = 2020 - n1 - n2
        if complement in numbers:
            print(n1 * n2 * complement)
