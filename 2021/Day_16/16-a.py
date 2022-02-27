import timeit
import copy

with open("Input.txt", "r") as inputFile:
	for line in inputFile:
		code = line[:-1]

### Problem Parameters ###

HEXTOBIN = {
	"0": "0000",
	"1": "0001",
	"2": "0010",
	"3": "0011",
	"4": "0100",
	"5": "0101",
	"6": "0110",
	"7": "0111",
	"8": "1000",
	"9": "1001",
	"A": "1010",
	"B": "1011",
	"C": "1100",
	"D": "1101",
	"E": "1110",
	"F": "1111"
}

### End Problem Parameters ###

### Helper Functions ###

def bin_to_dec(digit):
	"""Takes a binary number as a string, returns a base 10 integer"""
	exponent = 0
	dec_digit = 0
	while digit:
		last_digit = digit[-1]
		dec_digit += (2 ** exponent) * int(last_digit)
		exponent += 1
		digit = digit[:-1]

	return dec_digit

def convert_hex_to_bin_string(hex_string):
	bin_to_join = []
	for hex_char in hex_string:
		bin_to_join.append(HEXTOBIN[hex_char])

	bin_string = "".join(bin_to_join)
	return bin_string

def get_version(bin_string):
	bin_version = bin_string[0:3]
	return bin_to_dec(bin_version)

def get_type_id(bin_string):
	bin_id = bin_string[3:6]
	return bin_to_dec(bin_id)

def get_length_id(bin_string):
	length_id = bin_string[6]
	return length_id

def string_is_zeroes(bin_string):
	for char in bin_string:
		if char != "0":
			return False

	return True

def get_literal_packets(bin_string):
	"""For use with literal values (ID: 4)"""
	if get_type_id(bin_string) != 4:
		return False

	# Strip off first 6 digits - they're for Version & ID
	stripped_string = bin_string[6:]
	first_digit = stripped_string[0]
	packets = []

	while first_digit == "1":
		packets.append(stripped_string[1:5])
		stripped_string = stripped_string[5:]
		first_digit = stripped_string[0]

	# Exits when first digit = 0, repeat one last time
	packets.append(stripped_string[1:5])

	return packets

def handle_packet(bin_string):
	"""Requires that the string being entered is the beginning of the new packet"""
	version = get_version(bin_string)
	#print("Version: ", version)
	type_id = get_type_id(bin_string)

	if type_id == 4:
		#print("Literal Packet")
		packets = get_literal_packets(bin_string)
		length = 6 + 5 * len(packets)
		#print("Packet Length is: ", length)

		bin_string = bin_string[length:]

	else:
		length_id = get_length_id(bin_string)
		subpacket_values = []

		# First get values of all subpackets
		if length_id == "0":
			#print("Length ID = 0")
			subpacket_length_bin = bin_string[7:22]
			total_subpacket_length = bin_to_dec(subpacket_length_bin)

			subpackets = bin_string[22 : 22 + total_subpacket_length]
			while subpackets:
				subpackets, version_sum = handle_packet(subpackets)
				subpacket_values.append(version_sum)

			total_length = 6 + 1 + 15 + total_subpacket_length # 3(version) + 3(typeID) + 1(lengthID) + 15(binary subpacket length)
			bin_string = bin_string[total_length:]

		elif length_id == "1":
			num_subpackets = bin_to_dec(bin_string[7:18])
			bin_string = bin_string[18:]
			for i in range(num_subpackets):
				bin_string, sub_version = handle_packet(bin_string)
				subpacket_values.append(sub_version)
		
		# Now use the type of operator to determine how to use values
		if type_id == 0:
			version = sum(subpacket_values)

		elif type_id == 1:
			version = 1
			for value in subpacket_values:
				version *= value

		elif type_id == 2:
			version = min(subpacket_values)

		elif type_id == 3:
			version = max(subpacket_values)

		elif type_id == 5:
			if subpacket_values[0] > subpacket_values[1]:
				version = 1
			else:
				version = 2

		elif type_id == 6:
			if subpacket_values[0] < subpacket_values[1]:
				version = 1
			else:
				version = 2

		elif type_id == 7:
			if subpacket_values[0] == subpacket_values[1]:
				version = 1
			else:
				version = 2			

	return bin_string, version

### End Helper Functions ###

start = timeit.default_timer()
version_sum = 0

bin_string = convert_hex_to_bin_string(code)
while bin_string:	
	bin_string, version_sum = handle_packet(bin_string)
	if string_is_zeroes(bin_string):
		break

print("DONE - ", version_sum)


stop = timeit.default_timer()

print('Time: ', stop - start)
