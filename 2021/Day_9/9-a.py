import timeit

f = open("Input.txt", "r")

heights = {}
maxLine = 0
maxRow = 0

lineIndex = 0
for line in f:
	for rowIndex in range(len(line) - 1): #len(line) - 1 to drop the new line character
		heights[(lineIndex, rowIndex)] = line[rowIndex]

		if rowIndex > maxRow:
			maxRow = rowIndex

	if lineIndex > maxLine:
		maxLine = lineIndex

	lineIndex += 1

f.close()

### Helper Functions ###

def checkLeftHigher(heights, location):
	left = heights[(location[0], location[1] - 1)]

	if left <= heights[location]:
		return False

	return True

def checkRightHigher(heights, location):
	right = heights[(location[0], location[1] + 1)]

	if right <= heights[location]:
		return False

	return True

def checkAboveHigher(heights, location):
	above = heights[(location[0] - 1, location[1])]

	if above <= heights[location]:
		return False

	return True

def checkBelowHigher(heights, location):
	below = heights[(location[0] + 1, location[1])]

	if below <= heights[location]:
		return False

	return True

### End Helper Functions ###

start = timeit.default_timer()

lowPoints = []
for location in heights:
	line = location[0]
	row = location[1]

	if line == 0 and row == 0: # Top Left Corner
		if checkBelowHigher(heights, location) and checkRightHigher(heights, location):
			lowPoints.append(location)

	elif line == 0 and row == maxRow: # Top Right Corner
		if checkBelowHigher(heights, location) and checkLeftHigher(heights, location):
			lowPoints.append(location)

	elif line == 0: # Rest of top row
		if checkBelowHigher(heights, location) and checkLeftHigher(heights, location) and checkRightHigher(heights, location):
			lowPoints.append(location)

	elif line == maxLine and row == 0: # Bottom Left Corner
		if checkAboveHigher(heights, location) and checkRightHigher(heights, location):
			lowPoints.append(location)

	elif line == maxLine and row == maxRow: # Bottom Right Corner
		if checkAboveHigher(heights, location) and checkLeftHigher(heights, location):
			lowPoints.append(location)

	elif line == maxLine: # Rest of bottom row
		if checkAboveHigher(heights, location) and checkLeftHigher(heights, location) and checkRightHigher(heights, location):
			lowPoints.append(location)

	elif row == 0: # Rest of left hand column
		if checkBelowHigher(heights, location) and checkAboveHigher(heights, location) and checkRightHigher(heights, location):
			lowPoints.append(location)

	elif row == maxRow: # Rest of right hand column
		if checkBelowHigher(heights, location) and checkAboveHigher(heights, location) and checkLeftHigher(heights, location):
			lowPoints.append(location)

	else: # Everything else
		if checkBelowHigher(heights, location) and checkAboveHigher(heights, location) and checkLeftHigher(heights, location) and checkRightHigher(heights, location):
			lowPoints.append(location)

totalRisk = 0
for point in lowPoints:
	#print(point)
	height = int(heights[point])
	totalRisk += (height + 1)

print("Risk: ", totalRisk)


stop = timeit.default_timer()

print('Time: ', stop - start)
