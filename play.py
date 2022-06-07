from scoring import get_current_score


def hit_and_append(cards, hand):
    new_card = cards.hit()
    # adding new card to hand
    hand.append(new_card)
    # updating score
    hand, score = get_current_score(hand)
    return hand, score


def soft_play_hand(hand, score, cards, threshold):
    dealer_1_card = hand[0]
    dealer_2_card = hand[1]
    if "Ace" in dealer_1_card[0] or "Ace" in dealer_2_card[0]:
        if score == 17:
            hand, score = hit_and_append(cards, hand)
    while score < threshold:
        hand, score = hit_and_append(cards, hand)
    return score


def value_play_hand(hand, score, cards, threshold):
    while score < threshold:
        hand, score = hit_and_append(cards, hand)
    return score


def situation_play_hand(hand, score, cards, threshold, dealer_card):
    hit = True
    while hit:
        if score >= 12:
            if dealer_card[1] >= 2:
                if dealer_card[1] <= 5:
                    return score
        if score > threshold:
            return score
        hand, score = hit_and_append(cards, hand)


def basic_play_hand(hand, score, cards, threshold, dealer_card, already_split=False):
    # Checking if there is an ace in the hand initially to evaluate soft hand totals, also accounts for split Aces
    ace_in_hand = False
    if len(hand) > 1:
        player_1_card = hand[0]
        player_2_card = hand[1]
        if "Ace" in player_1_card[0] or "Ace" in player_2_card[0]:
            ace_in_hand = True
    else:
        player_1_card = hand[0]
        if "Ace" in player_1_card[0]:
            ace_in_hand = True

    # Getting dealer card name and value
    dealer_card_val = dealer_card[1]
    dealer_card_name = dealer_card[0]
    # Incorporating double down betting - default is no double down has occurred
    double_down = False
    # To activate loop
    playing = True
    # To check if the player has already hit to check if doubling down is available based on totals
    already_hit = False
    while playing:
        # Soft total decisions for hand with an ace and another card in hand
        if ace_in_hand and not already_hit and len(hand) == 2:
            # Standing scenarios for soft totals
            if score == 20:
                return score, double_down
            if score == 19 and dealer_card_val != 6:
                return score, double_down
            if score == 18 and (dealer_card_val == 7 or dealer_card_val == 8):
                return score, double_down

            # Double down scenarios for soft totals
            if score == 19 and dealer_card_val == 6:
                if not already_split:
                    hand, score = hit_and_append(cards, hand)
                    double_down = True
                    return score, double_down
                else:
                    return score, double_down
            if score == 18 and (dealer_card_val <= 6 and "Ace" not in dealer_card_name):
                if not already_split:
                    hand, score = hit_and_append(cards, hand)
                    double_down = True
                    return score, double_down
                else:
                    return score, double_down
            if score == 17 and dealer_card_val <= 6:
                if dealer_card_val <= 3:
                    if not already_split:
                        hand, score = hit_and_append(cards, hand)
                        double_down = True
                        return score, double_down
            if (score == 16 or score == 15) and dealer_card_val <= 6:
                if dealer_card_val <= 4:
                    if not already_split:
                        hand, score = hit_and_append(cards, hand)
                        double_down = True
                        return score, double_down
            if (score == 13 or score == 14) and (dealer_card_val == 5 or dealer_card_val == 6):
                if not already_split:
                    hand, score = hit_and_append(cards, hand)
                    double_down = True
                    return score, double_down
            hand, score = hit_and_append(cards, hand)
            already_hit = True

        # Standing scenarios
        if score > threshold:
            return score, double_down
        if score >= 13 and (dealer_card_val <= 6 and "Ace" not in dealer_card_name):
            return score, double_down
        if score == 12 and (dealer_card_val == 4 or dealer_card_val == 5 or dealer_card_val == 6):
            return score, double_down
        # Double down scenarios
        if score == 11:
            if not already_hit and not already_split:
                hand, score = hit_and_append(cards, hand)
                double_down = True
                return score, double_down
        if score == 10:
            if not already_hit and not already_split and (dealer_card_val != 10 or "Ace" not in dealer_card_name):
                hand, score = hit_and_append(cards, hand)
                double_down = True
                return score, double_down
        if score == 9:
            if not already_hit and not already_split and dealer_card_val <= 6:
                if dealer_card_val >= 3:
                    hand, score = hit_and_append(cards, hand)
                    double_down = True
                    return score, double_down
        # If no conditions above met, then hit
        hand, score = hit_and_append(cards, hand)
        already_hit = True
