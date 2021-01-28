
#Read input file into list, then close file
f = open("C:\\Users\craig\Documents\AoC\Day_1\Input.txt", "r")

input = []
for line in f:
    input.append(int(line))
f.close()


#Iterate through each input to see if a pair is in the input list. Output both
#pairs and the multiple if found
for first in input:
    for second in input:
        if first + second == 2020:
            print(f"First = {first}, Second = {second}, multiple = {first * second}")
            break


#For Larger Input Size
# - Sort by size
# - Find required pair
# - Search for pair
