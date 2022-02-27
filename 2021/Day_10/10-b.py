import timeit

### Problem Parameters ###

closeBrackets = [")", "]", "}", ">"]

# Key = close bracket, Value = open bracket
closeBracketPairs = {
	")" : "(",
	"]" : "[",
	"}" : "{",
	">" : "<"
}

# Key = open bracket, Value = close bracket
openBracketPairs = {
	"(" : ")",
	"[" : "]",
	"{" : "}",
	"<" : ">"
}

# Key = close backets, Value = (Times found, score per time)
bracketScores = {
	")" : 1,
	"]" : 2,
	"}" : 3,
	">" : 4
}

### End Problem Parameters ###

### Helper Functions ###

# Requires that all brackets in bracketList are valid open brackets
def getClosingBrackets(bracketList):
	closingBrackets = []
	for i in reversed(bracketList):
		newBracket = openBracketPairs[i]
		closingBrackets.append(newBracket)

	return closingBrackets

# Requires that all brackets in bracketList exist in bracketScores
def scoreBrackets(bracketList, bracketScores):
	score = 0
	for bracket in bracketList:
		score *= 5
		score += bracketScores[bracket]

	return score

### End Helper Functions ###

start = timeit.default_timer()

scoreList = []

f = open("Input.txt", "r")
for line in f:
	noIllegalChars = True
	openBrackets = []
	#print(line)
	for char in line[:-1]: #No new line character
		if char in closeBrackets:
			expectedMatch = closeBracketPairs[char]
			if expectedMatch == openBrackets[-1]: #Legally closed a bracket
				openBrackets.pop(-1)

			else: #Illegally closed - discard
				noIllegalChars = False
				break
		
		else:
			openBrackets.append(char)

	if noIllegalChars:
		closingBrackets = getClosingBrackets(openBrackets)
		lineScore = scoreBrackets(closingBrackets, bracketScores)
		scoreList.append(lineScore)

f.close()

# Determine the middle index of scores sorted smallest -> largest
sortedScores = sorted(scoreList)
middleIndex = int(len(sortedScores) / 2)
print("Middle Score: ", sortedScores[middleIndex])

stop = timeit.default_timer()

print('Time: ', stop - start)
