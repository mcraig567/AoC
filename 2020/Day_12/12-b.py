
directions = []

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_12\input.txt", "r")

for line in f:
    #line_trim = line[:-1]
    cardinal = line[0]
    amount = int(line[1:-1])
    directions.append((cardinal, amount))

#print(directions)

    
f.close()

position = [0, 0] #[Vertical, Horizontal]
waypoint = [1,10] #[Vertical, Horizontal]

for item in directions:
    #Now need to move waypoint instead of ship
    if item[0] == 'E':
        waypoint[1] += item[1]
    elif item[0] == 'W':
        waypoint[1] -= item[1]
    elif item[0] == 'N':
        waypoint[0] += item[1]
    elif item[0] == 'S':
        waypoint[0] -= item[1]

    elif item[0] == "L":
        amount = (item[1] / 90) % 4
        if amount == 1:
            waypoint = [waypoint[1], waypoint[0] * -1]
        elif amount == 2:
            waypoint = [waypoint[0] * -1, waypoint[1] * -1]
        elif amount == 3:
            waypoint = [waypoint[1] * -1, waypoint[0]]

    elif item[0] == "R":
        amount = (item[1] / 90) % 4
        if amount == 1:
            waypoint = [waypoint[1] * -1, waypoint[0]]
        elif amount == 2:
            waypoint = [waypoint[0] * -1, waypoint[1] * -1]
        elif amount == 3:
            waypoint = [waypoint[1], waypoint[0] * -1]   

    elif item[0] == "F":
        position[0] += waypoint[0] * item[1]
        position[1] += waypoint[1] * item[1]

print(f"Vertical: {position[0]}")
print(f"Horizontal: {position[1]}")
print()
print(f"Manhattan: {abs(position[0]) + abs(position[1])}")

