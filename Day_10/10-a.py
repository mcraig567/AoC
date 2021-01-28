
adapters = []

def read_lines(adapters):
    f = open("C:\\Users\craig\Documents\AoC\Day_10\Input.txt", "r")

    for line in f:
        adapters.append(int(line))

    f.close()

    adapters.sort()

    return adapters

adap = read_lines(adapters)

one = 0
three = 1 #Device to adapter, so start at one

for i in range(len(adap)):
    if i == 0:
        if adap[i] == 1:
            one += 1

        elif adap[i] == 3:
            three += 1

    else:
        if adap[i] - adap[i - 1] == 1:
            one += 1

        elif adap[i] - adap[i - 1] == 3:
            three += 1

print(f"One: {one}")
print(f"Three: {three}")
print(f"Product: {one * three}")




