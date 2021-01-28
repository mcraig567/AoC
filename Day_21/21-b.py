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
        
        #Create list of lists
        options.append(ingredients)
        allergen_option_lists[allergen] = options

        #Create set of all possible ingredients
        existing = list(allergen_option_all.get(allergen, []))
        for ingredient in ingredients:
            existing.append(ingredient)
            reduced = set(existing)

        allergen_option_all[allergen] = reduced

f.close()

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

total = 0
for item in items:
    total += ingredient_times[item]

#print(f"Impossible items show up {total} times")

for item in items:
    for foods in allergen_option_lists:
        for listed in allergen_option_lists[foods]:
            if item in listed:
                listed.remove(item)
        if item in allergen_option_all[foods]:
            allergen_option_all[foods].remove(item)
            
#Correct word must be in all of the lists
new_possible = {}
for food in allergen_option_lists:
    new_list = []
    for ind_food in allergen_option_all[food]:
        check = True
        for ind_list in allergen_option_lists[food]:
            if ind_food not in ind_list:
                check = False
                break
        if check == True:
            new_list.append(ind_food)

    new_possible[food] = new_list

def reduce_items(foods):
    for food in foods:
        if len(foods[food]) == 1:
            for other_food in foods:
                if other_food != food and foods[food][0] in foods[other_food]:
                    foods[other_food].remove(foods[food][0])

for i in range(9):
    reduce_items(new_possible)

print("Done reducing")
for key in sorted(new_possible):
    print(f"{new_possible[key][0]},", end="")