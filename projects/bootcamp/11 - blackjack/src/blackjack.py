import random

# Game's card
cards = [11, 3, 4, 5, 6, 7, 8, 2]
user_cards = []
computer_cards = []
is_game_over = False

# Function that usus the list to return a random card
def deal_card(cards: list) -> int:
    card = random.choice(cards)
    return card

# Deal the user and computer 2 cards each using deal_card()
for _ in range(2):
    user_cards.append(deal_card(cards))
    computer_cards.append(deal_card(cards))

# Create a function called calculate_score() that take a list of cards and return the score
def calculate_score(cards: list) -> int:
    # Inside calculate_score() check for blackjack (a hand with only 2 cards: ace + 10) and return 0 instead of the actual score. 0 will represent a blackjack in our game.
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    # Inside calculate_score() check for an 11 (ace). If the score is over 21 remove the 11 and replace it with a 1.
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(user_score: int, computer_score: int) -> str:
    if user_score == computer_score:
        return 'Draw'
    elif computer_score == 0:
        return 'Lose, opponent has Blackjack'
    elif user_score == 0:
        return 'Win, with a Blackjack'
    elif user_score > 21:
        return 'You went over. You lose.'
    elif computer_score > 21:
        return 'Opponent went over. You win.'
    elif user_score > computer_score:
        return 'You win.'
    else:
        return 'You lose.'

while not is_game_over:
    # User and Computer score
    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    print(f'Your cards: {user_cards}, Current score: {user_score}')
    print(f'Computer cards: {computer_cards}, Current score: {computer_score}')

    # Call calculate_score(). If the computer or the user has a blackjack(0) or if the score is over 21, then the game end.
    if user_score == 0 or computer_score == 0 or user_score > 21:
        is_game_over = True
        print('Game over')
    else:
        user_should_play = input(
            'Type "y" to get another card, type "n" to pass:')
        if user_should_play.lower == "y":
            user_cards.append(deal_card(cards))
        else:
            is_game_over = True
            print('Game over')

while computer_score != 0 and computer_score < 17:
    computer_cards.append(deal_card(cards))
    computer_score = calculate_score(computer_cards)

print(compare(user_score, computer_score))
print(f'Your cards: {user_cards}, Current score: {user_score}')
print(f'Computer cards: {computer_cards}, Current score: {computer_score}')