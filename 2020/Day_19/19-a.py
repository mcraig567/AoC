f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_19\input.txt", "r")

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
    
messages.pop(0) #First entry is the blank line, remove it

f.close()

def check_rules(message, rule):
    """Recursively dig through the rules to see if the message matches the initial rules"""

    rule_type = rule[0]

    if rule_type == "LETTER":
        if message[0] == rule[1]:
            remainder = message[1:] #Remove good letter from message       
            return True, remainder
        else:
            return False, message

    elif rule_type == "RULE":
        remainder = message
        for i in rule[1]:
            check, remainder = check_rules(remainder, rules[i])
            if not check:
                return False, message #Back up if failure

        return True, remainder

    else: #OR rule
        remainder = message
        for i in rule[1]:
            check, remainder = check_rules(remainder, ('RULE', i))
            if check:          
                return True, remainder

        return False, message

total = 0           
for message in messages:
    check, remainder = check_rules(message, rules['0'])

    if len(remainder) != 0:
        check = False

    if check == True:
        total += 1

print()
print(f"There are {total} passing messages")
