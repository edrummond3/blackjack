# game.py>
"""
Blackjack Game (Console)
"""
import os
import random

mode = "console"

# Card, has suit and value
class Card:
    def __init__(self, s="", v=""):
        self.suit = s
        self.value = v

# Standard 52-card deck, gets built and shuffled whenever instantialized
class Deck:
    def __init__(self):
        self.decklist = []
        suits = ["♣", "♦", "♥", "♠"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        for s in range(4):
            for v in range(13):
                card = Card(suits[s], values[v])
                self.decklist.append(card)
        random.shuffle(self.decklist)

# Dealer, has hand (of cards)
class Dealer:
    def __init__(self):
        self.hand = []

# Player, has hand (of cards) and chips.  Chips default value is 50
class Player:
    def __init__(self):
        self.hand = []
        self.chips = 50

# Returns the given person's hand as a readable string
def getHand(person):
    handString = ""
    for c in person.hand:
        handString += "[" + c.value + c.suit + "] "
    return handString

# Prints the given person's hand
def printHand(person):
    for c in person.hand:
        print("[" + c.value + c.suit + "]", end=" ")

# Calculates the score of the given person's hand.  By normal Blackjack rules aces are worth
# 1 or 11, face cards are worth 10, and all other cards are worth their numeric value
def calculateHand(person):
    handScore = 0
    hasAce = False # checks if the hand contains an ace
    for c in person.hand:
        if c.value == "A":
            if hasAce or handScore+11 > 21:
                handScore += 1
            else:
                handScore += 11
                hasAce = True
        elif c.value == "K" or c.value == "Q" or c.value == "J":
            if hasAce and handScore+10 > 21:
                hasAce = False
                pass
            else:
                handScore += 10
        else:
            if hasAce and handScore+int(c.value) > 21:
                handScore -= 10 - int(c.value)
                hasAce = False
            else:
                handScore += int(c.value)
    return handScore

# Main game loop
def playGame():
    dealer = Dealer()
    player = Player()
    while(1):
        deck = Deck()
        dealer.hand = []
        player.hand = []
        i = 0       # Reads cards from the deck (cards are not actually added or removed)

        # Deal
        for j in range(2):
            dealer.hand.append(deck.decklist[i])
            i += 1
        for j in range(2):
            player.hand.append(deck.decklist[i])
            i += 1
        print("Dealer: ??", dealer.hand[1].value + dealer.hand[1].suit)
        print("Player:", end=" ")
        printHand(player)
        print("\nChips: ", player.chips, end=" ")
        
        # Player Phase
        if calculateHand(player) == 21:
            print("Blackjack!")
        else:
            while calculateHand(player) < 21:
                print("\n[H]it, [S]tand, or [Q]uit? : ", end=" ")
                input2 = input().lower()
                if input2 == "h":
                    player.hand.append(deck.decklist[i])
                    i += 1
                    print("Player:", end=" ")
                    printHand(player)
                    if calculateHand(player) == 21:
                        print("Blackjack!")
                        break
                    if calculateHand(player) > 21:
                        print("Bust!")
                        break
                elif input2 == "s":
                    break
                elif input2 == "q":
                    return
                else:
                    print ("Invalid command.")
                    
        # Dealer Phase
        # Dealer must hit 16 and stand on all 17
        if calculateHand(player) <= 21:
            print("Dealer:", end=" ")
            printHand(dealer)
            if calculateHand(dealer) >= 17:
                print("Dealer stands...")
            while calculateHand(dealer) < 17:
                print("Dealer hits...")
                dealer.hand.append(deck.decklist[i])
                i += 1
                print("Dealer:", end=" ")
                printHand(dealer)
                if calculateHand(dealer) > 21:
                    print("Dealer busts!")
                    break
                if (calculateHand(dealer) >= 17):
                    print("Dealer stands...")
            print("Player:", end=" ")
            printHand(player)
            
        # Winner decided
        if calculateHand(player) > 21:
            print("Dealer wins!")
            player.chips -= 1
        elif calculateHand(dealer) > 21:
            print("You win!")
            player.chips += 2
        elif calculateHand(player) < calculateHand(dealer):
            print("Dealer wins!")
            player.chips -= 1
        elif calculateHand(player) > calculateHand(dealer):
            print("You win!")
            player.chips += 2
        else:
            print("Tie!")

        # Record statistics to a text file
        with open("statistics.txt", "r") as reader:
            stats = reader.readlines()
            gamesPlayed = stats[0][stats[0].find(" ")+1:stats[0].find("\n")]
            gamesPlayed = str(int(gamesPlayed)+1)
            stats[0] = stats[0][0:stats[0].find(" ")+1]+gamesPlayed+"\n"
            chipsHiScore = stats[1][stats[1].find(" ")+1:stats[1].find("\n")]
            if player.chips > int(chipsHiScore):
                stats[1] = stats[1][0:stats[1].find(" ")+1]+str(player.chips)+"\n"
        with open("statistics.txt", "w") as writer:
            writer.write(stats[0])
            writer.write(stats[1])

        # Play again?
        print("[P]lay again? or [Q]uit :", end=" ")
        input2 = input().lower()
        while(input2 != "p"):
            if input2 == "q":
                print("Quitting to main menu...")
                return
            else:
                print ("Invalid command.")
                input2 = input().lower()

# Reads and prints game statistics from a text file
def getStatistics():
    print ("Statistics")
    with open("statistics.txt", "r") as reader:
            stats = reader.readlines()
            print(stats[0], end="") 
            print(stats[1], end="")

def main():
    while(1):
        print("Blackjack Game\nWritten by Eric Drummond")
        print("[P]lay, View [S]tatistics, [Q]uit :", end=" ")
        input1 = input().lower()
        if input1 == "p":
            playGame()
        elif input1 == "s":
            getStatistics()
        elif input1 == "q":
            print ("Quitting...")
            return
        else:
            print ("Invalid command.")
  
    
if __name__ == "__main__":
    main()
