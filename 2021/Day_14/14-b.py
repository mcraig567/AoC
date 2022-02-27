import timeit
import copy

codes = {}

with open("InputTest.txt", "r") as inputFile:
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
		new_letter = code_dict.get(code, "")
		letters_to_join.append(new_letter)

	# Catch final letter of original code
	letters_to_join.append(old_code[-1]) 

	return "".join(letters_to_join)

def get_counts(code):
	letter_counts = {}
	for char in code:
		amount = letter_counts.get(char, 0)
		amount += 1
		letter_counts[char] = amount

	return letter_counts

### End Helper Functions ###

start = timeit.default_timer()
old_code = main_code

#Build 20 turn dictionary -- CURRENTLY INCLUDES EDGES, MIDDLE EDGE REPEATS BETWEEN CODE 1 AND CODE 2
twenty_turn_codes = {}
print("Creating 20 turn codes...")
for code in codes:
	print(code)
	new_code = code
	for i in range(20):
		new_code = find_new_code(new_code, codes)

	code_count = get_counts(new_code)

	twenty_turn_codes[code] = {
		"old_code" : code,
		"code" : new_code,
		"count" : code_count,
		"first_letter" : code[0],
		"last_letter" : code[1]
	}

print("Done")

# Use starting code and create a list of codes after 20 turns that need to be checked
# "abc" => [20Turn[ab], 20Turn[bc]]

code_after_twenty_turns = []
for i in range(len(old_code[:-1])): #Don't want to check final letter
	code = old_code[i:i+2]
	expanded_code = twenty_turn_codes.get(code, "")
	code_after_twenty_turns.append(expanded_code)

# Codes are now too large to effeciently join, use char counts only
final_char_count = {}
for j in range(len(code_after_twenty_turns)):
	code = code_after_twenty_turns[j]
	long_code = code["code"]


	# For each of the longer codes, analyze the 2 character codes and add the 
	# characters that would appear after 20 turns
	for i in range(len(long_code[:-1])):
		next_code = long_code[i:i+2]
		code_after_twenty = twenty_turn_codes[next_code]

		counts = code_after_twenty["count"]
		for letter in counts:
			letter_count = final_char_count.get(letter, 0)
			letter_count += counts[letter]
			final_char_count[letter] = letter_count

		# Middle sections create an extra "first letter"
		if i != 0 or j != 0:
			first_letter = next_code[0]
			letter_count = final_char_count.get(first_letter, 0)
			letter_count -= 1
			final_char_count[first_letter] = letter_count

for letter in final_char_count:
	print(letter, " - ", final_char_count[letter])

# Sort count to get the largest and smallest values
count_list = []
for letter in sorted(final_char_count.values()):
	count_list.append(letter)

ans = count_list[-1] - count_list[0]
print("ANS: ", ans)

stop = timeit.default_timer()

print('Time: ', stop - start)
