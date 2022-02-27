import copy

class Seat:
    def __init__(self, location, value):
        self.value = value
        self.location = location #(y, x), y goes top (0) to bottom (n)

    def set_val(self, v):
        self.value = v

    def get_up(self, seats):
        """Returns the value of the chair above it"""
        if self.location[0] == 0:
            return None

        else:
            #print(f"Printing Seat {self.location[0] - 1}, {self.location[1]}")
            if seats[self.location[0] - 1][self.location[1]].value == '.':
                return seats[self.location[0] - 1][self.location[1]].get_up(seats)
            
            elif seats[self.location[0] - 1][self.location[1]].value == 'L':
                return 'L'

            else:
                return '#'

    def get_bot(self, seats):
        if self.location[0] == len(seats) - 1:
            return None

        else:
            if seats[self.location[0] + 1][self.location[1]].value == '.':
                return seats[self.location[0] + 1][self.location[1]].get_bot(seats)

            elif seats[self.location[0] + 1][self.location[1]].value == 'L':
                return 'L'
            
            else:
                return '#'

    def get_left(self, seats):
        if self.location[1] == 0:
            return None
        
        else:
            if seats[self.location[0]][self.location[1] - 1].value == '.':
                return seats[self.location[0]][self.location[1] - 1].get_left(seats)

            elif seats[self.location[0]][self.location[1] - 1].value == 'L':
                return 'L'

            else:
                return '#'

    def get_right(self, seats):
        if self.location[1] == len(seats[0]) - 2:
            return None

        else:
            if seats[self.location[0]][self.location[1] + 1].value == '.':
                return seats[self.location[0]][self.location[1] + 1].get_right(seats)

            elif seats[self.location[0]][self.location[1] + 1].value == 'L':
                return 'L'

            else:
                return '#'

    def get_up_left(self, seats):
        #Check if top row or left side
        if self.location[0] == 0 or self.location[1] == 0:
            return None

        else:
            if seats[self.location[0] - 1][self.location[1] - 1].value == '.':
                return seats[self.location[0] - 1][self.location[1] - 1].get_up_left(seats)

            elif seats[self.location[0] - 1][self.location[1] - 1].value == 'L':
                return 'L'

            else:
                return '#'

    def get_up_right(self, seats):
        #Check if top row or right side
        if self.location[0] == 0 or self.location[1] == len(seats[0]) - 2:
            return None

        else:
            if seats[self.location[0] - 1][self.location[1] + 1].value == '.':
                return seats[self.location[0] - 1][self.location[1] + 1].get_up_right(seats)

            elif seats[self.location[0] - 1][self.location[1] + 1].value == 'L':
                return 'L'

            else:
                return '#'

    def get_bot_left(self, seats):
        if self.location[0] == len(seats) - 1 or self.location[1] == 0:
            return None

        else:
            if seats[self.location[0] + 1][self.location[1] - 1].value == '.':
                return seats[self.location[0] + 1][self.location[1] - 1].get_bot_left(seats)

            elif seats[self.location[0] + 1][self.location[1] - 1].value == 'L':
                return 'L'

            else:
                return '#'

    def get_bot_right(self, seats):
        if self.location[0] == len(seats) - 1 or self.location[1] == len(seats[0]) - 2:
            return None

        else:
            if seats[self.location[0] + 1][self.location[1] + 1].value == '.':
                return seats[self.location[0] + 1][self.location[1] + 1].get_bot_right(seats)

            elif seats[self.location[0] + 1][self.location[1] + 1].value == 'L':
                return 'L'

            else:
                return '#'

    def count_neighbours(self, seats):
        empty_count = 0
        full_count = 0
        if self.get_up_left(seats) == "L":
            empty_count += 1
        elif self.get_up_left(seats) == "#":
            full_count += 1

        if self.get_up(seats) == "L":
            empty_count += 1
        elif self.get_up(seats) == "#":
            full_count += 1

        if self.get_up_right(seats) == "L":
            empty_count += 1
        elif self.get_up_right(seats) == "#":
            full_count += 1         
                
        if self.get_left(seats) == "L":
            empty_count += 1
        elif self.get_left(seats) == "#":
            full_count += 1

        if self.get_right(seats) == "L":
            empty_count += 1
        elif self.get_right(seats) == "#":
            full_count += 1  

        if self.get_bot_left(seats) == "L":
            empty_count += 1
        elif self.get_bot_left(seats) == "#":
            full_count += 1   
        
        if self.get_bot(seats) == "L":
            empty_count += 1
        elif self.get_bot(seats) == "#":
            full_count += 1          

        if self.get_bot_right(seats) == "L":
            empty_count += 1
        elif self.get_bot_right(seats) == "#":
            full_count += 1  

        return(empty_count, full_count)

# def count_full(seats):
#     count = 0
#     for row in len(range(seats)):
#         for col in len(range(seats[0])):
#             if seats[row][col] == "#"


seats = []

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_11\input.txt", "r")

pos = 0

for line in f:
    new_line = []

    for x in range(len(line)):
        new_line.append(Seat((pos, x), line[x]))
    
    seats.append(new_line)
    pos += 1

f.close()

seat_copy = copy.deepcopy(seats)
different = True
i = 0

while different == True:
    full_count = 0
    change = False
    for row in range(len(seats)):
        for col in range(len(seats[0]) - 1):
            #print(f"Seat [{row}][{col}] has {seats[row][col].count_neighbours(seats)} seats")
            if seats[row][col].value == "L" and seats[row][col].count_neighbours(seats)[1] == 0:
                seat_copy[row][col].set_val("#")
                full_count += 1
                change = True
            
            elif seats[row][col].value == "#" and seats[row][col].count_neighbours(seats)[1] >= 5:
                seat_copy[row][col].set_val("L")
                change = True

            elif seats[row][col].value == "#":
                full_count += 1

    # print(f"Round {i}")
    # print("Printing Seats")
    # for newline in seats:
    #     for spot in newline:
    #         print(spot.value, end="")

    # print()
    # print("Printing Seat Copy")
    # for newline in seat_copy:
    #     for spot in newline:
    #         print(spot.value, end="")
    # print()

    if change == False:
        different = False

    seats = copy.deepcopy(seat_copy)
    i += 1

print(f"Stopped after {i} rounds")
print(f"There are {full_count} full seats")
print()


"""Print statements for debugging"""
# for newline in seats:
#     for spot in newline:
#         print(spot.value, end="")

    #print()

# print("#########")

# print(seats[0][9].get_up_left(seats), end = " ")
# print(seats[0][9].get_up(seats), end = " ")
# print(seats[0][9].get_up_right(seats))
# print(seats[0][9].get_left(seats), end = " ")
# print(seats[0][9].value, end = " ")
# print(seats[0][9].get_right(seats))
# print(seats[0][9].get_bot_left(seats), end = " ")
# print(seats[0][9].get_bot(seats), end = " ")
# print(seats[0][9].get_bot_right(seats))
# print()
# print(f"Seat has {seats[0][9].count_neighbours(seats)} seats")
# print(len(seats[1]))
# for spot in seats[1]:
#         print(spot.value, end="")

# print("ba;")
# print(seats[1][10].value)