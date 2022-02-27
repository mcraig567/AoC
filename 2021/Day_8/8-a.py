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
	1 : ["c", "f"],
	2 : ["a", "c", "d", "e" "g"],
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

start = timeit.default_timer()


easyRepeats = 0
for line in lines:

	#Probably part b work
	""" print(line[0])
	possible = copy.copy(ALLPOSSIBLE)

	for code in line[0]:
		numOptions = SEGLENGTHS[len(code)]
		
		if len(numOptions) == 1: # We know what number it's going to be
			num = numOptions[0]
			possibleSegs = NUMSEGS[num]
			for char in code:
				if len(possible[char]) > len(possibleSegs): #Don't add chars back to possible
					possible[char] = possibleSegs

		#Determine which is "a" from the 
		

	for key in sorted(possible.keys()):
		print(key, " : ", possible[key])
	print() """

	#print(line[1])
	for code in line[1]:
		if len(code) in [2,4,3,7]:
			#print(code)
			easyRepeats += 1

print(easyRepeats)

stop = timeit.default_timer()

print('Time: ', stop - start)
