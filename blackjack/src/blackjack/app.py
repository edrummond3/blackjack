"""
Blackjack Game
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
# from game import *
import random
import sys
import os

class Blackjack(toga.App):

    # build main menu
    def startup(self):
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.game_box = toga.Box(style=Pack(direction=COLUMN))
        self.app_box = toga.Box('app_box', children=[self.main_box, self.game_box])
        
        title = toga.Label('Blackjack', style=Pack(padding=(0, 5)))
        author = toga.Label('Written by Eric Drummond', style=Pack(padding=(0, 5)))

        title_box = toga.Box(style=Pack(direction=ROW, padding=5, text_align=CENTER))
        title_box.add(title)
        title_box.add(author)

        playButton = toga.Button('Play', on_press=self.playButton, style=Pack(padding=5))
        quitButton = toga.Button('Quit', on_press=self.quit, style=Pack(padding=5))

        self.app_box.add(self.main_box)
        self.main_box.add(title_box)
        self.main_box.add(playButton)
        self.main_box.add(quitButton)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.app_box
        self.main_window.show()
        
    def playButton(self, button):
        self.playGame()

    def playGame(self):
        self.app_box.remove(self.main_box)
        self.dealer = Dealer()
        self.player = Player()
        self.deck = Deck()
        self.dealer.hand = []
        self.player.hand = []
        self.i = 0       # Reads cards from the deck (cards are not actually added or removed)

        # Deal
        for j in range(2):
            self.dealer.hand.append(self.deck.decklist[self.i])
            self.i += 1
        for j in range(2):
            self.player.hand.append(self.deck.decklist[self.i])
            self.i += 1

        # Build game UI
        dealerText = toga.Label('Dealer', style=Pack(padding=(0, 5)))
        dealerCards_box = toga.Box(style=Pack(direction=COLUMN))
        self.dealerCards = toga.Label('[??] [' + self.dealer.hand[1].value + self.dealer.hand[1].suit + ']', style=Pack(padding=(0, 5)))
        playerText = toga.Label('Player', style=Pack(padding=(0, 5)))
        playerCards_box = toga.Box(style=Pack(direction=COLUMN))
        self.playerCards = toga.Label(getHand(self.player), style=Pack(padding=(0, 5)))

        self.buttons_box = toga.Box(style=Pack(direction=COLUMN))
        hitButton = toga.Button('Hit', on_press=self.hit, style=Pack(padding=5))
        standButton = toga.Button('Stand', on_press=self.stand, style=Pack(padding=5))
        quitButton = toga.Button('Quit', on_press=self.quit, style=Pack(padding=5))
             
        self.app_box.add(self.game_box)
        self.game_box.add(dealerText)
        self.game_box.add(dealerCards_box)
        dealerCards_box.add(self.dealerCards)
        
        self.game_box.add(playerText)
        self.game_box.add(playerCards_box)
        playerCards_box.add(self.playerCards)

        # If player has Blackjack, automatically passes to dealer.  Otherwise, the player may Hit
        if calculateHand(self.player) == 21:
            self.dealerPhase()
        else:
            self.game_box.add(self.buttons_box)
            self.buttons_box.add(hitButton)
            self.buttons_box.add(standButton)
            self.buttons_box.add(quitButton)

    # Add a card to the player's hand
    def hit(self, button):
        self.player.hand.append(self.deck.decklist[self.i])
        self.playerCards.text = getHand(self.player)
        self.i += 1
        self.playerPhase()

    # Stop hitting and pass to the dealer
    def stand(self,button):
        self.dealerPhase()

    # Player can Hit, Stand, or Quit
    def playerPhase(self):
        if calculateHand(self.player) >= 21:
            self.dealerPhase()

    # Adds a card to the dealer's hand
    def dealerHit(self):
        self.dealer.hand.append(self.deck.decklist[self.i])
        self.dealerCards.text = getHand(self.dealer)
        self.i += 1
        self.dealerPhase()

    # Dealer can hit or stand.  Dealer must hit 16 and stand on all 17
    def dealerPhase(self):
        self.dealerCards.text = getHand(self.dealer)
        if calculateHand(self.player) <= 21:
            if calculateHand(self.dealer) >= 17:
                self.decideWinner()
            else:
                self.dealerHit()
        else:
            self.decideWinner()

    # Compares dealer and player's hand
    def decideWinner(self):
        if calculateHand(self.player) > 21:
            self.main_window.info_dialog('Blackjack', 'Dealer wins!')
            self.player.chips -= 1
        elif calculateHand(self.dealer) > 21:
            self.main_window.info_dialog('Blackjack', 'You win!')
            self.player.chips += 2
        elif calculateHand(self.player) < calculateHand(self.dealer):
            self.main_window.info_dialog('Blackjack', 'Dealer wins!')
            self.player.chips -= 1
        elif calculateHand(self.player) > calculateHand(self.dealer):
            self.main_window.info_dialog('Blackjack', 'You win!')
            self.player.chips += 2
        else:
            self.main_window.info_dialog('Blackjack', 'Tie!')

        # Removes Hit and Stand buttons, replaces them with Play Again button
        self.game_box.remove(self.buttons_box)
        self.playAgain_box = toga.Box(style=Pack(direction=COLUMN))
        self.game_box.add(self.playAgain_box)
        playAgainButton = toga.Button('Play Again', on_press=self.restart, style=Pack(padding=5))
        quitButton = toga.Button('Quit', on_press=self.quit, style=Pack(padding=5))
        self.playAgain_box.add(playAgainButton)

    # Restarts the program
    def restart(self, button):
        os.execl(sys.executable, sys.executable, *sys.argv)

    # Closes the program
    def quit(self, button):
        self.main_window.close()

def main():
    return Blackjack()



## Helper functions imported from game.py

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
