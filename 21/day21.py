import re

p = re.compile(r'(?P<ingredients>(?:(\w+)\s)+)\(contains (?P<allergens>\w+(?:, \w+)*)\)')


def compute_allergens(f):
    all_ingredients = []
    candidates = {}
    for l in f:
        m = p.match(l.strip())
        ingredients = set(m.group('ingredients').strip().split())
        all_ingredients.extend(ingredients)
        allergens = [s.strip() for s in m.group('allergens').strip().split(',')]
        for allergen in allergens:
            candidates[allergen] = candidates.get(allergen, ingredients).intersection(ingredients)
    unfixed = set(candidates.keys())
    fixed = {}
    while unfixed:
        for allergen in unfixed:
            c = candidates[allergen]
            if len(c) == 1:
                food = next(iter(c))
                fixed[allergen] = food
                for cs in candidates.values():
                    cs.discard(food)
                unfixed.remove(allergen)
                break
    non_allergen_ingredients = set(all_ingredients) - set(fixed.values())
    return (sum(1 for ingredient in all_ingredients if ingredient in non_allergen_ingredients),
            ",".join(it[1] for it in sorted(fixed.items(), key=lambda it: it[0])))


def main():
    with open('sample_input.txt') as f:
        print(compute_allergens(f))
    with open('input.txt') as f:
        print(compute_allergens(f))


if __name__ == '__main__':
    main()
