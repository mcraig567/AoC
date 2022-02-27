
#Read input file into list, then close file
f = open("Input.txt", "r")

input = []
for line in f:
	input.append(int(line))
f.close()

#Iterate through each input and calculate the current and previous rolling depths
#Start at the second item in the list as the first is N/A
depthIncreases = 0

for i in range(1, len(input)-2):
	previousDepth = input[i - 1] + input[i] + input[i + 1]
	currentDepth = input[i] + input[i + 1] + input[i + 2]

	if currentDepth > previousDepth:
		depthIncreases += 1

print(depthIncreases)
