from copy import deepcopy
from math import sqrt


class Tile:
    def __init__(self, name, top, bottom, left, right, lines, flipped = False, position = 0):
        self.id = name
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.lines = lines
        self.position = position #0 = origin, 1 = rotate right 90, 2 = upside down, 3 = rotate right 270
        self.flipped = flipped

    def rotate(self):
        #Correct position
        if self.position == 3:
            self.position = 0
        else:
            self.position += 1

        #Correct sides
        temp = self.top
        self.top = self.left
        self.left = self.bottom
        self.bottom = self.right
        self.right = temp

        self.top.reverse()
        self.bottom.reverse()

        #Correct lines
        new_lines = []
        for i in range(len(self.lines[0])): #Add first character of each line to top row, repeat for second character, etc
            line = ""
            for j in range(len(self.lines[0]) - 1, -1, -1): #Iterate through the rows
                line += self.lines[j][i]
            new_lines.append(line)
        self.lines = new_lines
    
        return None

    def flip_horizontal(self):
        #Correct Flipped
        if self.flipped == True:
            self.flipped = False
        else:
            self.flipped = True
        
        #Correct lines
        new_lines = []
        for line in self.lines:
            word = ""
            for char in reversed(line):
                word += char
            new_lines.append(word)
        self.lines = new_lines

        #Correct sides
        left = []
        right = []
        for i in range(len(self.left)):
            left.append(self.right[i])
            right.append(self.left[i])
        self.left = left
        self.right = right

        #Correct top 
        top = []
        for char in reversed(self.top):
            top.append(char)
        self.top = top

        #Correct bottom
        bottom = []
        for char in reversed(self.bottom):
            bottom.append(char)
        self.bottom = bottom

        return None


    def print_tile(self):
        print(f"Tile: {self.id} - Position {self.position} - Flipped: {self.flipped}")
        for char in self.top:
            print(char, end = "")
        print()
        
        for i in range(1, len(self.left) - 1):
            print(self.left[i] + ' ' * (len(self.top) - 2), end = "")
            print(self.right[i])
        
        for char in self.bottom:
            print(char, end = "")
        print()

        return None

    def __eq__(self, other):
        if self.id == other.id and self.position == other.position and self.flipped == other.flipped:
            return True
        else:
            return False

#Rotated Tile not updated from part a to handle lines
def rotated_tile(tile):
    """Creates a new tile rotated right 90 degrees from input tile"""
    flip = deepcopy(tile.flipped)
    temp = deepcopy(tile.top)
    position = deepcopy(tile.position)
    if position == 3:
        position = 0
    else:
        position += 1
    
    top = deepcopy(tile.left)
    top.reverse()

    left = deepcopy(tile.bottom)

    bottom = deepcopy(tile.right)
    bottom.reverse()

    right = temp

    return Tile(tile.id, top, bottom, left, right, flipped = flip, position = position)

#Flipped Tile not updated from part a to handle lines
def flipped_tile(tile):
    """Creates a new tile horizontally flipped from input tile"""
    position = deepcopy(tile.position)
    top = deepcopy(tile.top)
    top.reverse()

    bottom = deepcopy(tile.bottom)
    bottom.reverse()

    left = deepcopy(tile.right)
    right = deepcopy(tile.left)

    return Tile(tile.id, top, bottom, left, right, True, position = position)

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_20\input.txt", "r")

tile_check = False
top = True
bottom = False
tiles = {}

lines = []
top_row = []
bottom_row = []
left_col = []
right_col = []

for line in f:
    #Iterate through each line of input, storing each tile, its edges
    #and each character in the tile
    line = line.strip()

    line = line.split()
    if not line: #For blank lines
        pass
    elif line[0] == "Tile":
        tile_check = True
        tile_ID = int(line[1][:-1])  
        top = True  

    elif tile_check:
        line = line[0]
        if top:
            left_col.append(line[1])
            right_col.append(line[-2])
            lines.append(line[1:-1])
            top = False

        elif not bottom:
            left_col.append(line[1])
            right_col.append(line[-2])
            lines.append(line[1:-1])
            if len(left_col) == 9:
                bottom = True

        else:
            lines.append(line[1:-1])
            left_col.append(line[1])
            right_col.append(line[-2])
            bottom = False
            tile_check = False

            for char in lines[1]:
                top_row.append(char)

            for char in lines[-2]:
                bottom_row.append(char)

            #Trim edges off
            left_col = left_col[1:-1]
            right_col = right_col[1:-1]
            lines = lines[1:-1]

            tiles[tile_ID] = Tile(tile_ID, top_row, bottom_row, left_col, right_col, lines)

            #Prepare for next tile
            top_row = []
            bottom_row = []
            left_col = []
            right_col = []
            lines = []
