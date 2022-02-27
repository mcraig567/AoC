import timeit

f = open("Input.txt", "r")

#openBrackets = ["(", "[", "{", "<"]
closeBrackets = [")", "]", "}", ">"]

# Key = close bracket, Value = open bracket
bracketPairs = {
	")" : "(",
	"]" : "[",
	"}" : "{",
	">" : "<"
}

# Key = close backets, Value = (Times found, score per time)
illegalCloseBrackets = {
	")" : (0, 3),
	"]" : (0, 57),
	"}" : (0, 1197),
	">" : (0, 25137)
}

start = timeit.default_timer()

for line in f:
	openBrackets = []
	#print(line)
	for char in line[:-1]: #No new line character
		if char in closeBrackets:
			expectedMatch = bracketPairs[char]
			if expectedMatch == openBrackets[-1]: #Legally closed a bracket
				openBrackets.pop(-1)

			else: #Illegally closed - add illegal character to dictionary for scoring
				#print(line[:-1])
				#print("Illegaly found ", char)
				#print()
				bracketHistory = illegalCloseBrackets[char]
				newHistory = (bracketHistory[0] + 1, bracketHistory[1])
				illegalCloseBrackets[char] = newHistory
				break

		else:
			openBrackets.append(char)

f.close()

score = 0
for value in illegalCloseBrackets.values():
	score += value[0] * value[1]

print("Score: ", score)

stop = timeit.default_timer()

print('Time: ', stop - start)
