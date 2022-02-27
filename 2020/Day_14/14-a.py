
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

mem = {}

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_14\input.txt", "r")

for line in f:
    info = line.split(" = ")

    if info[0] == "mask":
        #print("Mask")
        mask = info[1]
        #print(mask)
        #print()
    else:
        #print("Mem")
        index = int(info[0][4:-1])
        amount = int(info[1])
        #print(f"mem[{index}] = {amount}")
        #print()

        #Convert to binary list
        binary = to_binary(amount)

        #Apply mask
        for i in range(len(mask)):
            if mask[i] == '1':
                binary[i] = 1
            elif mask[i] == '0':
                binary[i] = 0

        #Return to decimal and update dict
        decimal = to_dec(binary)
        mem[index] = decimal

f.close()

#Calculate sum of all entries in mem
total = 0
for value in mem.values():
    total += value

print(f"The total is {total}")




# x = to_binary(10)
# print(x)
# print("and back")
# x = to_dec(x)
# print(x)