f.close()

#Populate locations with correct tiles and rotations from part A
f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_20\existing.txt", "r")
existing = {}
for line in f:
    line = line.split()
    if line[-1] == 'False':
        flip = False
    else:
        flip = True
        flip
    existing[int(line[0])] = [int(line[2]), int(line[5]), flip]
f.close()

def correct_tile(tile, rotation, flip):
    """Adjust tile to the orientation in part a as described in existing"""
    if flip != tile.flipped:
        tile.flip_horizontal()

    while tile.position != rotation:
        tile.rotate()

def connect_tiles(tiles, existing):
    """Combine all the lines together to make larger tile"""
    square_size = int(sqrt(len(tiles)))
    counter = 1
    lines = []
    left = []
    right = []
    top = []
    bottom = []
    
    #Combine lines together
    for i in range(square_size): #Iterate through the rows

        #Create row lines
        row_lines = []
        for i in range(len(tiles[existing[1][0]].lines)):
            row_lines.append('')
        
        for j in range(square_size): #Iterate though columns
            tile = tiles[existing[counter][0]]
            for row in range(len(tile.lines)):
                row_lines[row] += tile.lines[row]
            counter += 1

        for line in row_lines:
            lines.append(line)

    #Get sides - Needs to be a square
    for i in range(len(lines[0])):
        top.append(lines[0][i])
        bottom.append(lines[-1][i])

        left.append(lines[i][0])
        right.append(lines[i][-1])

    big_tile = Tile("Full", top, bottom, left, right, lines)

    return big_tile

def get_next_tile(tiles, possible_tiles, position, existing):
    x = {}

    for tile in possible_tiles: #Pick a tile, assume it is right
        for rotate in possible_tiles[tile]:
            existing[position] = rotate
            remaining = deepcopy(tiles)
            tile_copy = deepcopy(tiles)

            #Check for next possible tiles, if not possible, remove from tile_copy
            for possible in tiles:
                for possible_rotate in tiles[possible]:
                    """Production Code"""
                    #Bottom Right Corner
                    if position == 144:
                        # print("CORRECT")
                        # for key in existing:
                        #     print(f"{key} - {existing[key].id}")
                        # print()
                        return existing

                    #Right column
                    elif position % 12 == 0:
                        if possible_rotate.top != existing[position - 11].bottom:
                            if possible_rotate in tile_copy[possible]:
                                tile_copy[possible].remove(possible_rotate)

                    #Top row
                    elif position < 12:
                        if rotate.right != possible_rotate.left:
                            if possible_rotate in tile_copy[possible]:
                                tile_copy[possible].remove(possible_rotate)

                    #Remainder of tiles
                    else:
                        if rotate.right != possible_rotate.left or possible_rotate.top != existing[position - 11].bottom:
                            if possible_rotate in tile_copy[possible]:
                                tile_copy[possible].remove(possible_rotate)

                    """End Production Code"""

                    """FOR 3 x 3 TESTING"""
                    # #Bottom Right Corner
                    # if position == 9:
                    #     print("CORRECT")
                    #     for key in existing:
                    #         print(f"{key} - {existing[key].id}")
                    #     print()
                    #     return existing

                    # #Right column
                    # elif position % 3 == 0:
                    #     if possible_rotate.top != existing[position - 2].bottom:
                    #         if possible_rotate in tile_copy[possible]:
                    #             tile_copy[possible].remove(possible_rotate)

                    # #Top row
                    # elif position < 3:
                    #     if rotate.right != possible_rotate.left:
                    #         if possible_rotate in tile_copy[possible]:
                    #             tile_copy[possible].remove(possible_rotate)

                    # #Remainder of tiles
                    # else:
                    #     if rotate.right != possible_rotate.left or possible_rotate.top != existing[position - 2].bottom:
                    #         if possible_rotate in tile_copy[possible]:
                    #             tile_copy[possible].remove(possible_rotate)
                    
                    """END 3 x 3 TESTING"""
                    

                    """FOR 2 x 2 TESTING"""
                    # if position == 1:
                    #     if tiles[tile].right != tile_copy[possible].left:
                    #         tile_copy.pop(possible, None)

                    # #Bottom row
                    # elif position == 2:
                    #     if tile_copy[possible].top != existing[1].bottom:
                    #         tile_copy.pop(possible, None)

                    # #Left Column
                    # elif position == 3:
                    #     if tile_copy[possible].top != existing[2].bottom and tile_copy[possible].left == existing[3].right:
                    #         tile_copy.pop(possible, None)

                    # else:
                    #     print("CORRECT")
                    #     for key in existing:
                    #         print(f"{key} - {existing[key].id}")
                    #     print()
                    #     return existing

                    """END 2 x 2 TESTING"""

            tile_copy.pop(tile, None) #Don't want to check this tile again on recurse --- CHECK THIS LINE TOMORROW
            remaining.pop(tile, None) #Remove chosen tile from searching on next recurse --- THIS ONE TOO
            x = get_next_tile(remaining, tile_copy, position + 1, existing)

            if x:
                break

        if x:
            break
    # print("Extra")
    # print("Unknown")
    # for key in x:
    #     print(f"{key} - {x[key].id}")
    # print()
    return x

