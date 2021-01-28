"""This is actually 3-b, 3-a was saved over"""

#Read input file into list, then close file
input = []
move_index = [1, 3, 5, 7, 1]
down_index = [1, 1, 1, 1, 2]

for i in range(len(move_index)):
    pos = 0
    tree = 0
    line_num = 0

    f = open("C:\\Users\craig\Documents\AoC\Day_3\Input.txt", "r")

    for line in f:

        #Skip a line if down_index is greater than 1
        if down_index[i] != 1:
            if line_num % down_index[i] == 0:
                if line[pos] == "#":
                    tree = tree + 1

                pos = pos + move_index[i]

                if pos >= len(line) - 1:
                    pos = pos - (len(line) - 1)

                line_num = line_num + 1
            else:
                line_num = line_num + 1
                print("SKIP")
                print()
                
        else:
            if line[pos] == "#":
                tree = tree + 1

            pos = pos + move_index[i]
            if pos >= len(line) - 1:
                pos = pos - (len(line) - 1)

    f.close()

    input.append(tree)

print(input)

prod = 1
for i in input:
    prod = prod * i

print("Product: ", prod)