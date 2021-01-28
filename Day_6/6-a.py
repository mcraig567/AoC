
"""DAY 7 - saved over day 6"""

#Read input file into list, then close file

f = open("C:\\Users\craig\Documents\AoC\Day_7\Input.txt", "r")

bags = {}

#Each bag type will be a key in the dictionary. Each value will be a list with the bags it can contain

for line in f:
    #Clean up data - get key
    if len(line) > 1:
        first_split = line.split("contain")
        #print(first_split)
        key = first_split[0][:-6]

        second = first_split[1][1:-2]
        #print(second)

        if second == "no other bags":
            bags[key] = None
        else:
            second_split = second.split(", ")
            #print(f"second: {second_split}")

            items = []
            for i in second_split:
                third_split = i.split(" ")
                #print(third_split)
                combined = third_split[1] + " " + third_split[2]
                #print(f"comb: {combined}")
                #print()
                #print("ts1: ", third_split[1][:-5])
                
                items.append(combined)

            # print(line[:-1])
            # print(key)
            # print(items)
            # print()
            bags[key] = items

f.close()

total = 0

def bag_check(bag_dict, bag_key):
    """Recursively determine if bag will contain a shiny gold bag"""

    has_gold = False
    if bag_dict[bag_key] != None:
        for bag in bag_dict[bag_key]:
            if "shiny gold" in bag_dict[bag_key]:
                #print(f"{bag_key} contains shiny gold")
                has_gold = True

            else:
                for bag in bag_dict[bag_key]:
                    #print(f"Kids are {bag_dict[bag_key]}")
                    #print(f"recursing with {bag}")
                    has_gold = has_gold or bag_check(bag_dict, bag)

    else:
        pass
        #print("No bags here")
    
    return has_gold

# print(len(bags))
# for key, value in bags.items():
#     print(key, " - ", value)
i = 1
for key in bags:
    #print()
    print(f"Testing bag {i} {key}")
    if bag_check(bags, key):
        #print("success")
        total += 1
    i += 1

print(f"total: {total}")