def test_tile(tile, lines = True, edges = False, full = False):
    """
    Debugging function to help visualize any tiles
    
    lines = True is default, showing all characters
    edges = False is default, printing an outline of the tile
    full = False is dfault, printing all lines and edges

    """

    print(f"Testing Tile {tile.id} - Position {tile.position} - Flipped {tile.flipped}")
    for line in tile.lines:
        print(line)
    print()
    if full:
        print(f"Left: {tile.left}")
        print(f"Right: {tile.right}")
        print(f"Top: {tile.top}")
        print(f"Bottom: {tile.bottom}")
        print()
        tile.print_tile()
        print()

    if edges:
        print(f"Left: {tile.left}")
        print(f"Right: {tile.right}")
        print(f"Top: {tile.top}")
        print(f"Bottom: {tile.bottom}")
        print()

def monster_check(tile, location):
    """Takes a tile and location to start looking for monster in lines. Location = (y, x)"""
    x = location[1]
    y = location[0]

    check = True
    #Check row of leftmost # in monster
    if tile.lines[y][x + 5] != "#":
        check = False

    if tile.lines[y][x + 6] != "#":
        check = False

    if tile.lines[y][x + 11] != "#":
        check = False

    if tile.lines[y][x + 12] != "#":
        check = False

    if tile.lines[y][x + 17] != "#":
        check = False

    if tile.lines[y][x + 18] != "#":
        check = False
    
    if tile.lines[y][x + 19] != "#":
        check = False

    #Check top row of monster
    if tile.lines[y - 1][x + 18] != "#":
        check = False

    #Check bottom row of monster
    if tile.lines[y + 1][x + 1] != "#":
        check = False

    if tile.lines[y + 1][x + 4] != "#":
        check = False

    if tile.lines[y + 1][x + 7] != "#":
        check = False

    if tile.lines[y + 1][x + 10] != "#":
        check = False

    if tile.lines[y + 1][x + 13] != "#":
        check = False

    if tile.lines[y + 1][x + 16] != "#":
        check = False

    #Done checking for monster
    if check == True:
        return True
    else:
        return False


for position in existing:
    tile = existing[position][0]
    rotation = existing[position][1]
    flip = existing[position][2]
    correct_tile(tiles[tile], rotation, flip)

#Combine all the tiles and find total number of #s
big_tile = connect_tiles(tiles, existing)

"""Testing"""
# big_tile.rotate()
# big_tile.flip_horizontal()
# big_tile.print_tile()
"""END TESTING"""

hash_total = 0
for line in big_tile.lines:
    for char in line:
        if char == '#':
            hash_total += 1

#Flip and rotate trying to find monsters
length = len(big_tile.lines)
monsters = 0
rotated = 0
while monsters == 0:
    for y in range(1, length - 1): #Leftmost # has a row above and below
        for x in range(length - 19): #Monster has a span of 20, search starts at 1
            if big_tile.lines[y][x] == "#" and monster_check(big_tile, (y,x)):
                monsters += 1

    #Check all non-flipped rotations, then flip and check those rotations
    if rotated != 3:
        big_tile.rotate()
    else:
        big_tile.flip_horizontal()
    rotated += 1

print(f"Monsters: {monsters}")
print(f"There are {hash_total - monsters * 15} #'s in the grid")




# test_tile(big_tile, full = True)
# big_tile.flip_horizontal()
# test_tile(big_tile, full = True)
# big_tile.rotate()
# test_tile(big_tile, full = True)
