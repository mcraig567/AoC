from copy import deepcopy

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_23\inputtest.txt", "r")
cups = {}
index = {}

i = 0
for line in f:
    for char in line:
        cups[int(char)] = i
        index[i] = int(char)
        i += 1
f.close()

print(cups)
print()

#Add all million cups
while len(cups) < 1000000:
    cups[len(cups) + 1] = len(cups)
    index[len(cups) - 1] = len(cups)

def play_turn(cups, index, start):
    """Start is 0 indexed"""

    #index_copy = deepcopy(index)

    # for key in sorted(index):
    #     print(f"{index[key]}, ", end = "")
    # print()
    # print(f"Current Cup: {start}")
    start_index = cups[start]
    if start_index + 4 >= len(cups):
        new_current = index[start_index + 4 - len(cups)]
    else:
        new_current = index[start_index + 4]

    new_cups = []
    for i in range(3):
        if start_index + i + 1 >= len(cups):
            new_cups.append(index[start_index + i - len(cups) + 1])
        else:
            new_cups.append(index[start_index + i + 1])

    #print(f"Pick up: {new_cups}")

    destination_label = start - 1

    if destination_label < min(cups):
        destination_label = max(cups)

    while destination_label in new_cups:
        destination_label -= 1
        if destination_label < min(cups):
            destination_label = max(cups)
    dest_index = cups[destination_label]

    if start_index > dest_index:
        #Move all numbers after destination, up to and including start up by 3
        index_copy = []
        for i in range(dest_index + 1, start_index + 1):
            index_copy.append((i, index[i]))

        for pair in index_copy:
            number = pair[1]
            i = pair[0]
            if number not in new_cups:
                if i + 3 >= len(cups):
                    cups[number] = i + 3 - len(cups)
                    index[i + 3 - len(cups)] = number
                else:  
                    cups[number] = i + 3
                    index[i + 3] = number

        #Move the three picked cups back to destination
        for i in range(3):
            number = new_cups[i]
            if dest_index + i + 1 >= len(cups):
                cups[number] = dest_index + i + 1 - len(cups)
                index[dest_index + i + 1 - len(cups)] = number
            else:
                cups[number] = dest_index + i + 1
                index[dest_index + i + 1] = number               

    else:
        #Move all numbers after start, up to and including destination down by 3
        index_copy = []
        for i in range(start_index + 1, dest_index + 1):
            index_copy.append((i, index[i]))

        for pair in index_copy:
            number = pair[1]
            i = pair[0]


        # for i in range(start_index + 1, dest_index + 1):
        #     number = index_copy[i]
            if number not in new_cups:
                if i - 3 < 0:
                    cups[number] = i - 3 + len(cups)
                    index[i - 3 + len(cups)] = number
                else:
                    cups[number] = i - 3
                    index[i - 3] = number
        
        #Moved destination, recalculate new index
        dest_index = cups[destination_label]
        #Move the three picked cups to destination
        for i in range(3):
            number = new_cups[i]
            if dest_index + i + 1 >= len(cups):
                cups[number] = dest_index + i + 1 - len(cups)
                index[dest_index + i + 1 - len(cups)] = number
            else:
                cups[number] = dest_index + i + 1
                index[dest_index + i + 1] = number   

    # print(f"Destination: {destination_label}")
    # for key in sorted(index):
    #     print(f"{index[key]}, ", end = "")
    # print()
    # print()

    return cups, index, new_current

start = 3
for i in range(10000000):
    print(f"-- Move {i + 1} --")
    cups, index, start = play_turn(cups, index, start)

print()
print()
# for key in sorted(index):
#     print(f"{index[key]}, ", end = "")
# print()
#Find index for 1
i = cups[1]
if i + 1 < len(cups):
    print(f"first cup is {cups[i + 1]}")
    j = i + 1
else:
    print(f"first cup is {cups[i + 1 - len(cups)]}")
    j = i + 1 - len(cups)
if i + 2 < len(cups):
    print(f"second cup is {cups[i + 2]}")
    k = i + 2
else:
    print(f"second cup is {cups[i + 2 - len(cups)]}")
    k = i + 2 - len(cups)
print(f"Total is {cups[j] * cups[k]}")