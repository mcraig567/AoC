
tiles = {} #Key = (x, y, z), value = 1 (Black) or 0 (White)
black_tiles = []
seen_tiles = []


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

def add_neighbours(tile):
    x = tile[0]
    y = tile[1]
    z = tile[2]

    loc = (x, y, z)
    nw = (x, y + 1, z - 1)
    ne = (x + 1, y, z - 1)
    e = (x + 1, y - 1, z)
    se = (x, y - 1, z + 1)
    sw = (x - 1, y, z + 1)
    w = (x - 1, y + 1, z)

    return [loc, nw, ne, e, se, sw, w]

def sum_neighbours(tile, tiles):
    x = tile[0]
    y = tile[1]
    z = tile[2]

    nw = (x, y + 1, z - 1)
    ne = (x + 1, y, z - 1)
    e = (x + 1, y - 1, z)
    se = (x, y - 1, z + 1)
    sw = (x - 1, y, z + 1)
    w = (x - 1, y + 1, z)

    neighbours = [nw, ne, e, se, sw, w]
    total = 0
    for i in neighbours:
        total += tiles.get(i, 0)

    return total

#Set the initial layout
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
        black_tiles.append(tile)
        for_total += 1
    else:
        current = 0
        black_tiles.remove(tile)
        for_total -= 1
    tiles[tile] = current
    

total = 0
# for key in tiles:
#     print(f"Tile {key} is {tiles[key]}")
#     total += tiles[key]

#Get list of all black tiles, and tiles neighbouring them
def create_list(black_tiles):
    seen_tiles = set() #empty set
    for tile in black_tiles:
        for neighbour in add_neighbours(tile):
            seen_tiles.add(neighbour)
    return seen_tiles


def end_day(black_tiles, tiles):
    to_black = []
    to_white = []

    for tile in create_list(black_tiles):
        surround = sum_neighbours(tile, tiles)
        if tiles.get(tile, 0) == 1:
            if surround == 0 or surround > 2:
                to_white.append(tile)
        else:
            if surround == 2:
                to_black.append(tile)

    for tile in to_white:
        tiles[tile] = 0
        black_tiles.remove(tile)
    
    for tile in to_black:
        tiles[tile] = 1
        black_tiles.append(tile)

    return black_tiles, tiles


for i in range(100):
    black_tiles, tiles = end_day(black_tiles, tiles)
    print(f"Day {i + 1}: {len(black_tiles)}")



# print(f"Total: {total}")
# print(f"For_Total: {for_total}") 

