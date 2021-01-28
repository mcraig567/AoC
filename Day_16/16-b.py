from copy import deepcopy

limits = {}
my_ticket = []
nearby_tickets = []

f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_16\input.txt", "r")

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
            desc = words[0]
            limits[desc] = [(int(lower[0]), int(lower[1])), (int(upper[0]), int(upper[1])), None] #[(lower), (upper), position]

        words = words[0].split(",")
        if self_ticket and len(words) > 2: #Don't want the initial line "your ticket:"
            for value in words:
                my_ticket.append(int(value))

        if other_ticket and len(words) > 2: #Don't want initial line
            """For all ticket values in one list"""
            # for value in words:
            #     nearby_tickets.append(int(value))

            """For list of tickets in nearby_tickets"""
            ind_ticket = []
            for value in words:
                ind_ticket.append(int(value))
            nearby_tickets.append(ind_ticket)

f.close()

#Discard any invalid tickets
def check_validity(nearby_tickets, limits):
    invalid_numbers = []
    invalid_tickets = []

    for i in range(len(nearby_tickets)):
        for value in nearby_tickets[i]:
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
                invalid_tickets.append(i)

    return invalid_numbers, invalid_tickets

def find_valid_spots(ticket, limits):
    spots = {} #[possible, not possible]
    for i in range(len(ticket)):
        value = ticket[i]
        possible = []
        not_possible = []

        for key in limits:
            lower = limits[key][0]
            upper = limits[key][1]
            position = limits[key][2]

            if (lower[0] <= value <= lower[1] or upper[0] <= value <= upper[1]) and len(position) > 1:
                possible.append(key)

            elif len(position):
                not_possible.append(key)

        spots[i] = [spots.get(i, [[],[]])[0] + possible, spots.get(i, [[],[]])[1] + not_possible]

    return spots

def remove_spots(index, limits, not_possible):
    """Takes index and removes spot index from any keys in not_possible""" 
    for key in not_possible:
        if len(limits[key][2]) == 1:
            pass
        else:
            if index in limits[key][2]:
                limits[key][2].remove(index)

                #Can only be in one spot - can remove from all others
                if len(limits[key][2]) == 1:
                    all_keys = list(limits.keys())
                    all_keys.remove(key)
                    lone_spot = limits[key][2][0]

                    remove_spots(lone_spot, limits, all_keys)

    return None
        




in_num, in_tick = check_validity(nearby_tickets, limits)
           
ticket_copy = deepcopy(nearby_tickets)
for index in in_tick:
    ticket_copy.remove(nearby_tickets[index])
nearby_tickets = ticket_copy

#Ensure that there are no more invalid tickets, both should be empty lists
#in_num_check, in_tick_check = check_validity(nearby_tickets, limits)

#All keys can be in all spots, assign to all keys
possible = []
for i in range(len(nearby_tickets[0])):
    possible.append(i)

for key in limits.keys():
    limits[key][2] = deepcopy(possible)

#Start removing spots from keys, based on not_possible
for i in range(len(nearby_tickets) + 1):
    for ticket in nearby_tickets:
        spots = find_valid_spots(ticket, limits)

        for spot in spots.keys():
            not_possible = spots[spot][1]
            remove_spots(spot, limits, not_possible)
           
"""Checking to validate test input"""
print(limits)
print(f"Class: {limits['class'][2]}, my ticket: {my_ticket[limits['class'][2][0]]}")
print(f"Row: {limits['row'][2]}, my ticket: {my_ticket[limits['row'][2][0]]}")
print(f"Seat: {limits['seat'][2]}, my ticket: {my_ticket[limits['seat'][2][0]]}")

departure_spots = []
for key in limits:
    if "departure" in key:
        departure_spots.append(limits[key][2][0])

product = 1
for spot in departure_spots:
    product *= my_ticket[spot]
print(departure_spots)
print(f"The product is {product}")