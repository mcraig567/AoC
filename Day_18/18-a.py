f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_18\inputtest.txt", "r")

equations = []

for line in f:
    equation = line[:-1] #If closed bracket is at end, would break
    equations.append(equation)
    # for char in line:
    #     if char == " ":
    #         pass
    #     elif char == "+" or char == "*":
f.close()

#print(equations)

def bracket_check(bracket_line):
    open_brackets = []
    bracket_pairs = []
    index = 0
    for char in bracket_line:
        if char == "(":
            open_brackets.append(index)
        elif char == ")":
            x = open_brackets.pop()
            bracket_pairs.append((x, index))
        index += 1

    bracket_pairs = sorted(bracket_pairs, key=lambda x: x[0], reverse=True)
    return bracket_pairs

def sum_line(in_line, start = 0, end = len(line)):
    in_line = in_line[start:end]
    in_line_split = in_line.split()
    number = int(in_line_split[0])
    operator = "+"
    for char in in_line_split[1:]:
        if char == "+":
            operator = "+"
        elif char == "*":
            operator = "*"
        else:
            if operator == "+":
                number += int(char)
            elif operator == "*":
                number *= int(char)
            else:
                print("OH NO THIS SHOULDNT EXIST")

    return number

total = 0
for eq in equations:
    eq_copy = eq
    print(eq_copy)
    pairs = bracket_check(eq)
    if pairs != []:
        for pair in pairs:
            difference = pair[1] - pair[0]

            x = str(sum_line(eq, pair[0] + 1, pair[1]))
            x_len = len(x)

            #Pad x with spaces to keep previous indexing correct
            #Will only work if number of digits smaller than space taken up by brackets
            if difference > x_len:
                for i in range(x_len, difference + 1):
                    x = x + " "
            else:
                print("OH NO BIG NUMBERS")

            #Splice in new x replacing the old brackets
            eq = eq[:pair[0]] + str(x) + eq[pair[1] + 1:]
            print(eq)

    eq_total = sum_line(eq, 0, len(eq))
    print(f"Line Total: {eq_total}")
    print()
    total += eq_total

#print()
print(f"The total is {total}")