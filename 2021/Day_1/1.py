
#Read input file into list, then close file
f = open("Input.txt", "r")

input = []
for line in f:
	input.append(int(line))
f.close()

#Iterate through each input to see if a depth is greater than the previous depth
#Start at the second item in the list as the first is N/A
depthIncreases = 0

for i in range(1, len(input)):
	if input[i] > input[i - 1]:
		depthIncreases += 1

print(depthIncreases)
