def get_current_score(hand):
    score = sum([card[1] for card in hand])
    # checking for Aces in hand and adjusting Ace value based on current score
    for i in range(len(hand)):
        card_name = hand[i][0]
        card_value = hand[i][1]
        if 'Ace' in card_name:
            if card_value == 1 and score + 10 <= 21:
                card_value = 11
                score += 10
            elif card_value == 11 and score > 21 and score - 10 <=21:
                card_value = 1
                score -= 10
            else:
                card_value = card_value
            new_card = [card_name, card_value]
            hand[i] = new_card
    return hand, score
