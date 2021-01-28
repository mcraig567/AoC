"""This is actually 5-b as 5-a was saved over"""

#Read input file into list, then close file

f = open("C:\\Users\craig\Onedrive\Documents\AoC\Day_5\Input.txt", "r")
seats = []
boarding_id = []

plane = []
for i in range(128):
    column = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    plane.append(column)

for line in f:
    #print(line[:-1])
    #print(len(line[:-1]))
    #print()

    #Binary Search
    min_index = 1
    max_index = 128
    row_index = max_index / 2

    for char in line[:-4]:
        #print(char)
        if char == "F":
            max_index = row_index
            
        else:
            min_index = row_index
            
        row_index = int(min_index + (max_index - min_index) / 2)
        #print(f"max: {max}")
        #print(f"min {min}")
        #print(f"new index: {row_index}")
        #print()

    min_index = 1
    max_index = 8
    column_index = max_index / 2

    for char in line[7:-1]:
        if char == "L":
            max_index = column_index

        else:
            min_index = column_index

        column_index = int(min_index + (max_index - min_index) / 2)

    #print(f"Row {row_index}, column {column_index}")
    #print()

    seats.append((row_index, column_index))
    plane[row_index][column_index] = 1
    boarding_id.append(row_index * 8 + column_index)

f.close()

boarding_id.sort()
#print(boarding_id)
highest = max(boarding_id)
#print(f"the max ID is {highest}")

#Print out the plane seats, find seat that is 0 instead of 1
for i in range(128):
    print(i, " - ", plane[i])