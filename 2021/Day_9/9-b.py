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

	return left

def checkRightHigher(heights, location):
	right = heights[(location[0], location[1] + 1)]

	if right <= heights[location]:
		return False

	return right

def checkAboveHigher(heights, location):
	above = heights[(location[0] - 1, location[1])]

	if above <= heights[location]:
		return False

	return above

def checkBelowHigher(heights, location):
	below = heights[(location[0] + 1, location[1])]

	if below <= heights[location]:
		return False

	return below

#Checks surrounding points, return True if all are higher, False otherwise
def checkForLowPoint(heights, location):

	# Top Left Corner
	if line == 0 and row == 0:
		if checkBelowHigher(heights, location) and checkRightHigher(heights, location):
			return True

	# Top Right Corner
	elif line == 0 and row == maxRow:
		if checkBelowHigher(heights, location) and checkLeftHigher(heights, location):
			return True

	# Rest of top row
	elif line == 0:
		if checkBelowHigher(heights, location) and checkLeftHigher(heights, location) and checkRightHigher(heights, location):
			return True

	# Bottom Left Corner
	elif line == maxLine and row == 0:
		if checkAboveHigher(heights, location) and checkRightHigher(heights, location):
			return True

	# Bottom Right Corner
	elif line == maxLine and row == maxRow:
		if checkAboveHigher(heights, location) and checkLeftHigher(heights, location):
			return True

	# Rest of bottom row
	elif line == maxLine:
		if checkAboveHigher(heights, location) and checkLeftHigher(heights, location) and checkRightHigher(heights, location):
			return True

	# Rest of left hand column
	elif row == 0:
		if checkBelowHigher(heights, location) and checkAboveHigher(heights, location) and checkRightHigher(heights, location):
			return True

	# Rest of right hand column
	elif row == maxRow:
		if checkBelowHigher(heights, location) and checkAboveHigher(heights, location) and checkLeftHigher(heights, location):
			return True

	# Everything else
	else:
		if checkBelowHigher(heights, location) and checkAboveHigher(heights, location) and checkLeftHigher(heights, location) and checkRightHigher(heights, location):
			return True

	return False

def buildBasin(heights, location):
	line = location[0]
	row = location[1]
	ans = []

	#Check the points around the location to see if they're higher (and not 9)

	# Top Left Corner
	if line == 0 and row == 0:
		if checkBelowHigher(heights, location) and checkBelowHigher(heights, location) != "9":
			ans.append((line + 1, row))

		if checkRightHigher(heights, location) and checkRightHigher(heights, location) != "9":
			ans.append((line, row + 1))

	# Top Right Corner
	elif line == 0 and row == maxRow:
		if checkBelowHigher(heights, location) and checkBelowHigher(heights, location) != "9":
			ans.append((line + 1, row))

		if checkLeftHigher(heights, location) and checkLeftHigher(heights, location) != "9":
			ans.append((line, row - 1))

	# Rest of top row
	elif line == 0:
		if checkBelowHigher(heights, location) and checkBelowHigher(heights, location) != "9":
			ans.append((line + 1, row))

		if checkLeftHigher(heights, location) and checkLeftHigher(heights, location) != "9":
			ans.append((line, row - 1))

		if checkRightHigher(heights, location) and checkRightHigher(heights, location) != "9":
			ans.append((line, row + 1))
	
	# Bottom Left Corner
	elif line == maxLine and row == 0:
		if checkAboveHigher(heights, location) and checkAboveHigher(heights, location) != "9":
			ans.append((line - 1, row))
		
		if checkRightHigher(heights, location) and checkRightHigher(heights, location) != "9":
			ans.append((line, row + 1))

	# Bottom Right Corner
	elif line == maxLine and row == maxRow:
		if checkAboveHigher(heights, location) and checkAboveHigher(heights, location) != "9":
			ans.append((line - 1, row))

		if checkLeftHigher(heights, location) and checkLeftHigher(heights, location) != "9":
			ans.append((line, row - 1))

	# Rest of bottom row
	elif line == maxLine:
		if checkAboveHigher(heights, location) and checkAboveHigher(heights, location) != "9":
			ans.append((line - 1, row))
		
		if checkLeftHigher(heights, location) and checkLeftHigher(heights, location) != "9":
			ans.append((line, row - 1))

		if checkRightHigher(heights, location) and checkRightHigher(heights, location) != "9":
			ans.append((line, row + 1))

	# Rest of left hand column
	elif row == 0:
		if checkBelowHigher(heights, location) and checkBelowHigher(heights, location) != "9":
			ans.append((line + 1, row))

		if checkAboveHigher(heights, location) and checkAboveHigher(heights, location) != "9":
			ans.append((line - 1, row))

		if checkRightHigher(heights, location) and checkRightHigher(heights, location) != "9":
			ans.append((line, row + 1))

	# Rest of right hand column
	elif row == maxRow:
		if checkBelowHigher(heights, location) and checkBelowHigher(heights, location) != "9":
			ans.append((line + 1, row))

		if checkAboveHigher(heights, location) and checkAboveHigher(heights, location) != "9":
			ans.append((line - 1, row))

		if checkLeftHigher(heights, location) and checkLeftHigher(heights, location) != "9":
			ans.append((line, row - 1))

	# Everything else
	else:
		if checkBelowHigher(heights, location) and checkBelowHigher(heights, location) != "9":
			ans.append((line + 1, row))

		if checkAboveHigher(heights, location) and checkAboveHigher(heights, location) != "9":
			ans.append((line - 1, row))

		if checkLeftHigher(heights, location) and checkLeftHigher(heights, location) != "9":
			ans.append((line, row - 1))

		if checkRightHigher(heights, location) and checkRightHigher(heights, location) != "9":
			ans.append((line, row + 1))

	# Recursively go through any points to see if there are extra points to add to the basin
	# Any new found points go into tempAnsPoints, and at the end of all recursion, those get added to ans

	tempAnsPoints = []
	if ans:
		for point in ans:
			newPoints = buildBasin(heights, point)
			tempAnsPoints.extend(newPoints)
			
	ans.extend(tempAnsPoints)
	return ans


### End Helper Functions ###

start = timeit.default_timer()

lowPoints = []
for location in heights:
	line = location[0]
	row = location[1]

	if checkForLowPoint(heights, location):
		lowPoints.append(location)

basinSizes = []

# take each low point and find the basin around it
for point in lowPoints:
		basin = buildBasin(heights, point)
		basin.append(point)	# buildBasin doesn't include the original low point
		basinSet = set(basin) # no repeating allowed as we care about sizes
		basinSizes.append(len(basinSet))

basinSizes.sort(reverse = True)

basinProd = 1
for i in range(3):
	basinProd *= basinSizes[i]

print("Basin Sizes: ", basinProd)

stop = timeit.default_timer()

print('Time: ', stop - start)
