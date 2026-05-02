import random
import os

# -------------------------
# Utility
# -------------------------

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def my_shuffle(array):
    random.shuffle(array)
    return array


# -------------------------
# Player
# -------------------------

class BlackJackPlayer():
    def __init__(self, name, bank, amount=25):
        self.name = name
        self.bank = bank
        self.amount = amount

    def __str__(self):
        return f"AVAILABLE BANK: {self.bank}\n"

    def bet(self, number):
        self.amount = number
        self.bank -= self.amount
        deck(self.name)


# -------------------------
# GAME START (REPLACED BUTTON)
# -------------------------

def start_blackjack():
    clear()
    print("WELCOME TO BLACKJACK!")

    name_input = input("Enter your name: ")

    global BLACKJACK_CURRENT_PLAYER
    BLACKJACK_CURRENT_PLAYER = BlackJackPlayer(name_input, 200)

    go_to_bet()


# -------------------------
# DECK
# -------------------------

def deck(deck_player):
    full_deck = []
    four_suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
    deck_base = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']

    while four_suits:
        for i in deck_base:
            full_deck.append(f"{i} of {four_suits[0]}")
        four_suits.pop(0)

    five_decks = full_deck * 5
    final_deck = my_shuffle(five_decks)

    deal(final_deck)


# -------------------------
# DEAL
# -------------------------

def deal(incoming_deck):
    global card_next_up, players_hand, dealers_card, this_deck

    card_next_up = 3
    this_deck = incoming_deck

    dealers_card = this_deck[0]
    players_hand = this_deck[1:card_next_up]

    print(f"\nDEALER SHOWS: {dealers_card}")
    print(f"YOUR CARDS: {players_hand} ({check_hand(players_hand)})")

    player_turn()


# -------------------------
# PLAYER TURN (REPLACES BUTTONS)
# -------------------------

def player_turn():
    global card_next_up, players_hand, dealers_card, this_deck

    while True:
        print(f"\nYOUR CARDS: {players_hand} ({check_hand(players_hand)})")

        choice = input("Hit or Stay? (h/s): ").lower()

        if choice == "h":
            card_next_up += 1
            players_hand = this_deck[1:card_next_up]

            if check_hand(players_hand) > 21:
                print("BUST! You lose.")
                go_to_bet()
                return

            if check_hand(players_hand) == 21:
                dealer_plays_next(players_hand, dealers_card, this_deck)
                return

        elif choice == "s":
            dealer_plays_next(players_hand, dealers_card, this_deck)
            return


# -------------------------
# DEALER
# -------------------------

def dealer_plays_next(hand_to_beat, dealers_first_card, rest_of_the_deck):

    dealer_deck = rest_of_the_deck
    dealer_deck.insert(0, str(dealers_first_card))

    dealers_hand = dealer_deck[0:2]

    dealers_points = check_hand(dealers_hand)
    dplayers_points = check_hand(hand_to_beat)

    if dealers_points >= 17:
        print(f"DEALER: {dealers_hand} ({dealers_points})")

        if dealers_points > 21:
            display_who_won('busted')
        elif dealers_points > dplayers_points:
            print("DEALER WINS!")
        elif dealers_points == dplayers_points:
            display_who_won('tie')
        else:
            display_who_won('player')

        go_to_bet()
        return

    else:
        while check_hand(dealers_hand) < 17:
            dealers_hand = dealer_deck[:len(dealers_hand)+1]
            print(f"DEALER: {dealers_hand} ({check_hand(dealers_hand)})")

        if check_hand(dealers_hand) > 21:
            display_who_won('busted')
        elif check_hand(dealers_hand) > dplayers_points:
            print("DEALER WINS!")
        elif check_hand(dealers_hand) == dplayers_points:
            display_who_won('tie')
        else:
            display_who_won('player')

        go_to_bet()


# -------------------------
# HAND VALUE
# -------------------------

def check_hand(to_check):
    count_it = 0

    for i in to_check:
        card = i.split()[0]

        if card == 'Ace':
            count_it += 11
        elif card in ['Jack','Queen','King']:
            count_it += 10
        else:
            count_it += int(card)

    ace_count = sum(1 for c in to_check if c.startswith("Ace"))

    while count_it > 21 and ace_count > 0:
        count_it -= 10
        ace_count -= 1

    return count_it


# -------------------------
# WIN DISPLAY
# -------------------------

def display_who_won(outcome):
    if outcome == 'tie':
        print("TIE!")
    elif outcome == 'player':
        BLACKJACK_CURRENT_PLAYER.bank += BLACKJACK_CURRENT_PLAYER.amount * 2
        print("YOU WIN!")
    elif outcome == 'busted':
        BLACKJACK_CURRENT_PLAYER.bank += BLACKJACK_CURRENT_PLAYER.amount * 2
        print("DEALER BUSTED! YOU WIN!")


# -------------------------
# BETTING
# -------------------------

def go_to_bet():
    if BLACKJACK_CURRENT_PLAYER.bank < 25:
        print("Game over - no cash left")
        return

    print(f"\nBANK: {BLACKJACK_CURRENT_PLAYER.bank}")
    bet = int(input("Enter bet (min 25): "))

    BLACKJACK_CURRENT_PLAYER.bet(bet)


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":
    start_blackjack()