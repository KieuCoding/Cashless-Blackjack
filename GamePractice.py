import random
import time

# Simple game of blackjack
# 52 unique cards in a deck
# No money or betting in this version

class deck:
    def __init__(self):
        self.cards = [
            2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
            5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7,
            8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10,
            11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13,
            14, 14, 14, 14
        ]

    def answer(self, user):
        # .lower() is used for letter casing comparison
        if user.lower() in ["yes", "y"]:
            return True
        else:
            return False

    def shuffle(self, user):
        if user:
            random.shuffle(self.cards)
        return self.cards


class game:
    def __init__(self):
        self.deck = deck()
        self.player = []
        self.dealer = []

    def first_dealing(self):
        user_input = input("shuffle?(Yes/No)\ntype y or n : ")
        user = self.deck.answer(user_input)
        shuffle_deck = self.deck.shuffle(user)
        player = self.player
        dealer = self.dealer
        player.append(shuffle_deck[0])
        shuffle_deck.pop(0)
        dealer.append(shuffle_deck[0])
        shuffle_deck.pop(0)
        player.append(shuffle_deck[0])
        shuffle_deck.pop(0)
        dealer.append(shuffle_deck[0])
        shuffle_deck.pop(0)
        print("\nPlayer's deck: ", player)
        print("\nDealer's deck: [", dealer[0], ", face down ]")
        return shuffle_deck, player, dealer

    def PlayerAction(self, shuffle_deck, player, flag, surrender):
        hand_one = []
        hand_two = []
        print("\npick an action:\n1.) Hit\n2.) Double Down\n3.) Split\n4.) Stand\n5.) Surrender")
        user = int(input("\nPlease enter the corresponding action's number:"))
        if user == 1:
            player.append(shuffle_deck[0])
            shuffle_deck.pop(0)
            flag = 0
        elif user == 2:
            player.append(shuffle_deck[0])
            shuffle_deck.pop(0)
            flag = 1
        elif user == 3:
            if player[0] == player[1]:
                hand_one.append(player[0])
                hand_two.append(player[1])
                flag = 0
            else:
                user = int(input("\nNo pairs, pick another action:"))
            flag = 0
        elif user == 4:
            flag = 1
            pass
        elif user == 5:
            flag = 1
            surrender = 1
        return flag, surrender, hand_one, hand_two, player, shuffle_deck, user

    def split_hands(self, hand_one, hand_two, shuffle_deck):
        choice = int(input("\nWhich hand do you want to use?\nType 1 or 2: "))
        Next = 0
        while Next == 3 or Next == 0:
            if choice == 1:
                print("\nHand One Chosen")
                Next = int(input("\npick an action:\n1.) Hit\n2.) Double Down\n3.) Switch Hands"))
                if Next == 1:
                    hand_one.append(shuffle_deck[0])
                    shuffle_deck.pop(0)
                    flag = 0
                elif Next == 2:
                    hand_one.append(shuffle_deck[0])
                    shuffle_deck.pop(0)
                    flag = 1
                elif Next == 3:
                    print("\nSwitching hands")
                    choice = 2
            elif choice == 2:
                print("\nHand Two Chosen")
                Next = int(input("\npick an action:\n1.) Hit\n2.) Double Down\n3.) Switch Hands"))
                if Next == 1:
                    hand_two.append(shuffle_deck[0])
                    shuffle_deck.pop(0)
                    flag = 0
                elif Next == 2:
                    hand_two.append(shuffle_deck[0])
                    shuffle_deck.pop(0)
                    flag = 1
                elif Next == 3:
                    print("\nSwitching hands")
                    choice = 1
        return flag, hand_one, hand_two, choice, shuffle_deck

    def DealerAction(self, shuffle_deck, dealer):
        dealer_sum = sum(dealer)
        if dealer_sum >= 17:
            pass
        elif dealer_sum <= 16:
            dealer.append(shuffle_deck[0])
            shuffle_deck.pop(0)
        return dealer_sum, dealer, shuffle_deck

    def WinLose(self, user, flag, surrender, dealer_sum, player, hand_one, hand_two):
        if surrender == 1 or dealer_sum == 21:
            print("YOU LOSE!")
        elif dealer_sum > 21:
            print("DEALER BUST!")
        elif sum(player) > 21:
            print("BUST!")
        elif flag == 1:
            if user != 3:
                if sum(player) > 21:
                    print("BUST!")
                elif sum(player) > dealer_sum:
                    print("YOU WIN!")
                elif sum(player) == 21:
                    print("YOU WIN!")
                elif sum(player) < dealer_sum:
                    print("YOU LOSE!")
                elif sum(player) == dealer_sum:
                    print("DRAW GAME")
            if user == 3:
                if sum(hand_one) > 21 or sum(hand_two) > 21:
                    print("BUST!")
                elif sum(hand_one) > dealer_sum or sum(hand_two) > dealer_sum:
                    print("YOU WIN!")
                elif sum(hand_one) == 21 or sum(hand_two) == 21:
                    print("YOU WIN!")
                elif sum(hand_one) < dealer_sum or sum(hand_two) < dealer_sum:
                    print("YOU LOSE!")
                elif sum(hand_one) == dealer_sum or sum(hand_two) == dealer_sum:
                    print("DRAW GAME!")
        elif flag == 0:
            if user != 3:
                if sum(player) > 21:
                    print("BUST!")
                    flag = 1
                elif sum(player) == 21:
                    print("YOU WIN!")
                    flag = 1
            if user == 3:
                if sum(hand_one) > 21 or sum(hand_two) > 21:
                    print("BUST!")
                    flag = 1
                elif sum(hand_one) == 21 or sum(hand_two) == 21:
                    print("YOU WIN!")
                    flag = 1
        return flag
               
