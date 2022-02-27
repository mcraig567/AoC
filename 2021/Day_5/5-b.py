import timeit

### HELPER FUNCTIONS ###

#Converts a pair of coordinates separated by ',' into a tuple (x, y)
def convertStrPointToInt(strPoint):
	coords = strPoint.split(',')
	return (int(coords[0]), int(coords[1]))

def determineOrientation(line):
	start = line[0]
	end = line[1]

	#If X1 == X2
	if start[0] == end[0]:
		return "vert"
	elif start[1] == end[1]:
		return "hor"
	else:
		return "diag"

def flipStart(start, end, orientation):
	if orientation == "vert":
		if start[1] > end[1]:
			return end, start
		else:
			return start, end

	else: #For both horizontal and diagonal lines
		if start[0] > end[0]:
			return end, start
		else:
			return start, end

def updateCoordinates(line, orientation, coordinates):
	start = line[0]
	end = line[1]
	start, end = flipStart(start, end, orientation)

	if orientation == "vert":
		#print("Vertical Line - ", start, " ", end)
		for spot in range(start[1], end[1] + 1):
			#print("Updating Location: (", start[0], ",", spot, ")")
			existingCoord = coordinates.get((start[0], spot), 0)
			existingCoord += 1
			coordinates[(start[0], spot)] = existingCoord

			coordinates["data"]["total"] += 1


			if existingCoord == 2: #We now have a spot that has been hit twice. Only add this location to multiple once.
				coordinates["data"]["multiple"] += 1

	elif orientation == "hor":
		#print("Horizontal Line - ", start, " ", end)
		for spot in range(start[0], end[0] + 1):
			#print("Updating Location: (", spot, ",", start[1], ")")
			existingCoord = coordinates.get((spot, start[1]), 0)
			existingCoord += 1
			coordinates[(spot, start[1])] = existingCoord

			coordinates["data"]["total"] += 1

			if existingCoord == 2:
				coordinates["data"]["multiple"] += 1

	else:
		# Start and End are already flipped so that the line "goes" left -> right
		# Need to determine if line goes up or down

		iterCounter = 0
		for spot in range(start[0], end[0] + 1):
			if end[1] > start[1]: # Line goes up
				existingCoord = coordinates.get((spot, start[1] + iterCounter), 0)
				existingCoord += 1
				coordinates[(spot, start[1] + iterCounter)] = existingCoord

			else: # Line goes down
				existingCoord = coordinates.get((spot, start[1] - iterCounter), 0)
				existingCoord += 1
				coordinates[(spot, start[1] - iterCounter)] = existingCoord

			coordinates["data"]["total"] += 1

			if existingCoord == 2:
				coordinates["data"]["multiple"] += 1

			iterCounter += 1

	return coordinates

### END HELPER FUNCTIONS ###

### INPUT CLEANUP ###
f = open("Input.txt", "r")

lines = []
for line in f:
	points = line.split(" -> ")
	lineStart = convertStrPointToInt(points[0])
	lineEnd = convertStrPointToInt(points[1])
	lines.append((lineStart, lineEnd))

f.close()
### END INPUT CLEANUP ###
 
### DATA ANALYSIS ###

coordinates = {
	"data" : {
		"total" : 0,
		"multiple" : 0
	}
}

start = timeit.default_timer()

for line in lines:
	orientation = determineOrientation(line)
	coordinates = updateCoordinates(line, orientation, coordinates)

#print(coordinates)
print("Number of overlaps: ", coordinates["data"]["multiple"])

""" for y in range(10):
	line = ""
	for x in range(10):
		amount = coordinates.get((x,y), ".")
		line = line + str(amount)
	print(line) """

stop = timeit.default_timer()

print('Time: ', stop - start)
