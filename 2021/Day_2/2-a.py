
#Read input file into list, then close file
f = open("Input.txt", "r")

input = []
for line in f:
	input.append(line)
f.close()

#Keep both depth and horizontal positions in a dictionary
position = {
	"depth" : 0,
	"horizontal" : 0
}

for instruction in input:

	#Split input on space to separate the direction and distance
	instructionSplit = instruction.split(" ")
	direction = instructionSplit[0]
	amount = int(instructionSplit[1])

	#Apply change in position
	if direction == "forward":
		position["horizontal"] += amount
	elif direction == "down":
		position["depth"] += amount
	else:
		position["depth"] -= amount

print(position["horizontal"])
print(position["depth"])
print(position["horizontal"] * position["depth"])
