import timeit
import copy

codes = {}

with open("InputTest2.txt", "r") as inputFile:
	for line in inputFile:
		if line == "\n":
			pass
		elif len(line.split("->"))== 1:
			main_code = line[:-1]
		else:
			code, new = line.split(" -> ")
			new = new[:-1]
			codes[code] = new

### Problem Parameters ###

### End Problem Parameters ###

### Helper Functions ###

def find_new_code(old_code, code_dict):
	letters_to_join = []
	for i in range(len(old_code[:-1])): #Don't want to check final letter

		# First add letter that's part of the main code
		letters_to_join.append(old_code[i])

		# Now check the next letter to see if a code exists
		code = old_code[i:i+2]
		#print("CHECKING CODE: ", code)
		new_letter = code_dict.get(code, "")
		letters_to_join.append(new_letter)
		#print(letters_to_join)
		#print()

	# Catch final letter of original code
	letters_to_join.append(old_code[-1]) 

	return "".join(letters_to_join)

def get_counts(code):
	letter_counts = {}
	max_count = 0
	min_count = 99

	for char in code:
		amount = letter_counts.get(char, 0)
		amount += 1
		letter_counts[char] = amount

		if amount > max_count:
			letter_counts["max_letter"] = char
			max_count = amount

		if amount < min_count or letter_counts["min_letter"] == char:
			letter_counts["min_letter"] = char
			min_count = amount

	return letter_counts

### End Helper Functions ###

start = timeit.default_timer()

iterations = 3
old_code = main_code

for i in range(iterations):
	#print("Iteration: ", i)
	new_code = find_new_code(old_code, codes)
	old_code = new_code

print(new_code)
letter_count = get_counts(new_code)
for letter in letter_count:
	print(letter, " - ", letter_count[letter])
max_count = letter_count[letter_count["max_letter"]]
min_count = letter_count[letter_count["min_letter"]]

print("ANS: ", max_count - min_count)


stop = timeit.default_timer()

print('Time: ', stop - start)
