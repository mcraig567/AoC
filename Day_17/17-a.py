from copy import deepcopy

spots = {} #key = (x,y,z), value = # or .

#Prepopulate off cubes
for x in range(-15, 20):
    for y in range(-15, 20):
        for z in range(-15, 20):
            spots[(x,y,z)] = '.'




f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_17\input.txt", "r")

x = y = z = 0
x_max = 0
for line in f:
    new_line = line[:-1]
    for char in new_line:
        spots[(x,y,z)] = char
        #spots[(x,y,z + 1)] = '.'
        #spots[(x,y,z - 1)] = '.'
        x += 1
        if x > x_max:
            x_max = x
    y += 1
    x = 0

f.close()

def count_neighbours(key, spots):
    #Key = (x, y, z)
    """
    x - 1, y, z - 1     x - 1, y - 1, z - 1     x - 1, y + 1, z - 1
    x - 1, y, z         x - 1, y - 1, z         x - 1, y + 1, z
    x - 1, y, z + 1     x - 1, y - 1, z + 1     x - 1, y + 1, z + 1

    x, y, z - 1         x, y - 1, z - 1         x, y + 1, z - 1
    x, y, z             x, y - 1, z             x, y + 1, z
    x, y, z + 1         x, y - 1, z + 1         x, y + 1, z + 1    

    x + 1, y, z - 1     x + 1, y - 1, z - 1     x + 1, y + 1, z - 1
    x + 1, y, z         x + 1, y - 1, z         x + 1, y + 1, z
    x + 1, y, z + 1     x + 1, y - 1, z + 1     x + 1, y + 1, z + 1
    """
    neighbours = 0
    x_range = [key[0] - 1, key[0], key[0] + 1]
    y_range = [key[1] - 1, key[1], key[1] + 1]
    z_range = [key[2] - 1, key[2], key[2] + 1]
    
    for x in x_range:
        #print(f"x = {x}")
        for y in y_range:
            #print(f"y = {y}")
            for z in z_range:
                #print(f"({x},{y},{z}) - {spots.get((x,y,z), '.')}")
                if spots.get((x,y,z), '.') == '#':
                    neighbours += 1
    
    #Will have counted self, correct if #
    if spots.get(key, '.') == '#':
        neighbours -= 1

    return neighbours

# count_neighbours((1,1,1), spots)
# print(spots)

x_min = -1 #x and y have same max/min
x_max = 3
z = 1

for i in range(6):
    to_neg = []
    to_pos = []

    # #Create new side cubes
    # for y in range(x_min, x_max):
    #     spots[(x_min, y, 0)] = '.'
    #     spots[(x_max, y, 0)] = '.'
    #     spots[(y, x_min, 0)] = '.'
    #     spots[(y, x_max, 0)] = '.'
    #     spots[(x_max, x_max, 0)] = '.'

    # #Create new top and bottom levels
    # for y in range(x_min, x_max + 1):
    #     for x in range(x_min, x_max + 1):
    #         spots[(x,y,z)] = '.'
    #         spots[(x,y,z * -1)] = '.'


    #Testing - Printing all levels
    print("####")
    print(f"Round {i}")
    print("####")
    print()
    for z_test in range(z * -1, z + 1):
        print(f"z = {z_test}")
        for y_test in range(x_min + 1, x_max):
            for x_test in range(x_min + 1, x_max):
                print(spots[(x_test, y_test, z_test)], end="")
            print()
        print()

    x_max += 1
    x_min -= 1
    z += 1

    #See what cubes should be changed
    for key in spots:
        if spots[key] == '#':
            neighbours = count_neighbours(key, spots)
            if neighbours == 2 or neighbours == 3:
                pass
            else:
                to_neg.append(key)

        elif spots[key] == '.':
            neighbours = count_neighbours(key, spots)
            if neighbours == 3:
                to_pos.append(key)

    #Update cubes for next iteration
    for key in to_neg:
        spots[key] = '.'

    for key in to_pos:
        spots[key] = '#'

    #print(spots)



#Count all active cubes
total = 0
for key in spots:
    if spots[key] == '#':
        total += 1

print(f"There are {total} cubes on")