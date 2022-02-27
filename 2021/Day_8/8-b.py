import timeit
import copy

f = open("Input.txt", "r")

lines = []
for line in f:
	lineSplit = line.split(" | ")
	codes = lineSplit[0].split(" ")
	digits = lineSplit[1].split(" ")

	#Clean up new line
	digits[-1] = digits[-1][:-1]

	newEntry = (codes, digits)
	lines.append(newEntry)

f.close()

# Key = number of segments, Value = digits that use that number of segments
SEGLENGTHS = {
	2 : [1],
	3 : [7],
	4 : [4],
	5 : [2, 3, 5],
	6 : [0, 6, 9],
	7 : [8]
}

# Key = digit, Value = letter segments required to make digit for a seven-segment display
NUMSEGS = {
	0 : ["a", "b", "c", "e", "f", "g"],
	1 : ["c", "f"],
	2 : ["a", "c", "d", "e", "g"],
	3 : ["a", "c", "d", "f", "g"],
	4 : ["b", "c", "d", "f"],
	5 : ["a", "b", "d", "f", "g"],
	6 : ["a", "b", "d", "e", "f", "g"],
	7 : ["a", "c", "f"],
	8 : ["a", "b", "c", "d", "e", "f", "g"],
	9 : ["a", "b", "c", "d", "f", "g"]
}

ALLNUMS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ALLCHARS = ["a", "b", "c", "d", "e", "f", "g"]
ALLPOSSIBLE = {}
for char in ALLCHARS:
	ALLPOSSIBLE[char] = ALLCHARS

### HELPER FUNCTIONS ###

def checkForSingle(possible):
	ans = []
	for key in possible:
		if len(possible[key]) == 1:
			ans.append(key)
	return ans

def removeFinished(possible, finished):
	for letter in finished:
		segToRemove = possible[letter][0]
		for key in possible:
			possibleList = possible[key]
			if segToRemove in possibleList and key != letter:
				possibleList.remove(segToRemove)

	return possible

def removeUnfinished(possible, segsToRemove):
	for key in possible:
		if key not in segsToRemove:
			possibleList = possible[key]
			for seg in possible[segsToRemove[0]]:
				if seg in possibleList:
					possibleList.remove(seg)
					possible[key] = possibleList

	return possible

def printPossible(possible):
	for key in sorted(possible.keys()):
		print(key, " : ", possible[key])
	print()

	return None

def convertListToChar(possible):
	for key in possible.keys():
		temp = possible[key][0]
		possible[key] = temp
	return possible

def buildInvertedDict(possible):
	ans = {}
	for key in possible.keys():
		correctChar = possible[key]
		ans[correctChar] = key
	return ans

### END HELPER FUNCTIONS ###

start = timeit.default_timer()

totalOutput = 0
for line in lines:

	possible = copy.deepcopy(ALLPOSSIBLE) #Key = segment in puzzle, value = 'correct' segment
	oneSegs = set()
	for code in line[0]:
		numOptions = SEGLENGTHS[len(code)]

		if len(numOptions) == 1: # We know what number it's going to be
			num = numOptions[0]
			possibleSegs = copy.deepcopy(NUMSEGS[num])

			for char in code:
				if len(possible[char]) > len(possibleSegs): #Don't add chars back to possible
					possible[char] = possibleSegs

				if len(possibleSegs) == 2:
					oneSegs.add(char)
	
	oneSegs = list(oneSegs)

	#Remove the 'c' and 'f' options from all but the segments in 1
	possible = removeUnfinished(possible, oneSegs)

	finished = checkForSingle(possible)
	if finished:
		possible = removeFinished(possible, finished)

	twoSegs = set()
	for key in possible:
		if len(possible[key]) == 2 and key not in oneSegs:
			twoSegs.add(key)
	twoSegs = list(twoSegs)

	possible = removeUnfinished(possible, twoSegs)

	#Use the 8 and 0 to isolate d
	for code in line[0]:
		if len(code) == 7:
			eightCode = code
		elif len(code) == 6:
			if code.find(twoSegs[0]) < 0 or code.find(twoSegs[1]) < 0:
				zeroCode = code
	
	dSeg = eightCode
	for char in zeroCode:
		dSeg = dSeg.replace(char, "")

	possible[dSeg] = ['d']
	possible = removeFinished(possible, [dSeg])

	#Use the 6 to isolate c
	for code in line[0]:
		if len(code) == 6:
			if code.find(oneSegs[0]) < 0 or code.find(oneSegs[1]) < 0:
				sixCode = code
				break

	cSeg = eightCode
	for char in sixCode:
		cSeg = cSeg.replace(char, "")

	possible[cSeg] = ['c']
	posible = removeFinished(possible, [cSeg])

	#Use the 9 and dSeg to isolate e
	for code in line[0]:
		if len(code) == 6:
			if code.find(oneSegs[0]) >= 0 and code.find(oneSegs[1]) >= 0 and code.find(dSeg) >= 0:
				nineCode = code
				break
	
	eSeg = eightCode
	for char in nineCode:
		eSeg = eSeg.replace(char, "")

	possible[eSeg] = ['e']
	possible = removeFinished(possible, [eSeg])
	
	# Possible is now complete, each segment matches it's pair
	# Convert to char from list for building strings
	possibleChar = convertListToChar(possible)

	#Get corrected code specific numbers
	numsToSum = []
	ansSum = ""
	for code in line[1]:
		strBuild = ""
		for char in code:
			strBuild = strBuild + possible[char]
		numsToSum.append(strBuild)

		#Determine which numbers line up with each corrected code:
		possibleInts = SEGLENGTHS[len(code)]
		for num in possibleInts:
			correct = True
			for char in NUMSEGS[num]:
				if strBuild.find(char) == -1:
					correct = False

			if correct == True:
				ansSum = ansSum + str(num)

	totalOutput += int(ansSum)

print("TOTAL: ", totalOutput)

stop = timeit.default_timer()

print('Time: ', stop - start)
