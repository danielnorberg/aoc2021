import re

EXPECTED_FIELDS = {
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    # "cid", # optional
}

with open('input.txt') as f:
    data = f.read()

passports = data.split("\n\n")

valid = 0

whitespace = re.compile(r"\s+")

for passport in passports:
    fields = {r.split(":")[0] for r in whitespace.split(passport)}
    if not EXPECTED_FIELDS.difference(fields):
        valid += 1

print(valid)