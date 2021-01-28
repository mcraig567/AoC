f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_19\input2.txt", "r")

rules_check = True
rules = {} #Entry is [type, requirement]
messages = []

for line in f:
    line = line.strip()
    if line == "":
        rules_check = False

    if rules_check:
        line_split = line.split(": ")

        #Clean up rules
        if '"' in line_split[1]:
            line_split[1] = line_split[1].strip('"')
            rules[line_split[0]] = ("LETTER", line_split[1])

        elif "|" in line_split[1]:
            halves = line_split[1].split(" | ")
            halves[0] = halves[0].split(" ")
            halves[1] = halves[1].split(" ")
            rule = [halves[0], halves[1]]
            rules[line_split[0]] = ("OR", rule)

        else:
            rule = line_split[1].split(" ")
            rules[line_split[0]] = ("RULE", rule)

    else:
        messages.append(line)
    
messages.pop(0) #First entry is the blank line

f.close()

def get_remainders_42(message):
    remainders = []
    check = True
    remainder = message
    i = 0
    while check:
        check, remainder = check_rules(remainder, rules['42'], '42') #Run one pass of loop with rule 42       
        if check:
            remainders.append((remainder, i))
        i += 1

    return remainders

def check_31(message):
    check = True
    remainder = message
    remainders = []
    i = 0
    while check:
        check, remainder = check_rules(remainder, rules['31'], '31') #Run one pass of loop with rule 31
        remainders.append(remainder)
        if check and len(remainder) == 0:
            return True, i
        i += 1
    return False, i


def check_rules(message, rule, parent):
    rule_type = rule[0]
    remainder = message

    if rule_type == "LETTER":
        if len(message) == 0: #If checking an empty string, automatically will fail
            return False, message

        if message[0] == rule[1]:
            remainder = message[1:] #Remove good letter from message
            return True, remainder
        else:
            return False, message

    elif rule_type == "RULE":
        for i in rule[1]:
            check, remainder = check_rules(remainder, rules[i], i)
            if not check:
                return False, message
        return True, remainder

    else: #OR rule
        for i in rule[1]:
            check, remainder = check_rules(remainder, ('RULE', i), parent)
            if check:        
                return True, remainder
        return False, message


#Run through all messages and see which are valid
total = 0           
for message in messages:
    remainders = get_remainders_42(message)
    for remainder in remainders:
        iters_42 = remainder[1]
        second_check, iters_31 = check_31(remainder[0])

        if second_check and iters_31 < iters_42:
            total += 1
            break #If one remainder passes, the message passes. Don't want to overcount

print()
print(f"There are {total} passing messages")
