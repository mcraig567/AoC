
limits = {}
ticket = []
nearby_tickets = []
invalid_numbers = []
invalid_sum = 0

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_16\inputtest2.txt", "r")

#Start with recording limits
limit = True
self_ticket = False
other_ticket = False

#Currently go through each ticket number, and will need to 
#go through tickets a second time to check validity. Would
#it be faster to perform check for validity on initial access?
for line in f:
    words = line.split()
    if len(words) > 0:
        if words[0] == "your":
            self_ticket = True
            limit = False
            other_ticket = False

        elif words[0] == "nearby":
            self_ticket = False
            limit = False
            other_ticket = True

        if limit:
            words = line.split(": ")
            lim = words[1].split()

            lower = lim[0].split("-")
            upper = lim[2].split("-")
            desc = words[0][:-1]
            limits[desc] = [(int(lower[0]), int(lower[1])), (int(upper[0]), int(upper[1]))]

        words = words[0].split(",")
        if self_ticket and len(words) > 2: #Don't want the initial line "your ticket:"
            for value in words:
                ticket.append(int(value))

        if other_ticket and len(words) > 2: #Don't want initial line
            """For all ticket values in one list"""
            for value in words:
                nearby_tickets.append(int(value))

            """For list of tickets in nearby_tickets"""
            # ind_ticket = []
            # for value in words:
            #     ind_ticket.append(int(value))
            # nearby_tickets.append(ind_ticket)

f.close()

for value in nearby_tickets:
    valid = True
    for key in limits:
        lower = limits[key][0]
        upper = limits[key][1]

        if lower[0] <= value <= lower[1] or upper[0] <= value <= upper[1]:
            valid = True #May find valid criteria on second check
            break

        else:
            valid = False

    if not valid:
        invalid_numbers.append(value)
        invalid_sum += value

total = 0
for number in invalid_numbers:
    total += number

print(f"Invalid Numbers: {invalid_numbers}")
print(f"Sum: {total}")
print()
print(f"Other sum: {invalid_sum}")