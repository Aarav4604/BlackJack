"""
===============================================================================
ENGR 13300 Fall 2022

Program Description
    User plays Black jack one on one against computer

Assignment Information
    Assignment:     Individual Project
    Author:         Aarav Patel
    Team ID:        LC1 -18

Contributor:
    My contributor(s) helped me:
    [x ] understand the assignment expectations without
        telling me how they will approach it.
    [x ] understand different ways to think about a solution
        without helping me plan my solution.
    [x ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""
import random
import sys
import time

from UDF_getMove import getMove as move

# Set up the constants:
HEARTS = chr(9829)  # Character 9829 is '♥'.
DIAMONDS = chr(9830)  # Character 9830 is '♦'.
SPADES = chr(9824)  # Character 9824 is '♠'.
CLUBS = chr(9827)  # Character 9827 is '♣'.
HIDDEN = 'hidden'
#color constants
color = '\33[31m'
reset = '\033[0m'
CVIOLETBG = '\33[45m'
CWHITE = '\33[37m'
CWHITE2 = '\33[97m'
bold = '\033[01m'
CRED2 = '\33[91m'
CBLACK = '\33[30m'
CBLUE = '\33[34m'
CVIOLET = '\33[35m'
CYELLOW = '\33[33m'
CBLACKBG = '\33[40m'

def userbet(moneybet):
    maxbet = input('How much do you want to bet? (1-{})'.format(moneybet))

    while maxbet.isdigit()==False: #error checking
        maxbet= input('How much do you want to bet? (1-{})'.format(moneybet))

    maxbet = int(maxbet)

    while maxbet > moneybet or maxbet < 1:
        maxbet = int(input('How much do you want to bet? (1-{})'.format(moneybet)))

    return maxbet

def getCards():
    cards = []

    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for num in range(2, 11):
            cards.append((str(num), suit))  # Add the numbered cards.

        for num in ('J', 'Q', 'K', 'A'):
            cards.append((num, suit))  # Add the face and ace cards.
    random.shuffle(cards)
    return cards

def determine_hand(dealerHand, playerHand, factor):
    if factor:
        print(CRED2 + "\nDealer's Cards: " + reset)
        showCards(dealerHand)
        print("Dealer's Current Total: ", CalcValue(dealerHand))

    else:
        print(CRED2 + "\nDealer's Cards: " + reset)
        showCards([HIDDEN] + dealerHand[1:])

    print(CRED2 + "\nPlayer's Cards: " + reset)
    showCards(playerHand)
    print("Player's Current Total: ", CalcValue(playerHand))

def showCards(hand):
    rows = ['', '', '', '', '', '', '']  # The text to display on each row.

    for i, h in enumerate(hand):
        rows[0] += ' ________  '  # Print the top line of the card.
        if h == HIDDEN:
            # Print a card's back:
            rows[1] += '|####### | '
            rows[2] += '|########| '
            rows[3] += '|########| '
            rows[4] += '|########| '
            rows[5] += '| #######| '
            rows[6] += ' --------  '

        else:
            # Print the card's front:
            rank, suit = h  # The card is a tuple data structure.

            #check the suit and colors
            if suit == SPADES:
                c = CBLACK
            if suit == HEARTS:
                c = CRED2
            if suit == CLUBS:
                c = CBLACK
            if suit == DIAMONDS:
                c = CRED2
            rows[1] += '|{}      | '.format(CBLUE + rank.ljust(2) + reset)
            rows[2] += '|        | '
            rows[3] += '|   {}    | '.format(c + suit + reset)
            rows[4] += '|        | '
            rows[5] += '|      {}| '.format(CBLUE + rank.rjust(2, ' ') + reset)
            rows[6] += ' --------  '

    # Print each row on the screen:
    time.sleep(1)
    for row in rows:
        time.sleep(0.05)
        print(row)

def CalcValue(hand):
    value = 0
    ace = 0
    for i in hand:
        num = i[0] #storing num of first element
        if num == 'A':
            ace += 1
            value += 1

        elif num in ('J', 'Q', 'K'): #face cards
            value += 10

        else:
            value += int(num)

    if (value + 10) <= 21 and ace >= 1: #check if aces exist
        value += 10

    return value

def main():
    count = 1
    money = 3000

    while count == 1: #to play again
        if money == 0: #ran out of money
            print("\nOOPS, You're Out Of Money ")
            print("Better Luck Next Time ")
            print("Run the program again to play the game")
            sys.exit()
        print("")
        string = 'BlackJack game by Aarav Patel'
        for char in string:
            print(char, end='')
            time.sleep(0.20)

        print('''\nRules:
               Get 21 without getting wasted. 
               Kings, Queens, and Jacks are all worth 10 points. 
               Aces are worth 1 or 11 points.
    
               (H)it to take another card.
               (S)tand to stop taking cards.
               In case of a tie, the bet is returned to the player.''')

        # User enters their bet for this round:
        print("\nMoney: ", money)
        bet = userbet(money)

        deck = getCards() #calling function getCards
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        print("The Pot: ", bet + bet)
        determine_hand(dealerHand, playerHand, False)

        while True:
            if CalcValue(playerHand) > 21: #busted
                break

            choice = move(playerHand, money - bet)

            if choice == 'H':
                newcard = deck.pop() #getting an extra card
                num, suit = newcard
                print('You drew a {} of {}'.format(num, suit))
                time.sleep(2) #wait block
                playerHand.append(newcard)
                print(CRED2 + "\nPlayer's Cards: " + reset)
                showCards(playerHand)
                print("Player's Current Total: ", CalcValue(playerHand))
                continue

            if choice == 'S':
                break

        if CalcValue(playerHand) <= 21:
            while CalcValue(dealerHand) < CalcValue(playerHand):
                print('Dealer hits...')
                time.sleep(2)
                dealerHand.append(deck.pop())
                print(CRED2 + "\nDealer's Cards: " + reset)
                showCards([HIDDEN] + dealerHand[1:])

                if CalcValue(dealerHand) > 21:
                    break

        # SHOW CARDS:
        time.sleep(1.5)
        print("LETS REVEAL THE CARDS")
        time.sleep(1)
        input("To continue please press enter")
        determine_hand(dealerHand, playerHand, True)
        final_player_val = CalcValue(playerHand)
        final_dealer_val = CalcValue(dealerHand)

        time.sleep(1)
        if final_player_val > 21:
            print(CBLACKBG + CWHITE2 + "BUSTED " + reset)
            print("YOU LOSE" + reset)
            money -= bet

        elif final_player_val < final_dealer_val < 21:
            print(CBLACKBG + CWHITE2 + "DEALER WINS" + reset)
            print("YOU LOST" + reset)
            money -= bet

        elif final_player_val < final_dealer_val and final_dealer_val > 21:
            print(CBLACKBG + CWHITE2 + "DEALER BUSTED " + reset)
            print(CBLACKBG + CWHITE2 + "YOU WIN" + reset)
            money += bet

        elif final_player_val == final_dealer_val:
            print("It's a tie, the bet is returned to you.")

        elif final_player_val < final_dealer_val == 21:
            print(CBLACKBG + CWHITE2 + "DEALER WINS " + reset)
            print("YOU LOSE" + reset)
            money -= bet

        if money != 0:
            repeat = input("Do you want to play again Y/N").upper().strip()
            if repeat == 'Y':
                count = 1
            else:
                count = 0
                print("Run the program again to play the game")
        else:
            count = 1

if __name__ == '__main__':
    main()
