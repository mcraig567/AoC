
tiles = {} #Key = (x, y, z), value = 1 (Black) or 0 (White)

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_24\input.txt", "r")

instructions = []

for line in f:
    line.strip()
    i = 0
    new_line = []
    north = False
    south = False
    for char in line[:-1]:
        if char == "n":
            north = True       
        elif char == "s":
            south = True
        elif north:
            new_line.append('n' + char)
            north = False
        elif south:
            new_line.append('s' + char)
            south = False        
        else:
            new_line.append(char)
    instructions.append(new_line)

f.close()

for_total = 0
for line in instructions:
    x = 0
    y = 0
    z = 0

    for move in line:
        if move == 'e':
            x += 1
            y -= 1
        elif move == 'ne':
            x += 1
            z -= 1
        elif move == 'se':
            z += 1
            y -= 1

        elif move == 'w':
            x -= 1
            y += 1
        elif move == 'sw':
            x -= 1
            z += 1
        elif move == 'nw':
            z -= 1
            y += 1
        else:
            print("UH OH")

    tile = (x, y, z)
    current = tiles.get(tile, 0)
    if current == 0:
        current = 1
        for_total += 1
    else:
        current = 0
        for_total -= 1
    tiles[tile] = current

total = 0
for key in tiles:
    total += tiles[key]

print(f"Total: {total}")
print(f"For_Total: {for_total}") 