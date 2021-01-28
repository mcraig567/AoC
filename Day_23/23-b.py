from copy import deepcopy

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_23\input.txt", "r")
cups = {}
index = {}
neighbours = {}
i = 0
for line in f:
    for char in line:
        index[i] = int(char)
        i += 1
f.close()

# print(cups)
print()

#Add all million cups
while len(index) < 1000000:
    index[len(index)] = len(index) + 1

#Populate Neighbours
for key in index:
    if key == len(index) - 1:
        neighbours[index[key]] = index[0]
    else:
        neighbours[index[key]] = index[key + 1]

LOWEST = min(neighbours)
HIGHEST = max(neighbours)

def play_turn(neighbours, start):
    """Start is 0 indexed"""

    #index_copy = deepcopy(index)

    # for key in sorted(index):
    #     print(f"{index[key]}, ", end = "")
    # print()
    # print(f"Current Cup: {start}")
    
    destination = start - 1
    if destination < LOWEST:
        destination = HIGHEST

    first_moved = neighbours[start]
    second_moved = neighbours[first_moved]
    third_moved = neighbours[second_moved]
    
    moving = [first_moved, second_moved, third_moved]

    while destination in moving:
        destination -= 1
        if destination < LOWEST:
            destination = HIGHEST

    temp_dest = neighbours[destination]
    neighbours[destination] = neighbours[start]
    
    # print(f"Pick up: {moving}")
    # print(f"Destination: {destination}")

    temp_moving = neighbours[third_moved]
    
    neighbours[third_moved] = temp_dest
    neighbours[start] = temp_moving

    new_start = neighbours[start]

    # print(f"{start} ", end = "")
    # for i in range(len(neighbours) - 1):
    #     print(f"{neighbours[start]} ", end = "")
    #     start = neighbours[start]
    # print()
    # print()

    return neighbours, new_start

start = 4
for i in range(10000000):
    # if i % 1000 == 0:
    #     print(f"-- Move {i + 1} --")
    neighbours, start = play_turn(neighbours, start)

start = neighbours[1]
# print(f"{start} ", end = "")
# for i in range(len(neighbours) - 1):
#     print(f"{neighbours[start]} ", end = "")
#     start = neighbours[start]
# print()
# print()

#Find index for 1
first = neighbours[1]
print(f"first cup is {first}")
second = neighbours[first]
print(f"second cup is {second}")
print(f"Total is {first * second}")
