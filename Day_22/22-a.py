f = open("C:\\Users\craig\OneDrive\Documents\AoC\Day_22\input.txt", "r")
hands = []
for line in f:
    line = line.strip()
    line = line.split()
    if not line:
       hands.append(hand)
   
    elif line[0] == "Player":
       hand = []

    else:
        hand.append(int(line[0]))

f.close()

print(hands)

def calculate_score(hand):
    score = 0
    for i in range(len(hand)):
        score += hand[i] * (len(hand) - i)
        print(f"{hand[i]} * {len(hand) - i}")

    return score



turn = 1
while min(len(hands[0]), len(hands[1])) != 0:
    print(f"-- Round {turn} --")
    print(f"Player 1's deck: {hands[0]}")
    print(f"Player 2's deck: {hands[1]}")
    
    p1 = hands[0].pop(0)
    p2 = hands[1].pop(0)
    print(f"Player 1 plays: {p1}")
    print(f"Player 2 plays: {p2}")

    if p1 > p2: #Player one wins
        print("Player 1 wins the round!")
        hands[0].append(p1)
        hands[0].append(p2)
    else:       #Player 2 wins
        print("Player 2 wins the round!")
        hands[1].append(p2)
        hands[1].append(p1)
    print()

    turn += 1

print(hands)

if hands[0]:
    score = calculate_score(hands[0])
else:
    score = calculate_score(hands[1])

print(f"Winning Score is {score}!")