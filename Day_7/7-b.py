#Read input file into list, then close file

f = open("C:\\Users\craig\Documents\AoC\Day_7\Inputtest2.txt", "r")

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
                number = int(third_split[0])
                combined = third_split[1] + " " + third_split[2]
                #print(f"comb: {combined}")
                #print()
                #print("ts1: ", third_split[1][:-5])
                
                items.append((combined, number))

            # print(line[:-1])
            # print(key)
            # print(items)
            # print()
            bags[key] = items

f.close()

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

def bag_number(bag_dict, bag_key, total = 0):
    if bag_dict[bag_key] != None:
        #Check each kind of bag contained by current bag
        for i in bag_dict[bag_key]:
            #Add the bags contained by current bag
            total += i[1]

            #Check bags contained by current bag for other bags
            #If current bag contains 2 bags of same type, want to do twice
            for j in range(i[1]):
                total += bag_number(bag_dict, i[0])

        return total

    else:
        return 0

total = bag_number(bags, "shiny gold")

print(f"total: {total}")