def test():
    #YOU CAN PLACE YOUR EXPERIMENTAL/Testing CODE HERE :)
    pass

#_______________________________MAIN FUNCTION_____________________________
def main():
    start = int(input("\nWelcome to Cashless Blackjack!\n\n1.)start\n2.)Exit\nPlease type 1 or 2:"))
    if start == 2:
        print("Exiting Game...")
        time.sleep(5)
        raise SystemExit
    while True:
        black = game()
        user, surrender, flag = 0, 0, 0
        shuffle_deck, player, dealer = black.first_dealing()
        hand_one, hand_two = [], []
        while flag == 0 and surrender == 0:
            if user != 3:
                flag, surrender, hand_one, hand_two, player, shuffle_deck, user = black.PlayerAction(shuffle_deck, player, flag, surrender)
                if hand_one != []:
                    print("player:", hand_one, hand_two)
                elif hand_one == []:
                    print("player's total:", sum(player),"\nplayer's deck: ", player)
            elif user == 3:
                flag, hand_one, hand_two, choice, shuffle_deck = black.split_hands(hand_one, hand_two, shuffle_deck)
                if choice == 2:
                    print("hand two's total:", sum(hand_two),"\nhand two's deck", hand_two)
                elif choice == 1:
                    print("hand one's total:", sum(hand_one),"\nhand one's deck", hand_one)
            dealer_sum, dealer, shuffle_deck = black.DealerAction(shuffle_deck, dealer)
            print("n\ndealer's hands:", dealer[0], "Face Down")
            flag = black.WinLose(user, flag, surrender, dealer_sum, player, hand_one, hand_two)
            if flag == 1 or surrender == 1 or dealer_sum == 21 or dealer_sum > 21 or sum(player) > 21:
                user = str(input("\nPlay again?\n Yes or No?\n please type y or n: "))
                if user == "y":
                    break
                else:
                    print("\nThank you for playing, closing game in 5 seconds")
                    print("\nClosing...")
                    time.sleep(5)
                    raise SystemExit
            
if __name__ == '__main__':
    main()



"""
OLD TESTING CODE:
while True:
        black = game()
        user, surrender, flag = 0, 0, 0
        shuffle_deck, player, dealer = black.first_dealing()
        print("deck: ", shuffle_deck, "\n")
        hand_one, hand_two = [], []
        while flag == 0 and surrender == 0:
            flag, surrender, hand_one, hand_two, player, shuffle_deck, user = black.PlayerAction(shuffle_deck, player, flag, surrender)
            print("deck: ", shuffle_deck, "\n")
            print("player: ", flag, surrender, hand_one, hand_two, player)
            dealer_sum, dealer, shuffle_deck = black.DealerAction(shuffle_deck, dealer)
            print("dealer: ", dealer_sum, dealer, "\n")
            print("deck: ", shuffle_deck, "\n")
            black.WinLose(user, flag, surrender, dealer_sum, player, hand_one, hand_two)
            if flag == 1 or surrender == 1 or dealer_sum == 21 or dealer_sum > 21 or sum(player) > 21:
                user = int(input("Play again?\ntype in the corresponding action's number\n1.) Yes or 2.) No: "))
                if user == 1:
                    break
                elif user == 2:
                    print("Thank you for playing, closing game in 10 seconds")
                    print("Closing...")
                    time.sleep(10)
                    raise SystemExit
"""