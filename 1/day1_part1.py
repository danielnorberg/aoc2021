

with open('input.txt') as f:
    numbers = set(int(line.strip()) for line in f)

for n in numbers:
    complement = 2020 - n
    if complement in numbers:
        print(n * complement)
