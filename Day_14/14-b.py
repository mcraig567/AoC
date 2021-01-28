from copy import deepcopy


def to_binary(number):
    """Takes an integer and converts to a binary list of length 36
    (Leading zeroes as required)"""

    bin_num = []

    while number > 0:
        bin_num.append(number % 2)
        number = number // 2

    length = len(bin_num)
    #Update to 36 bits
    for i in range(length, 36):
        bin_num.append(0)

    bin_num.reverse()

    return bin_num

def to_dec(number):
    """Takes an array of 0s and 1s (binary number) and converts to base 10"""
    number.reverse()
    out = 0
    for i in range(len(number)):
        out += number[i] * 2 ** i

    return out

def make_float(binary, floaters, index):
    total = [binary]

    while index < len(floaters):
        temp = []
        for item in total:
            item[floaters[index]] = 0
            temp.append(deepcopy(item))
            item[floaters[index]] = 1
            temp.append(deepcopy(item))

        total = temp
        index += 1
    
    return total


mem = {}

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_14\input.txt", "r")

for line in f:
    info = line.split(" = ")

    if info[0] == "mask":
        mask = info[1]

    else:
        index = int(info[0][4:-1])
        amount = int(info[1])

        #Convert to binary list
        binary = to_binary(index)

        #Apply mask
        floater = []
        for i in range(len(mask) - 1):
            if mask[i] == '1':
                binary[i] = 1
            elif mask[i] != '0':
                floater.append(i)

        #First one will have all zeroes
        bin_list = make_float(binary, floater, 0)

        for item in bin_list:
            dec = to_dec(item)
            mem[dec] = amount

f.close()

#Calculate sum of all entries in mem
total = 0
for value in mem.values():
    total += value

print(f"The total is {total}")

