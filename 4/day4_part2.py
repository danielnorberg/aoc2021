import re

year_pattern = re.compile(r'^\d{4}$')

hgt_pattern = re.compile(r'^(\d{2,3})(cm|in)$')


def hgt(v):
    m = hgt_pattern.match(v)
    if not m:
        return False
    num = int(m.group(1))
    unit = m.group(2)
    if unit == 'cm':
        return 150 <= num <= 193
    elif unit == 'in':
        return 59 <= num <= 76
    else:
        return False


hcl_pattern = re.compile(r'^#[0-9a-f]{6}$')
ecl_pattern = re.compile(r'^(amb|blu|brn|gry|grn|hzl|oth)$')
pid_pattern = re.compile(r'^\d{9}$')


EXPECTED_FIELDS = {
    "byr": lambda v: year_pattern.match(v) and 1920 <= int(v) <= 2002,
    "iyr": lambda v: year_pattern.match(v) and 2010 <= int(v) <= 2020,
    "eyr": lambda v: year_pattern.match(v) and 2020 <= int(v) <= 2030,
    "hgt": hgt,
    "hcl": lambda v: hcl_pattern.match(v),
    "ecl": lambda v: ecl_pattern.match(v),
    "pid": lambda v: pid_pattern.match(v),
    # "cid", # optional
}

whitespace = re.compile(r"\s+")


def valid_passport(passport):
    fields = {k: v for (k, v) in (r.split(":") for r in whitespace.split(passport) if ':' in r)}
    for name, validator in EXPECTED_FIELDS.items():
        value = fields.get(name)
        if not value:
            return False
        if not validator(value):
            return False
    return True


def main():
    with open('input.txt') as f:
        data = f.read()

    passports = data.split("\n\n")

    valid = 0
    for passport in passports:
        if valid_passport(passport):
            valid += 1

    print(valid)


if __name__ == '__main__':
    main()