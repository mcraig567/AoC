"""PRODUCTION"""
CARD_PUBLIC = 16915772
DOOR_PUBLIC = 18447943
"""END PRODUCTION"""

"""TESTING"""
# CARD_PUBLIC = 5764801
# DOOR_PUBLIC = 17807724
"""END TESTING"""

SUBJECT_NUMBER = 7
MOD = 20201227

#Get card loop size
card = 1
card_loop = 0
while card != CARD_PUBLIC:
    card = card * SUBJECT_NUMBER
    card = card % MOD
    card_loop += 1

print(f"Card Loop: {card_loop}")

#Get door loop size
door = 1
door_loop = 0
while door != DOOR_PUBLIC:
    door = door * SUBJECT_NUMBER
    door = door % MOD
    door_loop += 1

print(f"Door Loop: {door_loop}")
print()

#Get encryption key from card
card_encryption = 1
for i in range(card_loop):
    card_encryption = card_encryption * DOOR_PUBLIC
    card_encryption = card_encryption % MOD

print(f"Card Encryption: {card_encryption}")

#Get encryption key from door
door_encryption = 1
for i in range(door_loop):
    door_encryption = door_encryption * CARD_PUBLIC
    door_encryption = door_encryption % MOD

print(f"Door Encryption: {door_encryption}")

#Ensure that the two encryption keys are the same
if card_encryption == door_encryption:
    check = True
else:
    check = False
print(f"Same Check: {check}")
print()
