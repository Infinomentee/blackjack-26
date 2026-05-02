import random
import os

# =========================
# CLEAR SCREEN (WORKS ON WINDOWS + LINUX)
# =========================

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# =========================
# DECK
# =========================

def create_deck():
    suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
    values = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']

    deck = [f"{v} of {s}" for s in suits for v in values]
    deck *= 5
    random.shuffle(deck)
    return deck


# =========================
# HAND VALUE
# =========================

def check_hand(hand):
    total = 0
    aces = 0

    for card in hand:
        value = card.split()[0]

        if value in ['Jack', 'Queen', 'King']:
            total += 10
        elif value == 'Ace':
            total += 11
            aces += 1
        else:
            total += int(value)

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


# =========================
# PLAYER TURN
# =========================

def player_turn(deck):
    hand = [deck.pop(), deck.pop()]

    while True:
        clear()
        print("YOUR HAND:", hand, check_hand(hand))

        choice = input("Hit or Stay? (h/s): ").lower()

        if choice == "h":
            hand.append(deck.pop())

            if check_hand(hand) > 21:
                clear()
                print("BUST! You lose.")
                return hand

        else:
            return hand


# =========================
# DEALER TURN
# =========================

def dealer_turn(deck):
    hand = [deck.pop(), deck.pop()]

    while check_hand(hand) < 17:
        hand.append(deck.pop())

    return hand


# =========================
# COMPARE RESULTS
# =========================

def compare(player, dealer):
    clear()

    p = check_hand(player)
    d = check_hand(dealer)

    print("PLAYER:", player, p)
    print("DEALER:", dealer, d)

    if p > 21:
        print("\nDealer wins (you busted)")
    elif d > 21:
        print("\nPlayer wins (dealer busted)")
    elif p > d:
        print("\nPlayer wins")
    elif p < d:
        print("\nDealer wins")
    else:
        print("\nTie")


# =========================
# GAME ENTRY
# =========================

def run_game():
    clear()
    print("BLACKJACK START\n")

    deck = create_deck()

    player = player_turn(deck)
    dealer = dealer_turn(deck)

    compare(player, dealer)


# =========================
# START
# =========================

if __name__ == "__main__":
    run_game()