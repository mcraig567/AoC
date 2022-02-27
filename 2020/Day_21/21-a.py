f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_21\input.txt", "r")

ingredient_times = {}
allergen_option_lists = {}
allergen_option_all = {}
impossible_ingredients = {}

for line in f:
    line = line.strip()
    line = line.split(" (contains ")
    ingredients = line[0].split()

    #Keep track of how many times each ingredient is listed
    for food in ingredients:
        times = ingredient_times.get(food, 0)
        times += 1
        ingredient_times[food] = times

    allergens = line[1][:-1]
    allergens = allergens.split(", ")

    for allergen in allergens:
        options = allergen_option_lists.get(allergen, [])
        
        #Create list of allergen lists
        options.append(ingredients)
        allergen_option_lists[allergen] = options

        #Create set of all possible ingredients
        existing = list(allergen_option_all.get(allergen, []))
        for ingredient in ingredients:
            existing.append(ingredient)
            reduced = set(existing)

        allergen_option_all[allergen] = reduced

f.close()

"""Debugging print statements"""
# for key in ingredient_times:
#     print(f"{key} - {ingredient_times[key]}")

# for key in allergen_option_lists:
#     print(f"{key} - {allergen_option_lists[key]}")
#     print()

# for key in allergen_option_all:
#     print(f"{key} - {allergen_option_all[key]}")
#     print()
"""End debugging print statements"""

#For an ingredient to be an allergen, it must be in each list of ingredients for foods
#Containing that allergen
for key in ingredient_times:
    for foods in allergen_option_lists:
        for listed in allergen_option_lists[foods]:
            if key not in listed:
                bad = impossible_ingredients.get(key, [])
                bad.append(food)
                impossible_ingredients[key] = bad
                break

items = []
for key in impossible_ingredients:
    if len(impossible_ingredients[key]) == len(allergen_option_lists):
        items.append(key)

#print(f"Impossible items: {items}")

total = 0
for item in items:
    total += ingredient_times[item]

print(f"Impossible items show up {total} times")