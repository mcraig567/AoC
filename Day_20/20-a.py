from copy import deepcopy


class Tile:
    def __init__(self, name, top, bottom, left, right, flipped = False, position = 0):
        self.id = name
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.position = position #0 = origin, 1 = rotate right 90, 2 = upside down, 3 = rotate right 270
        self.flipped = flipped

    def rotate(self):
        pass

    def flip_horizontal(self):
        pass

    def flip_vertical(self):
        pass

    def print_tile(self):
        print(f"Tile: {self.id} - Position {self.position} - Flipped: {self.flipped}")
        for char in self.top:
            print(char, end = "")
        print()
        
        for i in range(1, len(self.left) - 1):
            print(self.left[i] + ' ' * 8, end = "")
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

top_row = []
bottom_row = []
left_col = []
right_col = []

for line in f:
    #Iterate through each line of input, storing each tile and its edges
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
            for char in line:
                top_row.append(char)
            left_col.append(line[0])
            right_col.append(line[-1])
            top = False

        elif not bottom:
            left_col.append(line[0])
            right_col.append(line[-1])
            if len(left_col) == 9:
                bottom = True

        else:
            for char in line:
                bottom_row.append(char)
            left_col.append(line[0])
            right_col.append(line[-1])
            bottom = False
            tile_check = False

            tile_list = []
            original = Tile(tile_ID, top_row, bottom_row, left_col, right_col)
            flipped = flipped_tile(original)

            tile_list.append(original)
            tile_list.append(flipped)

            #Create and add each possible arrangement to tile_list, then add to tiles
            rotated = original
            flip_rotated = flipped

            for i in range(3):
                rotated = rotated_tile(rotated)
                flip_rotated = rotated_tile(flip_rotated)
                tile_list.append(rotated)
                tile_list.append(flip_rotated)
            tiles[tile_ID] = tile_list

            #Prepare for next tile
            top_row = []
            bottom_row = []
            left_col = []
            right_col = []

f.close()

"""Debugging Print Statements"""
# print(tiles)
# tiles[1].print_tile()
# print()
# tiles[2].print_tile()
# print()
# tiles[3].print_tile()
# print()
# tiles[4].print_tile()
# print()
# print(tiles[4].left)

"""
2 x 2 grid - position 1 is in top left, position 4 is in bottom right
"""

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

test = get_next_tile(tiles, tiles, 1, {})
print("FINAL")
for key in test:
    print(f"{key} - {test[key].id} - Rotation: {test[key].position} - Flipped: {test[key].flipped}")
print()

print("OPTION ONE")
#keys = [1,3,7,9]       #For a 3 x 3 grid
keys = [1,12,133,144]   #For a 12 x 12 grid
product = 1
for key in keys:
    print(f"1 - {test[key].id} - Rotation: {test[key].position} - Flipped: {test[key].flipped}")
    product *= test[key].id
print()
print(f"Product: {product}")
