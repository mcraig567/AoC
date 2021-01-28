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

def calculate_score(hand):
    score = 0
    for i in range(len(hand)):
        score += hand[i] * (len(hand) - i)
        print(f"{hand[i]} * {len(hand) - i}")

    return score


def play_game(hand1, hand2, game):
    turn = 1
    game_hands = {} #key = hand1, value = [hand2]
    # print(f"== Game {game} ==")
    # print()
    while min(len(hand1), len(hand2)) != 0:
        # print(f"-- Round {turn} (Game {game} --")
        # print(f"Player 1's deck: {hand1}")
        # print(f"Player 2's deck: {hand2}")
        
        #See if this combination of hands has already been played
        #Turn hand 1 into a string so can hash
        h1_string = ""
        for char in hand1:
            h1_string += str(char)

        hand2_opts = game_hands.get(h1_string, [])
        for option in hand2_opts:
            if hand2 == option:
                #Seen this hand already, Player 1 wins
                #print("We've already seen this hand! P1 Wins!")
                return 1, [hand1, hand2]

        #Haven't seen, add to dictionary
        hand2_opts.append(hand2)
        game_hands[h1_string] = hand2_opts

        p1 = hand1.pop(0)
        p2 = hand2.pop(0)
        # print(f"Player 1 plays: {p1}")
        # print(f"Player 2 plays: {p2}")

        #Recurse into another game to determine winner of hand
        if p1 <= len(hand1) and p2 <= len(hand2):
            #print("Playing a sub-game to determine the winner...")
            winner, hands = play_game(hand1[:p1], hand2[:p2], game + 1)

            #print(f"...anyway, back to game {game}")
            #print(f"Player {winner} wins round {turn} of game {game}")
            if winner == 1:
                hand1.append(p1)
                hand1.append(p2)
            else:
                hand2.append(p2)
                hand2.append(p1)

        elif p1 > p2: #Player one wins
            #print(f"Player 1 wins round {turn} of game {game}!")
            hand1.append(p1)
            hand1.append(p2)
        else:       #Player 2 wins
            #print(f"Player 2 wins round {turn} of game {game}!")
            hand2.append(p2)
            hand2.append(p1)
        #print()
        turn += 1

    if len(hand1) > len(hand2):
        winner = 1
    else:
        winner = 2
    #print(f"The winner of game {game} is Player {winner}!")
    #print()
    return winner, [hand1, hand2]

winner, hands = play_game(hands[0], hands[1], 1)

if hands[0]:
    score = calculate_score(hands[0])
else:
    score = calculate_score(hands[1])

print(f"Player {winner} wins with a score of {score}!")