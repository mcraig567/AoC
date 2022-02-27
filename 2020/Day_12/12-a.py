
directions = []

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_12\input.txt", "r")

for line in f:
    cardinal = line[0]
    amount = int(line[1:-1])
    directions.append((cardinal, amount))

#print(directions)

    
f.close()

horizontal = 0
vertical = 0
point = 2 #N = 1, E = 2, S = 3, W = 0

#Iterate through directions and move ship as directed
for item in directions:
    if item[0] == 'E':
        horizontal += item[1]
    elif item[0] == 'W':
        horizontal -= item[1]
    elif item[0] == 'N':
        vertical += item[1]
    elif item[0] == 'S':
        vertical -= item[1]
    elif item[0] == "L":
        point -= item[1]/90
    elif item[0] == "R":
        point += item[1]/90
    elif item[0] == "F":
        pointer = point % 4
        if pointer == 1:
            vertical += item[1]
        elif pointer == 2:
            horizontal += item[1]
        elif pointer == 3:
            vertical -= item[1]
        elif pointer == 0:
            horizontal -= item[1]
        else:
            print("WHAAAA")

print(f"Vertical: {vertical}")
print(f"Horizontal: {horizontal}")
print()
print(f"Manhattan: {abs(vertical) + abs(horizontal)}")

